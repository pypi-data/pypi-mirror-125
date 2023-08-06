import os
import time
from unittest import TestCase

from XsCore import XsPool, XsHttp, XsStrings, XsJob


def getHtml(url):
    time.sleep(1)
    rz = XsHttp.getText(url)
    print("获取到内容:", len(rz), "  来自:", url)


class XsPoolTest(TestCase):

    def testPool(self):
        """
        此方法演示了如果简单的向线程池添加任务
        :return:
        """
        #最大允许3个线程并发处理任务
        pool = XsPool(max_task=3)
        htmlc = XsHttp.getText('https://www.cnblogs.com')
        urls = XsStrings.getHtmlUrls(htmlc) #提取页面上的url
        for url in urls:  #批量添加获取页面内容的任务
            pool.addTask(getHtml, url)  #添加一个任务
        print("任务添加完成")
        os.system('pause')  # 不要退出终端

    def testPoolBackInfo(self):
        """
        此方法演示了如何向线程池添加任务，并定时获取任务的情况
        要获取任务的使用情况，需要构造时将is_future=True
        :return:
        """
        #最大允许3个线程并发处理任务
        pool = XsPool(max_task=3,is_future=True, is_process=False)

        htmlc = XsHttp.getText('https://www.cnblogs.com')
        urls = XsStrings.getHtmlUrls(htmlc) #提取页面上的url
        for url in urls:  #批量添加获取页面内容的任务
            pool.addTask(getHtml, url)

        print("任务添加完成")

        # 开启一个定时任务获取线程的使用情况
        job = XsJob()
        job.addTimer_Seconds(1, self.__get_info, [pool])
        job.start()

        # os.system('pause')

    def __get_info(self, pool: XsPool):
        print("正在执行:", pool.getRunningCount())
        print("等待中的任务数:", pool.getWaitingCount())
