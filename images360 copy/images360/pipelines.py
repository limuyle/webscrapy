# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class MysqlPipeline():
    def __init__(self,host,database,user,password,port):
        self.host=host
        self.database=database
        self.user=user
        self.password=password
        self.port=port
        
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )
    
    def open_spider(self,spider):
        self.db=pymysql.connect(host=self.host,user=self.user,password=self.password,
                                database=self.database,port=self.port)
        self.cursor=self.db.cursor()
        
        
    def close_spider(self,spider):
        self.db.close()
        
    def process_item(self,item,spider):
        print(item['title'])
        data=dict(item)
        keys=','.join(data.keys())
        values=','.join(['%s']*len(data))
        sql='insert into %s (%s) values(%s)'%(item.table,keys,values)
        self.cursor.execute(sql,tuple(data.values()))
        self.db.close()
        return item
        
        

        
        
        
# ImagePipeline 默认读取image_urls字段，遍历每个url并下载，这里的Item url不是列表，需重写相关方法
class ImagePipeline(ImagesPipeline):
    def file_path(self,request,response=None,info=None):
        url=request.url
        file_name=url.split('/')[-1]
        return file_name
    
    def item_completed(self,results,item,info):
        image_paths=[x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item
    # item为爬取生成的Item对象，把图片url取出执行下载
    def get_media_requests(self,item,info):
        yield Request(item['url'])
            
    
