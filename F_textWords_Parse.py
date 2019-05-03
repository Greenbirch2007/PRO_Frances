#! -# ! -*- coding:utf-8 -*-

import time
import re
import pymysql
import requests
from selenium import webdriver
# 还是要用PhantomJS
import datetime
import string
from lxml import etree

from s_links import f_list

driver = webdriver.Chrome()
#　因为只做一次，所以尽可能要全面！

def call_pages(url):
    driver.get(url)
    time.sleep(1)
    html = driver.page_source

    return html


def parse_pages(html):
    big_list = []
    selector = etree.HTML(html)
    F_word1 = selector.xpath('/html/body/div[5]/div[2]/table/tbody/tr/td[3]/div/span/text()')
    F_word2 = selector.xpath('/html/body/div[5]/div[2]/table/tbody/tr/td[4]/div/span/text()')
    A_word = selector.xpath('/html/body/div[5]/div[2]/table/tbody/tr/td[6]/div/span/text()')




    for i1,i2,i3 in zip(F_word1, F_word2,A_word):
        big_list.append((i1,i2,i3))

    return big_list



def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='France',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # 这里是判断big_list的长度，不是content字符的长度
    try:
        cursor.executemany('insert into ALlText_words_Parse (F_word1,F_word2,A_word) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except Exception :
        print('出列啦')







if __name__ == '__main__':
    for url in f_list:

        html = call_pages(url)
        content = parse_pages(html)
        insertDB(content)
        print(url)









#
# create table ALlText_words_Parse (
# id int not null primary key auto_increment,
# F_word1 varchar(80),
# F_word2 varchar(80),
# A_word text
# ) engine =InnoDB charset=utf8;
# # #
# drop table ALlText_words_Parse;
#


#





