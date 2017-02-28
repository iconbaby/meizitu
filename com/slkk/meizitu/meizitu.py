import requests
from bs4 import BeautifulSoup
import os


class Mzitu():
    def request(self, url):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content = requests.get(url, headers=headers)
        return content

    def mkdir(self, path):
        os.makedirs(os.path.join("D:\mzitu", path))
        os.chdir("D:\mzitu\\" + path)

    def save(self, img, name):
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def page(self, a, href):
        html = self.request(href)
        html_Soup = BeautifulSoup(html.text, 'lxml')
        max_span = html_Soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            # print(page_url)
            img = self.img(page_url)
            self.save(img[0], img[1])
        return max_span

    def img(self, page_url):
        img_html = requests(page_url)
        # print(img_html.text)
        img_Soup = BeautifulSoup(img_html.text, 'lxml')
        img_href = img_Soup.find('div', class_='main-image').find('img')['src']
        # print(img_href)
        name = img_href[-9:-4]
        img = requests(img_href)
        return img, name

    def home(self, all_a):
        for a in all_a:
            title = a.get_text()
            href = a['href']
            path = str(title).strip()

            self.mkdir(path)
            self.page(a, href)

    def all_url(self, url):
        start_html = self.request(url)
        Soup = BeautifulSoup(start_html.text, 'lxml')
        all_a = Soup.find('div', class_='all').find_all('a')
        self.home(all_a)


all_url = 'http://www.mzitu.com/all'
mzitu = Mzitu()
mzitu.all_url(all_url)
