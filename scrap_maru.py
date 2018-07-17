from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, FancyURLopener, urlretrieve
from urllib.parse import urljoin, quote
from urllib.parse import urlencode

import zipfile


class AppURLopener(FancyURLopener):
    version = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'


def souping(url, decode='utf-8'):
    opener = AppURLopener()
    response = opener.open(url)
    soup = BeautifulSoup(response, 'html.parser')
    response.close()

    return soup


def test_one():
    url = 'http://wasabisyrup.com/archives/108161'
    opener = AppURLopener()
    opener.addheader('Referer', 'http://wasabisyrup.com')

    soup = souping(url)

    # get title
    title = soup.select('#main > div > div.top-nav.viewer-hidden > div.article-title')[0].attrs['title']

    # get all image tags
    images = soup.find_all('img', attrs={'class': 'lz-lazyload'})

    # open zip file
    zip = zipfile.ZipFile(title+'.zip', 'w')

    for image in images:
        image_url = image.attrs['data-src']
        full_url = urljoin(url, quote(image_url))
        name = image_url.split('/')[-1]

        res = opener.open(full_url)

        # append image into zipfile
        zip.writestr(name, res.read())
        res.close()

        # print current progress
        print('%s of %s has saved' % (name, title))

    # close zip file
    zip.close()


if __name__ == "__main__":
    test_one()