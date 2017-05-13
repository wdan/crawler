import urllib2
import wget
import grequests
import json

if __name__ == '__main__':
    with open('eurovis.json', 'r') as inputFile:
        paperList = json.load(inputFile)
        for paper in paperList:
            year = paper['year']
            folder = 'pdf/' + year + '/'
            title = paper['title'].replace(':', '-')
            url = paper['url']
            print url
            filename = folder + title + '.pdf'
            # wget.download(url, filename)
