# -*- coding: utf-8 -*-
'''
web scraping
quanshuwang
'''


import requests
import re
from bs4 import BeautifulSoup

class ScrapingNovel:
    def __init__(self):
        self.session = requests.Session()

    def get_novel(self,url,title):
        index_html = self.download(url, encoding = "gbk")
        #print(index_html)
        #with open("home_page.html","wt") as file1:
        #    file1.write(index_html)
        #title = re.findall(r'<meta property="og:title" content="(.*?)" />',index_html)
        novel_chapter_info = self.get_chapter_info(index_html ) #chapter list

        self.chapter_download(title,novel_chapter_info)

        #self.save_novels(novel_chapter_info)

    def download(self, url, encoding):
        reponse = self.session.get(url)
        reponse.encoding = encoding
        html = reponse.text
        return html

    def get_chapter_info(self, index_html):
        div = re.findall(r'<div class="box_con mt10">.*?<div class="mark-box" id="mark-box">',index_html,re.S) #div is a list
        #print(div)
        #with open("chapter_list.html","wt") as chapter_file:
        #   chapter_file.write(str(div))
        info = re.findall(r'<dd data="(.*?)"><a href="(.*?)" title="(.*?)">(.*?)</a></dd>',str(div))  #info is a list
        # for i in info:
        #     print(i,"\n")
        return info

    def chapter_download(self,title,chapter_infos):
        file1 = open('%s.txt' % title,"w")
        file1.write(str(title))
        file1.write("\n")
        for chapter in chapter_infos:
            chap_url = chapter[1]
            chap_title = chapter[2]
            file1.write(str(chap_title))
            file1.write("\n")

            page = requests.get(chap_url)
            soup = BeautifulSoup(page.text, "html.parser")
            artical = soup.body.find('div',id='content').get_text()
            file1.write(str(artical))
            file1.write("\n")
        file1.close()

if __name__ == '__main__':
    quanshuwang = "https://www.xs4.cc/shuku/"
    home_page = requests.get(quanshuwang)
    home_page.encoding = "gbk"
    home_page_content = home_page.text
    #print(home_page_content)
    #home_soup = BeautifulSoup(home_page.text,"html.parser")
    novel_list = re.findall(r'<a href="(.*?)" title="(.*?)" target="_blank">.*?</a>',home_page_content)

    # print(type(novel_list),"\n")
    #print(novel_list)
    for novel in novel_list[0:100]:
        novel_url = novel[0]
        novel_title = novel[1]
        print("Downloading ", novel_title)
        spider = ScrapingNovel()
        spider.get_novel(novel_url,novel_title)

