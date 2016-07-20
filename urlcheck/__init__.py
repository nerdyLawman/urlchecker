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
    Main function of the boilerplate code is the entry point of the 'urlcheck' executable script (defined in setup.py).
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true",
        help="increase output verbosity")
    parser.add_argument("-r", "--remote", action="store_true",
        help="take user supplied urls to check links")
    parser.add_argument("-l", "--local", action="store_true",
        help="take user supplied .html files to check links")
    parser.add_argument("-c", "--current", action="store_true",
        help="search cwd for .html files to validate")
    parser.add_argument("files", nargs="*",
        help="URLs to check")
    args = parser.parse_args()
    
    if args.remote or args.local:
        htmlfiles = args.files
    else:
        htmlfiles = glob.glob('./*.html')
    if htmlfiles:
        for htmlfile in htmlfiles:
            errors = ""
            if args.remote:
                f = urllib.urlopen(htmlfile)
                data = f.read()
            else:
                if htmlfile[-5:] == '.html':
                    filename = htmlfile
                    with open(filename, 'r') as infile:
                        data = infile.read()
                else:
                    print "File must be .html"
            page = str(BeautifulSoup(data))
            errors = ""
            while True:
                url, n = getURL(page)
                page = page[n:]
                if url:
                    if url[:4] == "http":
                        resp = requests.head(url)
                        print str(resp.status_code) + ' :: ' + url + '\n'
                        if resp.status_code > 399:
                            errors += url + str(resp.status_code)
                else:
                    break
            print htmlfile
            if errors == '':
                print "It all checks out, boy-o!"
            else:
                print "You've got some problems!"
    else:
        print "No HTML files in directory or supplied"

