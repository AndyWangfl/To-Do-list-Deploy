from .base import FunctionalTest
from unittest import skip



class ItemValidationTest(FunctionalTest):
    
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        #伊迪斯访问首页，不小心提交了一个空代办事项
        #输入框内没有输入内容就按下了回车键
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        #首页刷新了，显示一个错误信息
        #提示代办事项不能为空
        error = self.get_error_element()
        self.assertEqual(error.text,"You can't have an empty list item")

        #她输入了一些文字，然后再次提交，这次没有问题了
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        #她又提交了一个空代办事项
        self.get_item_input_box().send_keys('\n')

        
        #在清单页面看到了一个类似的错误信息
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.get_error_element()
        self.assertEqual(error.text,"You can't have an empty list item")
        
        #输入文字之后就没有问题了
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        #伊迪斯访问首页，新建一个清单
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')

        #她一不小心输入了一个重复的代办事项
        self.get_item_input_box().send_keys('Buy wellies\n')
        
        #她看到一条有帮助的错误消息
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def test_error_messages_are_cleared_on_input(self):
        # 伊迪丝新建一个清单，但方法不当，所以出现了一个验证错误
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        #为了消除错误，她开始在输入框中输入内容
        self.get_item_input_box().send_keys('a')

        #看到错误消息消失了，她很高兴
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())


        

