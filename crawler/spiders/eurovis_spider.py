import scrapy
import wget
import socket
from bs4 import BeautifulSoup
from retry import retry
import urllib2

class EurovisSpider(scrapy.Spider):
    name = "eurovis"
    baseURL = 'http://onlinelibrary.wiley.com'

    def start_requests(self):
        urls = [
                # "http://onlinelibrary.wiley.com/doi/10.1111/cgf.2016.35.issue-3/issuetoc"
                # "http://onlinelibrary.wiley.com/doi/10.1111/cgf.2015.34.issue-3/issuetoc",
                # "http://onlinelibrary.wiley.com/doi/10.1111/cgf.2014.33.issue-3/issuetoc",
                # "http://onlinelibrary.wiley.com/doi/10.1111/cgf.2013.32.issue-3pt4/issuetoc",
                # "http://onlinelibrary.wiley.com/doi/10.1111/cgf.2013.32.issue-3pt3/issuetoc",
                # "http://onlinelibrary.wiley.com/doi/10.1111/cgf.2013.32.issue-3pt2/issuetoc",
                # "http://onlinelibrary.wiley.com/doi/10.1111/cgf.2013.32.issue-3pt1/issuetoc",
                # "http://onlinelibrary.wiley.com/doi/10.1111/cgf.2012.31.issue-3pt4/issuetoc",
                # "http://onlinelibrary.wiley.com/doi/10.1111/cgf.2012.31.issue-3pt3/issuetoc",
                # "http://onlinelibrary.wiley.com/doi/10.1111/cgf.2012.31.issue-3pt2/issuetoc",
                # "http://onlinelibrary.wiley.com/doi/10.1111/cgf.2012.31.issue-3pt1/issuetoc",
                # "http://onlinelibrary.wiley.com/doi/10.1111/cgf.2011.30.issue-3/issuetoc",
                "http://onlinelibrary.wiley.com/doi/10.1111/cgf.2010.29.issue-3/issuetoc"
                ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        articles = soup.find_all('div', {'class': 'tocArticle'})
        year = response.url[47:51]
        for article in articles:
            paper_url = self.baseURL + article.a['href'].replace('full', 'pdf')
            paper_title = article.a.text[0:(article.a.text.rfind('(') - 1)].replace(':', '-').replace('/', '-') + '.pdf'
            paper_page = self.urlopen_with_retry(paper_url)
            paper_soup = BeautifulSoup(paper_page, 'html.parser')
            pdf_url = paper_soup.find(id="pdfDocument")['src']
            savename = 'pdf/' + year + '/' + paper_title
            wget.download(pdf_url, savename)
            yield {'title': paper_title, 'url': pdf_url, 'year': year}

    @retry(socket.timeout, tries=5, delay=1)
    def urlopen_with_retry(self, url):
        return urllib2.urlopen(url, timeout=5).read()
