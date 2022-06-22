import requests
from bs4 import BeautifulSoup
import re
import sys


def get_page_content(url):
    request = requests.get(url)
    if request.status_code == 200:
        return request.text


def extract_gtm(page_content):
    match = re.search(r"Google Tag Manager -->(.*?'(GTM-[0-9a-zA-Z]+)'.*?)<!-- End Google Tag Manager", page_content, re.DOTALL)
    if match is not None:
        return match.group(2)


def get_links(page_content, main_url):
    uniq_urls = set()
    soup = BeautifulSoup(page_content, "html.parser")
    for link in soup.findAll('a'):
        url = link.get('href')
        if url:
            url = url.split('#')[0]
        if url:
            if url.count('/') > int(sys.argv[2]):
                continue
        if url:
            if main_url in url:
                url = url.replace(main_url, '')
            if url.startswith('http://') or url.startswith('https://') or url.startswith('mailto:') or re.search('.pdf', url) is not None or re.search('.jpg', url) is not None:
                continue

            uniq_urls.add(url)
    return uniq_urls