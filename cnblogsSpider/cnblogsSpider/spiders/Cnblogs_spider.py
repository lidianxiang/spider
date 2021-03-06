#coding:utf-8
import scrapy
from scrapy import Selector
from cnblogsSpider.items import CnblogsspiderItem

class CnblogsSpider(scrapy.Spider):
    name = "cnblogs" ##爬虫的名称
    allowed_domains = ["cnblogs.com"]##允许的域名
    start_urls = ["http://www.cnblogs.com/qiyeboy/default.html?page=1"]

    def parse(self, response):
        ##实现网页的解析
        #首先抽取所有的文章
        papers = response.xpath('.//*[@class="day"]')
        #从每篇文章中抽取数据
        from scrapy.shell import inspect_response
        inspect_response(response,self)

        for paper in papers:
            url = paper.xpath(".//*[@class='postTitle']/a/@href").extract()[0]
            title = paper.xpath(".//*[@class='postTitle']/a/text()").extract()[0]
            time = paper.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            content = paper.xpath(".//*[@class='postCon']/div/text()").extract()[0]
            item = CnblogsspiderItem(url=url, title=title, time=time, content=content)
            request = scrapy.Request(url=url, callback=self.parse_body)
            request.meta['item'] = item  # 将item暂存
            yield request
        next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>')
        if next_page:
            yield scrapy.Request(url=next_page[0], callback=self.parse)


    # def parse_body(self,response):
    #     item = response.meta['item']
    #     body = response.xpath(".//*[class='postBody']")
    #     item['cimage_url'] = body.xpath('.//img//@src').extract()
    #     yield item

    def parse_body(self, response):
        item = response.meta['item']
        body = response.xpath(".//*[@class='postBody']")
        item['cimage_urls'] = body.xpath('.//img//@src').extract()  # 提取图片链接
        yield item
