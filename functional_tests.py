from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do', header_text)
        #应用有一个输入待办事项文本输入框
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(inputbox.get_attribute('placehoder'),
                         'Enter a to-do item')

        # 输入任务并提交
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)  # 等待页面更新

        # 验证任务是否显示在列表中
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1: Buy flowers', [row.text for row in rows])

        # 测试未完成标记
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()