from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class  NewVisitorTest(FunctionalTest):
        
    def test_can_start_a_list_and_retrieve_it_later(self):

        #访问应用的首页
        #self.browser.get("http://127.0.0.1:8000")
        self.browser.get(self.live_server_url)

        #网页的标题和头部含有“To-Do”这个词
        self.assertIn('To-Do',self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)

        #应用邀请她输入一个代办事项
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        #她在一个文本框中输入了“Buy peacock feathers”
        #她的爱好是使用假绳做诱饵钓鱼
        inputbox.send_keys("Buy peacock feathers")

        #她按回车后，被带到了一个新的URL
        #这个页面的代办事项表格中显示了“1：Buy peacock feathers”

        inputbox.send_keys(Keys.ENTER) 
        edith_list_url = self.browser.current_url 
        self.assertRegex(edith_list_url, '/lists/.+') 
        self.check_for_row_in_list_table('1: Buy peacock feathers') 


        #页面中又显示了一个文本框，可以输入其他的代办事项
        #她输入了“Use peacock feathers to make a fly”

        inputbox = self.get_item_input_box()
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
    
        #页面再次跟新，她的清单中显示了这两个代办事项
        self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        

        #现在弗朗西斯的心用户访问了网站
        ##我们使用一个新的浏览器会话
        ##确保伊迪斯的信息不会从cookie中泄露出来
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #弗朗西斯访问首页
        #页面中看不到伊迪斯的清单

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        #弗朗西斯输入一个新待办事项，新建一个清单
        #他不像伊迪斯那样兴趣盎然

        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        #弗朗西斯获得了他的唯一一个URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #这个页面还是么有伊迪斯的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

