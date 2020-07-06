# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # 抓取内容：
    # 岗位：辅导老师-高一英语
    # 工资：0.6-1万/月
    # 公司：网易集团 
    # 位置：太原
    # 经验：3-4年
    # 性质：在校生/应届生
    # 要求：本科
    # 职位信息：...
    # 效益：五险一金扁平管理弹性工作晋升空间大团队氛围好
    # 链接：xxx
    title = scrapy.Field()
    money = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    experience = scrapy.Field()
    requirement = scrapy.Field()
    detail = scrapy.Field()
    goods  = scrapy.Field()
    url = scrapy.Field()