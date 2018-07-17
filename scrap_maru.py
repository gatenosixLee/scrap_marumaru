from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, FancyURLopener, urlretrieve
from urllib.parse import urljoin, quote
from urllib.parse import urlencode

from os.path import splitext
import zipfile

import optparse

url_archives = 'http://wasabisyrup.com/archives/'

class AppURLopener(FancyURLopener):
    version = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'


def souping(url, decode='utf-8'):
    opener = AppURLopener()
    response = opener.open(url)
    soup = BeautifulSoup(response, 'html.parser')
    response.close()

    return soup


def test_one(url):

    opener = AppURLopener()
    opener.addheader('Referer', 'http://wasabisyrup.com')

    soup = souping(url)

    # get title
    title = soup.select('#main > div > div.top-nav.viewer-hidden > div.article-title')[0].attrs['title']

    # get all image tags
    images = soup.find_all('img', attrs={'class': 'lz-lazyload'})

    # open zip file
    zip = zipfile.ZipFile(title+'.zip', 'w')

    page_count = 1
    for image in images:
        image_url = image.attrs['data-src']
        full_url = urljoin(url, quote(image_url))
        name = image_url.split('/')[-1]

        # adjust file name.
        name = title + '_%03d%s' % (page_count, splitext(name)[-1])

        res = opener.open(full_url)

        # append image into zipfile
        zip.writestr(name, res.read())
        res.close()

        # print current progress

        print('%s of %s has saved' % (name, title))
        page_count += 1

    # close zip file
    zip.close()


def text_all(url):
    soup = souping(url)

    target_urls = [x.attrs['href'].split('/')[-1] for x in soup.select('#vContent a')]

    print ('%d found.' % len(target_urls))

    for target_url in target_urls:
        # print (url_archives + target_url)
        test_one(url_archives + target_url)

if __name__ == "__main__":
    text_all('https://marumaru.in/?c=1/28&cat=%EC%A3%BC%EA%B0%84&uid=82955')