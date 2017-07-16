# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from settings import USER_AGENT_LIST
import random
import requests
import re


# User-Agent 下载中间件
class RandomUserAgent(object):
    def process_request(self, request, spider):
        # 这句话用于随机选择user-agent
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers.setdefault('User-Agent', user_agent)


#添加代理
class RandomProxy(object):
    def __init__(self):
        #计数
        self.num = 0
        # 代理api接口
        self.proxy_api = "http://proxy_api"
        self.rule = re.compile(r"(?m)\b(\d+\.\d+\.\d+\.\d+\:\d+)\b")
        # 发送代理api请求，获取代理列表
        self.proxy_list = self.rule.findall(requests.get(self.proxy_api).text)
        print self.proxy_list

    def process_request(self, request, spider):
        if self.num > 10:
            self.proxy_list = self.rule.findall(requests.get(self.proxy_api).text)
            self.num = 0
        proxy = random.choice(self.proxy_list)
        request.meta['proxy'] = "http://%s" %proxy
        self.num += 1
        print "http://%s" %proxy

    def process_proxy(self):
        print "*" * 30
        return self.rule.findall(requests.get(self.proxy_api).text)


