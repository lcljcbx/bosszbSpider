# -*- coding: utf-8 -*-
import scrapy
from bosszbSpider.items import BosszbspiderItem
import re
import itertools
import MySQLdb



class BosszbSpider(scrapy.Spider):
    name = "bosszb"
    # 利用scrapyd 部署时，如果了修改__init__()方法，需要添加这一句
    custom_settings = None


    def __init__(self,name=None, **kwargs):
        super(BosszbSpider, self).__init__()
        # 得到城市名
        self.citynames = self.get_citynames()
        # 职业类型
        self.job_names = self.get_job_names()
        # 两两组合城市名和职业类型
        self.url_params = [x for x in itertools.product(self.citynames, self.job_names)]
        self.url = 'http://www.zhipin.com/%s-%s/?page=%s'


    def get_citynames(self):
        '''从数据库查询得到城市名'''
        conn = MySQLdb.connect(host='localhost', user='root', passwd='***', charset='utf8', db='db_name')
        cur = conn.cursor()
        sql = 'select cityname from city where id>0 order by id'
        cur.execute(sql)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return [str(x[0].encode('utf-8')) for x in results]


    def get_job_names(self):
        '''从数据库查询得到职业类型'''
        conn = MySQLdb.connect(host='localhost', user='root', passwd='***', charset='utf8', db='db_name')
        cur = conn.cursor()
        sql = 'select job_name from job_category where id > 0'
        cur.execute(sql)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return [str(x[0].encode('utf-8')) for x in results]

    #发送请求
    def start_requests(self):
        for url_param in self.url_params:
            url = self.url%(url_param[1],url_param[0],'1')
            yield scrapy.Request(url=url,
                                 dont_filter=True,
                                 callback=self.parse
                                 )

    #解析列表页
    def parse(self, response):
        items = []
        content_list = response.xpath("//div[@class='job-box']//div[@class='job-list']/ul/li")
        if len(content_list) != 0:
            for each in content_list:
                item = BosszbspiderItem()
                item['post_name'] = each.xpath(".//h3/text()")[0].extract()
                l = each.xpath("./a/@href")[0].extract()
                job_link = "http://www.zhipin.com" + l
                item['url_path'] = job_link
                item['post_salary'] = each.xpath(".//h3/span/text()")[0].extract()
                item['post_city'] = each.xpath("./a/div[@class='job-primary']/div[@class='info-primary']/p/text()")[0].extract()
                item['req_job_exp'] = each.xpath("./a/div[@class='job-primary']/div[@class='info-primary']/p/text()")[1].extract()
                item['req_academic'] = each.xpath("./a/div[@class='job-primary']/div[@class='info-primary']/p/text()")[2].extract()
                item['ent_simple_name'] = each.xpath("./a/div[@class='job-primary']/div[@class='info-company']/div[@class='company-text']/h3[@class='name']/text()")[0].extract()
                item['territory'] = each.xpath("./a/div[@class='job-primary']/div[@class='info-company']/div[@class='company-text']/p/text()")[0].extract()
                # 需要捕获异常
                try:
                    item['stage'] = each.xpath("./a/div[@class='job-primary']/div[@class='info-company']/div[@class='company-text']/p/text()")[1].extract()
                    item['scope'] = each.xpath("./a/div[@class='job-primary']/div[@class='info-company']/div[@class='company-text']/p/text()")[2].extract()
                except:
                    item['stage'] = None
                    item['scope'] = each.xpath("./a/div[@class='job-primary']/div[@class='info-company']/div[@class='company-text']/p/text()")[1].extract()

                items.append(item)

            #职位链接，meta传参
            for item in items:
                yield scrapy.Request(item['url_path'],
                                    meta={'position': item},
                                    callback=self.parse_zhiwei)

            #翻页
            res_url = response.url
            new_url = res_url[:44]
            #生成数字序列，尽量用 xrange 代替 range
            for i in xrange(2,31):
                page_url = new_url + str(i)
                yield scrapy.Request(url=page_url,callback=self.parse)

    #处理职位详情
    def parse_zhiwei(self,response):
        item = response.meta['position']
        try:
            item['post_des'] = response.xpath("//div[@class='text']")[0].extract()
        except:
            item['post_des'] = None

        k = response.xpath("//div[@class='info-company']/h3[@class='name']/a/@href")[0].extract()
        strings = re.search(r'\d+',k).group()
        jieshao_url = "http://www.zhipin.com/gongsi/" + strings + ".html" + "?ka=company-intro"
        item['qiye_url'] = jieshao_url
        try:
            item['company_name'] = response.xpath("//div[@class='job-primary']/div[@class='info-company']/p[1]/text()")[0].extract()
        except:
            item['company_name'] = None
        try:
            item['entp_logo'] = response.xpath("//div[@class='job-primary']/div[@class='info-company']/div[@class='company-logo']/a/img/@src")[0].extract()
        except:
            item['entp_logo'] = None
        try:
            item['post_addr'] = response.xpath("//div[@class='location-address']/text()")[0].extract()
        except:
            item['post_addr'] = None

        yield scrapy.Request(item['qiye_url'],
                             meta={'position': item},
                             callback=self.parse_qiye)

    #处理公司简介
    def parse_qiye(self,response):
        item = response.meta['position']
        try:
            item['entp_url'] = response.xpath("//div[@class='job-primary']/div[@class='info-primary']/p[2]/text()")[0].extract()
        except:
            item['entp_url'] = None

        try:
            item['ent_intro'] = response.xpath("//div[@class='job-sec'][1]/div[@class='text fold-text']/text()")[0].extract()
        except:
            item['ent_intro'] = None

        yield item




