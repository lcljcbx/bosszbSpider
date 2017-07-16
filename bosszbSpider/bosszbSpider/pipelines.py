# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from scrapy.conf import settings
#import json
import MySQLdb
from datetime import datetime

#写入本地文件
# class BosszbspiderPipeline(object):
#     def __init__(self):
#         self.filename = open("zhipin.json","a")
#     def process_item(self, item, spider):
#         content = json.dumps(dict(item),ensure_ascii=False) + ", \n"
#         self.filename.write(content)
#         return item
#     def close_spider(self,spider):
#         self.filename.close()


#写入MySQL数据库
class MySQLPipline(object):
    def process_item(self, item, spider):
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWD']
        db = settings['MYSQL_DBNAME']
        c = settings['CHARSET']

        item['publish_time'] = datetime.utcnow()
        item['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        con = MySQLdb.connect(host=host, user=user, passwd=psd, db=db, charset=c)
        cur = con.cursor()
        sql = ("insert into table_name(ID,res_flag,url_path,url_isgather,url_ispublish,company_name,ent_simple_name,territory,stage,scope,entp_logo,post_name,post_salary,post_city,req_job_exp,req_academic,post_des,publish_time,create_time,entp_url,post_addr,ent_intro) values(0,0,%s,1,0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        list = [item['url_path'],item['company_name'],item['ent_simple_name'],item['territory'],item['stage'],item['scope'],item['entp_logo'],item['post_name'],item['post_salary'],item['post_city'],item['req_job_exp'],item['req_academic'],item['post_des'],item['publish_time'],item['create_time'],item['entp_url'],item['post_addr'],item['ent_intro']]
        try:
            cur.execute(sql, list)
            con.commit()
        except Exception, e:
            print('Insert error', e)
            con.rollback()
        finally:
            cur.close()
            con.close()
        return item
