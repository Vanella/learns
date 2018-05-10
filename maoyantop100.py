# -*- coding: utf-8 -*-
"""
Created on Wed May  9 17:08:38 2018

@author: jx
"""

import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool
def get_one_page(url):
    headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    } 
    try:
        resp=requests.get(url,headers=headers)
        if resp.status_code==200:
            return resp.text
        return None
    except RequestException:
        return None

#解析html代码
def parse_one_page(html):
    print(html)
    pattern=re.compile('<dd>.*?board-index.*?">(\d+)</i>.*?board-img".*?"(.*?)".*?name.*?title="(.*?)".*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?interger">(.*?)</i>.*?fraction">(\d)</i>.*?</dd>',re.S)
    results=re.findall(pattern,html)
    print(results)
    for item in results:
    	yield{
    		'index':item[0],
    		'img':item[1],
    		'title':item[2],
    		'star':item[3].strip()[3:],
    		'releasetime':item[4].strip()[5:],
    		'score':item[5]+item[6]
    	}

def write_to_file(content):
	with open('maoyantop100.text','a',encoding='utf-8') as f:
		f.write(json.dumps(content,ensure_ascii=False)+'\n')
		f.close()

def main(offset):
    url="http://maoyan.com/board/4?offset="+str(offset)
    html=get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)
                
if __name__=='__main__':
    pool=Pool()
    pool.map(main,[i*10 for i in range(10)])
    