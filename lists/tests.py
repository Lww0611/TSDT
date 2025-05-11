from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item
from django.test import TestCase
from .models import Item  # 假设你的模型在当前目录下的 models.py 文件中

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})

        # 检查数据库中是否新增了一条记录
        self.assertEqual(Item.objects.count(), 1)
        # 获取新增的记录
        new_item = Item.objects.first()
        # 检查新增记录的内容是否正确
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        # 检查响应状态码是否为302（重定向）
        self.assertEqual(response.status_code, 302)
        # 检查重定向的URL是否是根URL（'/'）
        self.assertEqual(response['location'], '/lists/the-new-page/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-new-page/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        # 创建两个列表项
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        # 发送 GET 请求到指定的列表页面 URL
        response = self.client.get('/lists/the-new-page/')

        # 检查响应内容中是否包含两个列表项的文本
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
# Create your tests here.
