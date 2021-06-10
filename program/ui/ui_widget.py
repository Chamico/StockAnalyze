from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.bubble import Bubble
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.base import runTouchApp
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
#from kivy.effects import DampedScrollEffect
import os
import sys
#from kivy.core.window import Window


myfont_path = os.path.join(os.getcwd(),'resource','font','STXIHEI.TTF')

class PublicCheckBtn(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '检查'
        self.size_hint_x = .30
        self.font_name = myfont_path
        self.font_size = 25

class PublicRecomBtn(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '推荐'
        self.size_hint_x = .30
        self.font_name = myfont_path
        self.font_size = 25

class PublicInfoBtn(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '信息'
        self.size_hint_x = .30
        self.font_name = myfont_path
        self.font_size = 25

class PublicOtherBtn(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '┇'
        self.size_hint_x = .1
        self.font_name = myfont_path
        self.font_size = 25

class PublicHeadLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 50

class PublicScrollViewItem(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.content = args
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60

        label_name = BoxLayout()
        label_name.orientation = 'vertical'
        label_name.size_hint_x = .4
        label_name.add_widget(Label(text=self.content[0],font_name = myfont_path))
        label_name.add_widget(Label(text=self.content[1],font_name = myfont_path))

        label_price = Label(text = self.content[2],font_name = myfont_path)
        label_price.size_hint_x = .3

        label_ratio = BoxLayout()
        label_ratio.orientation = 'vertical'
        label_ratio.size_hint_x = .3
        label_ratio.add_widget(Label(text=self.content[3],font_name = myfont_path))
        label_ratio.add_widget(Label(text=self.content[4],font_name = myfont_path))

        self.add_widget(label_name)
        self.add_widget(label_price)
        self.add_widget(label_ratio)

class PublicScrollViewLayout(ScrollView):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        #self.size_hint=(None, None)
        self.size=(500, 320)
        #self.pos_hint={'center_x': .5, 'center_y': .5}
        self.do_scroll_x=False

class PublicScrollViewRootLayout(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 15000
        self.item_list = []

    def add_item(self, *args):
        item = PublicScrollViewItem(*args)
        self.add_widget(item)
        self.item_list.append(item)

    def remove_all_items(self):

        for index in self.item_list:
            self.remove_widget(index)
            self.item_list.remove(index)
            
class PublicScreenRootLayout(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = 1



class PublicScreen(Screen):
    pass

class CheckFilterLayout(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 30

class BtnOtherBack(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50
        self.font_name = myfont_path
        self.text = '返回'

class BtnOtherRefresh(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50
        self.font_name = myfont_path
        self.text = '刷新'


class OtherScreenRootLayout(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'



# 实例化对象
# check screen
btn_check_check = PublicCheckBtn()
btn_check_recom = PublicRecomBtn()
btn_check_info = PublicInfoBtn()
btn_check_other = PublicOtherBtn()
check_head = PublicHeadLayout()
label_filter = Label(text = '筛选',font_name = myfont_path)
input_min_value = TextInput(text = '0')
label_minus = Label(text = '-')
input_max_value = TextInput(text = '0')
btn_check_filter_ok = Button(text = '确定',font_name = myfont_path)
check_filter = CheckFilterLayout()
check_scroll_root = PublicScrollViewRootLayout()
check_scroll = PublicScrollViewLayout()
check_root = PublicScreenRootLayout()
check_screen = PublicScreen(name = 'check')


# recom screen
btn_recom_check = PublicCheckBtn()
btn_recom_recom = PublicRecomBtn()
btn_recom_info = PublicInfoBtn()
btn_recom_other = PublicOtherBtn()
recom_head = PublicHeadLayout()
recom_scroll_root = PublicScrollViewRootLayout()
recom_scroll = PublicScrollViewLayout()
recom_root = PublicScreenRootLayout()
recom_screen = PublicScreen(name = 'recom')

# info screen
btn_info_check = PublicCheckBtn()
btn_info_recom = PublicRecomBtn()
btn_info_info = PublicInfoBtn()
btn_info_other = PublicOtherBtn()
info_head = PublicHeadLayout()
info_scroll_root = PublicScrollViewRootLayout()
info_scroll = PublicScrollViewLayout()
info_root = PublicScreenRootLayout()
info_screen = PublicScreen(name = 'info')


#other screen
btn_other_back = BtnOtherBack()
btn_other_refresh = BtnOtherRefresh()
input_interval_day = TextInput(text = '0')
other_root = OtherScreenRootLayout()
other_screen = PublicScreen(name = 'other')