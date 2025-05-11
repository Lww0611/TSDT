from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from .models import Item, List  # 假设你的模型在当前目录下的 models.py 文件中

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List.objects.create()  # 新增此行

        # 创建 Item 并关联到 List
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.list = list_  # 关键：设置关联
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_  # 关联到同一个 List
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


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-new-page/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        list_user=List.objects.create()
        # 创建两个列表项
        Item.objects.create(text='itemey 1',list=list_user)
        Item.objects.create(text='itemey 2',list=list_user)

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-new-page/')