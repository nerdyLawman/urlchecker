'''
urlcheck: Main module

Copyright 2016, Art Luman
Licensed under MIT.
'''

import requests, glob, argparse, urllib
from BeautifulSoup import BeautifulSoup

def getURL(page):
    """
    :param page: html of web page (here: Python home page) 
    :return: urls in that page 
    """
    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote

def colorize(output, color):
    """
    returns a string formatted with a ANSI color codes
    for purtier output,
    """
    
    ansiYellow = '\x1B[1;33;40m'
    ansiRed = '\x1B[1;31;40m'
    ansiCyan = '\x1B[1;36;40m'
    ansiGreen = '\x1B[1;32;40m'
    ansiMagenta = '\x1B[1;35;40m'
    ansiReset = '\x1B[m'
    
    if color == 'r':
        ansiColor = ansiRed
    elif color == 'y':
        ansiColor = ansiYellow
    elif color == 'c':
        ansiColor = ansiCyan
    elif color == 'g':
        ansiColor = ansiGreen
    elif color == 'm':
        ansiColor = ansiMagenta
    else:
        ansiColor = ansiReset
    
    return(ansiColor + output + ansiReset)


def main():
    """"
    urlcheck is a commandline app that will verify hyperlinks of a HTML file
    and report a list of errors if any are found.
    
    """
    
    # explanations for verbose output
    resultTypes = ('\nCommon Status Codes:\n\n'
        '>> 400 = bad request\n'
        '>> 401 = unauthorized\n'
        '>> 403 = forbidden\n'
        '>> 404 = url not found\n'
        '>> 408 = request timeout\n'
        '>> 500 = internal server error\n'
        '>> 502 = bad gateway\n'
        '>> 503 = service unavailable\n'
        '>> 504 = gateway timeout\n'
        '>> USL = unsupported link type\n\n'
        'for more codes and info, see:\nhttps://en.wikipedia.org/wiki/List_of_HTTP_status_codes\n')
    
    # parsers
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
        help='increase output verbosity')
    parser.add_argument('-r', '--remote', action='store_true',
        help="take user-supplied URLS to check")
    parser.add_argument('-l', '--local', action='store_true',
        help='take user-supplied .HTML files to check')
    parser.add_argument('-c', '--current', action='store_true',
        help='search current directory for .html files to validate')
    parser.add_argument('html', nargs='*',
        help='URLS or FILES s to check links')
    args = parser.parse_args()
    
    if args.remote or args.local:
        htmlfiles = args.html
    else:
        htmlfiles = glob.glob('./*.html')
    
    if htmlfiles:
        for htmlfile in htmlfiles:
            errors = []
            print(colorize('\nurlcheck for ' + htmlfile + '\n', 'c'))
            
            if args.remote:
                f = urllib.urlopen(htmlfile)
                data = f.read()
            else:
                if htmlfile[-5:] == '.html':
                    filename = htmlfile
                    with open(filename, 'r') as infile:
                        data = infile.read()
                else:
                    print(colorize('Files must be .html', 'r'))
            
            page = str(BeautifulSoup(data))
            
            # link checking loop
            while True:
                url, n = getURL(page)
                page = page[n:]
                if url:
                    if url[:4] == 'http':
                        resp = requests.head(url)
                        printColor = 'g'
                        if resp.status_code > 399:
                            errors.append(colorize(str(resp.status_code) + ' :: ' + url, 'r'))
                            printColor = "r"
                        print(colorize(str(resp.status_code) + ' :: ' + url, printColor))
                    else:
                        errors.append(colorize('USL :: ' + url, 'y'))
                        print(colorize('USL :: ' + url, 'y'))
                else:
                    break
            
            print(colorize('\n-------\nRESULT for ' + htmlfile, 'c'))
            if args.verbose: print(colorize(resultTypes, 'm'))
            if not errors:
                print(colorize('\nEverything checks out!', 'c'))
            else:
                print(colorize('Found ' + str(len(errors)) + ' ERRORS in ' + htmlfile + ':\n', 'c'))
                for error in errors:
                    print(error)
            if htmlfiles.index(htmlfile) >= len(htmlfiles):
                raw_input('\nENTER to continue: ')
    
    else:
        print(colorize('No HTML files in directory or supplied.', 'y'))
    print(colorize('\nurlcheck completed!\n', 'c'))

