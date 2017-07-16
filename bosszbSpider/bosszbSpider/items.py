# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BosszbspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 招聘职位
    post_name = scrapy.Field()
    # 职位详情页url
    url_path = scrapy.Field()
    # 职位月薪
    post_salary = scrapy.Field()
    # 工作城市
    post_city = scrapy.Field()
    # 经验要求
    req_job_exp = scrapy.Field()
    # 学历要求
    req_academic = scrapy.Field()
    # 发布时间
    publish_time = scrapy.Field()


    # 企业简称
    ent_simple_name = scrapy.Field()
    # 所属行业
    territory = scrapy.Field()
    # 企业阶段
    stage = scrapy.Field()
    # 企业规模
    scope = scrapy.Field()



    # 企业名称
    company_name = scrapy.Field()
    # 企业LOGO
    entp_logo = scrapy.Field()
    # 企业介绍页url
    qiye_url = scrapy.Field()
    # 职位描述
    post_des = scrapy.Field()
    # 工作地址
    post_addr = scrapy.Field()


    # 企业网址
    entp_url = scrapy.Field()
    # 企业介绍
    ent_intro = scrapy.Field()


    #抓取时间
    create_time = scrapy.Field()


