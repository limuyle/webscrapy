# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logging import getLogger
from scrapy.http import HtmlResponse


class SeleniumMiddleware():
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self,timeout=None):
        self.logger=getLogger(__name__)
        self.timeout=timeout
        self.browser=webdriver.Chrome()
        self.browser.set_window_size(1400,700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait=WebDriverWait(self.browser,self.timeout)
        
    def __del__(self):
        self.browser.close()
        
    def process_request(self,request,spider):
        self.logger.debug('scrapy is Starting')
        page=request.meta.get('page',1)
        try:
            self.browser.get(request.url)
            if page>1:
#                 input=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager\
#           div.form>input')))
#                 submit=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager div.form>span.btn.J_Submit')))
#                 input.clear()
#                 input.send_keys(page)
#                 submit.click()
                input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
                submit = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
                input.clear()
                input.send_keys(page)
                submit.click()
#             self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active>span'),str(page)))
#             self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
#             return HtmlResponse(url=request.url,body=self.browser.page_source,request=request,encoding='utf-8',status=200)
#         except TimeoutException:
#             return HtmlResponse(url=request.url,status=500,request=request)
            self.wait.until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)
        
        
            

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))





