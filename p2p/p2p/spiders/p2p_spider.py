import scrapy
import os
from p2p.items import P2PItem

class P2PSpider(scrapy.Spider):
    item_max = 20 #设一个抓取文章的上限，防止一直抓取
    url_max = 100 #设一个访问url的上限

    item_num = 0
    url_num = 0
    
    name = "p2p"
    allowed_domains = ["sohu.com","ifeng.com","news.baidu.com"] #将一些主要新闻网站加入抓取范围，当然baidu也得加入其中，因为翻页后还在baidu域名下面
    start_urls = [
        "https://news.baidu.com/ns?word=p2p"   #在百度新闻搜索中搜“p2p”
    ]

    def parse(self, response):
        self.log(f'enter baidu : {response.url}')
        url_res = response.css("div.result h3.c-title a::attr(href)").extract()

        url_page = response.css("p#page a::attr(href)").extract()

        for u in url_res:
            self.url_num += 1
            
            if (self.url_num < self.url_max) and (self.item_num < self.item_max):
                self.log(f'url id {self.url_num}/{self.url_max} : {u}')
                if "sohu.com" in u:
                    yield scrapy.Request(u,callback=self.parse_sohu)
                elif "ifeng.com" in u:
                    yield scrapy.Request(u,callback=self.parse_ifeng)
            else:
                return


        for u in url_page:
            u = response.urljoin(u)
            self.url_num += 1
            
            if (self.url_num < self.url_max) and (self.item_num < self.item_max):
                self.log(f'url id {self.url_num}/{self.url_max} : {u}')
                if "news.baidu.com" in u:
                    yield scrapy.Request(u,callback=self.parse)
            else:
                return

    def parse_sohu(self,response):
        self.log(f'parse sohu {self.item_num}: {response.url}')

        item = P2PItem()
        item['url'] = response.url
        item['title'] = response.css("div.text-title h1::text").extract_first()
        item['domain'] = 'sohu.com'

        item['content'] = ''.join(response.xpath("//article//text()").extract())
        
        self.item_num+=1
        if self.item_num<self.item_max:
            yield item
            


    def parse_ifeng(self,response):
        self.log(f'parse ifeng {self.item_num}: {response.url}')

        
        item = P2PItem()
        item['url'] = response.url
        item['title'] = response.css("h1#artical_topic::text").extract_first()
        item['domain'] = 'ifeng.com'

        item['content'] = ''.join(response.xpath("//div[@id='main_content']//text()").extract())
        
        self.item_num+=1
        if self.item_num<self.item_max:
            yield item
            

        
        