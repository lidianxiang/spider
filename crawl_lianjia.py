# !/usr/bin/env python
# -*- coding:utf-8  -*-
# author : lidianxiang 
# time:2018/7/17
import time
import re
import requests
from bs4 import BeautifulSoup
from parsel import Selector
import pandas as pd

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
}
pages = ['https://sh.lianjia.com/ershoufang/pg{}'.format(x) for x in range(1,100)]

lj_shanghai = pd.DataFrame(columns=['code','dec','img'])
count = 0

def l_par_html(url):
    wr = requests.get(url,headers = headers,stream = True)
    sel = Selector(wr.text)
    describe = sel.xpath('//li[@class="clear LOGCLICKDATA"]//text()').extract()
    new_information = ([x for x in describe if x != '关注' and x != '加入对比'])
    sep_info = ' '.join(new_information).split(r'/平米')[:-1]

    hou_code = sel.xpath('//li[@class ="clear LOGCLICKDATA"]/a/@data-housecode').extract()
    hou_image = sel.xpath('//li[@class = "clear LOGCLICKDATA"]/a/img/@data-original').extract()
    pages_info = pd.DataFrame(list(zip(hou_code,sep_info,hou_image)),columns=['code','dec','img'])
    return pages_info

for page in pages:
    a = l_par_html(page)
    count += 1
    print('the ' + str(count) + ' page is successful')
    time.sleep(5)
    lj_shanghai = pd.concat([lj_shanghai,a],ignore_index=True)

lj_shanghai.to_csv('d:\\lian_jia_shanghai.csv')