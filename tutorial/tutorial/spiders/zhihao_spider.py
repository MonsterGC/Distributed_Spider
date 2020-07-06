import scrapy
import re
import time
from tutorial.items import TutorialItem
from scrapy_redis.spiders import RedisCrawlSpider

import sys
class ZhihaoSpider(RedisCrawlSpider):

    name = "zw"
    redis_key = "myspider:start_urls"

    allowed_domains = ["51job.com"]
    # 填写爬取地址
    # start_urls = [
    #     "https://search.51job.com/list/000000,000000,0000,32,9,99,%2B,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=",
    # ]
    # 解析二级子页面
    def parse_detail(self, response):
        title = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/@title').extract_first()
        money = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()').extract_first()  # 万
        company = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/text()').extract_first()
        address = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/@title').extract_first().replace('\xa0','').split('|')[0]
        experience = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/@title').extract_first().replace('\xa0','').split('|')[1]
        requirement = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/@title').extract_first().replace('\xa0','').split('|')[2]
        detail = str(response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div').extract())
        detail = re.sub(r'\\r\\n|,|；|\'|\[|\]|[a-z|A-Z]|<.*?>|<//.*?>','', detail).strip()
        goods  = '、'.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span/text()').extract())
        
        # 取出meta的item
        item = response.meta['item']
        item['title'] = title
        item['money'] = money
        item['company'] = company
        item['experience'] = experience
        item['requirement'] = requirement
        item['detail'] = detail
        item['goods'] = goods
        yield item

    # 编写爬取方法
    def parse(self, response):
        for url in response.xpath('//*[@id="resultList"]/div[re:test(@class,"el")]/p/span/a/@href').extract():
                # 实例化item对象并存储
                item = TutorialItem()
                item['url'] = url
                # meta 传递第二次解析函数
                yield scrapy.Request(url=url, callback=self.parse_detail, meta={'item': item})
        next_page = response.xpath('//*[@id="resultList"]/div[55]/div/div/div/ul/li[8]/a/@href').extract()[0]
        print('=============================:',next_page)
        if next_page:
            # time.sleep(1)
            yield scrapy.Request(url=next_page, callback=self.parse)
