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

def main():
    '''
    Main function of the boilerplate code is the entry point of the 'urlcheck'
    executable script (defined in setup.py).
    
    '''
    
    # parsers
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true",
        help="increase output verbosity")
    parser.add_argument("-r", "--remote", action="store_true",
        help="take user-supplied URLS to check")
    parser.add_argument("-l", "--local", action="store_true",
        help="take user-supplied .HTML files to check")
    parser.add_argument("-c", "--current", action="store_true",
        help="search current directory for .html files to validate")
    parser.add_argument("html", nargs="*",
        help="URLS or FILES s to check links")
    args = parser.parse_args()
    
    if args.remote or args.local:
        htmlfiles = args.html
    else:
        htmlfiles = glob.glob('./*.html')
    
    if htmlfiles:
        for htmlfile in htmlfiles:
            errors = []
            print "\nurlcheck for " + htmlfile + "\n"
            
            if args.remote:
                f = urllib.urlopen(htmlfile)
                data = f.read()
            else:
                if htmlfile[-5:] == '.html':
                    filename = htmlfile
                    with open(filename, 'r') as infile:
                        data = infile.read()
                else:
                    print "Files must be .html"
            
            page = str(BeautifulSoup(data))
            
            # link checking loop
            while True:
                url, n = getURL(page)
                page = page[n:]
                if url:
                    if url[:4] == "http":
                        resp = requests.head(url)
                        print str(resp.status_code) + ' :: ' + url
                        if resp.status_code > 399:
                            errors.append(str(resp.status_code) + ' :: ' + url)
                    else:
                        errors.append('USL :: ' + url)
                        print "--links of this type: [" + url + "] not yet supported"
                else:
                    break
            
            print '\n-------\nRESULT\n' + htmlfile
            if args.verbose: print '>> 404 = not found\n>> USL = unsupported link type\n'
            if not errors:
                print "Everything checks out, boy-o!"
            else:
                print "The following problems found with " + htmlfile
                for error in errors:
                    print error
            raw_input("\nENTER to continue: ")
    
    else:
        print "No HTML files in directory or supplied."
    print "urlcheck completed\n"

