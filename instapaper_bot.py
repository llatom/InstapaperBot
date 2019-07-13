# -*- coding: utf-8 -*-
__author__ = 'cderek'

import getpass
import requests
from bs4 import BeautifulSoup 

headers = {
        'Content-Type': 'text/html;charset=UTF-8',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
        }

#文章列表
article_list = []
#Instapaper 的用户名和密码
# username = "
# password = ""

uid = '6c63c9f570f8'
#TODO

def user_login():
    username = raw_input("请输入用户名: ")
    password = getpass.getpass("请输入用户密码: ")
    main(username, password)

def fetch_data(url):
    try:
        respones = requests.get(url,headers = headers)
        respones.encoding = 'utf-8'
        if respones.status_code == 200:
            return respones.text
        return None
    except RequestException:
        print('请求索引页错误')
        return None

#URL 解析器, 获取文章列表
def parse_article_list(html):
    soup = BeautifulSoup(html,'lxml')
    note_list = soup.find_all('ul',class_ = 'note-list')[0]
    content_li = note_list.find_all("li")
    dir = {}
    for link in content_li:
        url = link.find_all('a',class_ = 'title')[0]
        href = url['href']
        title = url.text
        link="https://www.jianshu.com"+url.get("href")
        dir[link] = title
        article_list.append(link)


def main(username, password):
    html = fetch_data("https://www.jianshu.com/u/{}?order_by=shared_at&page={}".format(uid, 1))
    soup = BeautifulSoup(html,'lxml')

    #获取文章数量和最大页数
    article_num = int(soup.find_all('div',class_ = 'info')[0].find_all("li")[2].find_all('p')[0].text)
    max_page_num = article_num / 9

    #翻页序列
    pages = range(0, max_page_num)
    for page in pages:
        html = fetch_data("https://www.jianshu.com/u/{}?order_by=shared_at&page={}".format(uid, page))
        parse_article_list(html)

    for article in article_list:
        params = {'username':username, 'password':password, 'url':article, 'auto-title':1}
        pg = requests.post("https://www.instapaper.com/api/add", params)
        if str(pg.status_code) == "201":
            print u"添加成功：" + article
        elif str(pg.status_code) == "400":
            print u"错误代码400: 可能缺少必要的参数，比如url"+ article
        elif str(pg.status_code) == "403":
            print u"错误代码403：无效的用户名和密码，"+ article
        elif str(pg.status_code) == "500":
            print u"错误代码500：服务器出了点小问题，请稍后再试，"+ article


if __name__ == '__main__':
    user_login()
