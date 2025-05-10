from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
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
        # 测试未完成标记
        self.fail('Finish the test!')
