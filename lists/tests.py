from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from .models import Item, List  # 假设你的模型在当前目录下的 models.py 文件中

class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

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
        list_user = List.objects.create()  # 创建一个列表用户
        response = self.client.get(f'/lists/{list_user.id}/')
        self.assertTemplateUsed(response, 'list.html')  # 检查是否使用了正确的模板

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()  # 创建一个正确的列表
        Item.objects.create(text='itemey 1', list=correct_list)  # 创建一个属于正确列表的项目
        Item.objects.create(text='itemey 2', list=correct_list)  # 创建另一个属于正确列表的项目
        other_list = List.objects.create()  # 创建另一个列表
        Item.objects.create(text='other list item 1', list=other_list)  # 创建一个属于另一个列表的项目
        Item.objects.create(text='other list item 2', list=other_list)  # 创建另一个属于另一个列表的项目

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')  # 检查是否包含正确列表的项目
        self.assertContains(response, 'itemey 2')  # 检查是否包含正确列表的项目
        self.assertNotContains(response, 'other list item 1')  # 检查是否不包含另一个列表的项目
        self.assertNotContains(response, 'other list item 2')  # 检查是否不包含另一个列表的项目

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()  # 创建一个列表对象，用于测试
        correct_list = List.objects.create()  # 创建另一个列表对象，这是正确的列表

        response = self.client.get(f'/lists/{correct_list.id}/')  # 发送 GET 请求到正确的列表的 URL

        # 断言响应上下文中的 'list' 变量等于我们创建的正确列表对象
        self.assertEqual(response.context['list'], correct_list)

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list=List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')