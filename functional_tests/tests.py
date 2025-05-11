from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()  # 记录开始时间
        while True:  # 创建一个无限循环
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')  # 找到列表表格元素
                rows = table.find_elements(By.TAG_NAME, 'tr')  # 找到所有行元素
                self.assertIn(row_text, [row.text for row in rows])  # 检查目标文本是否在行文本中
                return  # 如果找到，退出函数
            except (AssertionError, WebDriverException) as e:  # 捕获异常
                if time.time() - start_time > MAX_WAIT:  # 检查是否超过最大等待时间
                    raise e  # 如果超过，抛出异常
                time.sleep(0.5)  # 如果未超过，等待0.5秒后重试

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do', header_text)
        #应用有一个输入待办事项文本输入框
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        # 输入任务并提交
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flowers')

        # 页面中又显示了一个文本输入框，可以输入其他待办事项
        # 他输入了"Give a gift to Lisi"
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy flowers')
        self.wait_for_row_in_list_table('2: Give a gift to Lisi')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 张三新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flowers')

        # 他注意到清单有个唯一的URL
        zhangsan_list_url = self.browser.current_url
        self.assertRegex(zhangsan_list_url, r'/lists/.+')

        # 现在一个新用户王五访问网站
        # 我们使用一个新浏览器会话
        # 确保张三的信息不会从Cookie中泄露出去
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # 王五访问首页
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy flowers', page_text)
        self.assertNotIn('Give a gift to Lisi', page_text)

        # 王五输入一个新待办事项，新建一个清单
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # 王五获得了他的唯一URL
        wangwu_list_url = self.browser.current_url
        self.assertRegex(wangwu_list_url, r'/lists/.+')
        self.assertNotEqual(wangwu_list_url, zhangsan_list_url)

        # 这个页面还是没有张三的清单
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy flowers', page_text)
        self.assertIn('Buy milk', page_text)

        # 两人都很满意，然后去睡觉了

    def test_layout_and_styling(self):
        # 张三访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 她看到输入框完美地居中显示
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )