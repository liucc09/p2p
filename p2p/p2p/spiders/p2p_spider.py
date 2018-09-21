import scrapy
import os

class P2PSpider(scrapy.Spider):
    item_max = 20 #设一个抓取文章的上限，防止一直抓取
    url_max = 20 #设一个访问url的上限
    
    name = "p2p"
    allowed_domains = ["sohu.com","ifeng.com","news.baidu.com"] #将一些主要新闻网站加入抓取范围，当然baidu也得加入其中，因为翻页后还在baidu域名下面
    start_urls = [
        "https://news.baidu.com/ns?word=p2p"   #在百度新闻搜索中搜“p2p”
    ]

    def parse(self, response):
        self.log(f'enter baidu : {response.url}')
        url_res = response.css("div.result a::attr(href)").extract()

        for u in url_res:
            self.url_max -= 1
            if self.url_max:
                if "news.baidu.com" in u:
                    yield response.follow(u,callback=self.parse)
                elif "sohu.com" in u:
                    yield response.follow(u,callback=self.parse_sohu)
                elif "ifeng.com" in u:
                    yield response.follow(u,callback=self.parse_ifeng)

    def parse_sohu(self,response):
        self.log(f'parse sohu : {response.url}')

    def parse_ifeng(self,response):
        self.log(f'parse ifeng : {response.url}')

        
        