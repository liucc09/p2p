import scrapy
import os
from p2p.items import P2PItem
import re
import logging

class P2PSpider(scrapy.Spider):
    item_max = 20 #设一个抓取文章的上限，防止一直抓取
    url_max = 1000 #设一个访问url的上限

    item_num = 0
    url_num = 0
    
    name = "p2p"
    allowed_domains = ["sohu.com","ifeng.com","news.baidu.com"] #将一些主要新闻网站加入抓取范围，当然baidu也得加入其中，因为翻页后还在baidu域名下面
    start_urls = [
        "https://news.baidu.com/ns?word=p2p"   #在百度新闻搜索中搜“p2p”
    ]

    def parse(self, response):
        logging.info(f'enter baidu : {response.url}')
        url_res = response.css("div.result h3.c-title a::attr(href)").extract()  #提取新闻的url

        url_page = response.css("p#page a::attr(href)").extract() #提取翻页的url

        for u in url_res:
            self.url_num += 1
            
            if (self.url_num < self.url_max) and (self.item_num < self.item_max):
                logging.debug(f'url id {self.url_num}/{self.url_max} : {u}')
                if "sohu.com" in u:
                    yield scrapy.Request(u,callback=self.parse_sohu) #由于不同站点的html格式不一样，所以callback调用不同函数分别处理
                elif "ifeng.com" in u:
                    yield scrapy.Request(u,callback=self.parse_ifeng)
            


        for u in url_page:
            u = response.urljoin(u)
            self.url_num += 1
            
            if (self.url_num < self.url_max) and (self.item_num < self.item_max):
                logging.debug(f'url id {self.url_num}/{self.url_max} : {u}')
                if "news.baidu.com" in u:
                    yield scrapy.Request(u,callback=self.parse)
            

    def parse_sohu(self,response):
        logging.info(f'parse sohu {self.item_num}/{self.item_max}: {response.url}')
        
        title = response.css("div.text-title h1::text").extract_first()
        content = ''.join(response.xpath("//article//text()").extract())
        
        if (title is not None) and (content is not None):
            item = P2PItem()
            item['url'] = response.url
            item['title'] = title.replace(' ','')
            item['domain'] = 'sohu.com'
            item['content'] = re.sub(r'\s+',r'\n',content.replace(' ',''))
            
            self.item_num+=1
            if self.item_num<self.item_max:
                return item #返回数据结构
            


    def parse_ifeng(self,response):
        logging.info(f'parse ifeng {self.item_num}/{self.item_max}: {response.url}')

        title = response.css("h1#artical_topic::text").extract_first()
        content = ''.join(response.xpath("//div[@id='main_content']//text()").extract())

        if (title is not None) and (content is not None):
            item = P2PItem()
            item['url'] = response.url

            item['title'] = title.replace(' ','')
            item['domain'] = 'ifeng.com'
            item['content'] = re.sub(r'\s+',r'\n',content.replace(' ',''))
            
            self.item_num+=1
            if self.item_num<self.item_max:
                return item
                

        
        