# -*- coding: utf-8 -*-  
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
#from kivy.core.window import Window
from ui.ui_widget import *
from ui.ui_interface import *
import string
import pandas as pd
import os
from analyze.crawler import get_interval_stock_info



#from kivy.app import runTouchApp
# define ScreenManager
sm = ScreenManager()

result_path = os.path.join(os.getcwd(),'program','message', 'result.csv')

def show_check_screen(instance):
    sm.switch_to(check_screen)

def show_recom_screen(instance):
    sm.switch_to(recom_screen)

def show_info_screen(instance):
    sm.switch_to(info_screen)

def show_other_screen(instance):
    sm.switch_to(other_screen)

def refresh_filter_value(instance):
    #清除之前的所有列表
    check_scroll_root.remove_all_items()
    # 获取最大值和最小值，并保存为浮点型
    min_value = float(input_min_value.text)
    max_value = float(input_max_value.text)

    print(min_value, type(min_value))

    result_path = os.path.join(os.getcwd(),'program','message', 'result.csv')
    # 打开 result 文件
    csv_data = pd.read_csv(result_path,dtype = object)
    df = pd.DataFrame(csv_data)    # csv 转换为 DataFrame
    # 获取总的行数
    row_num = df.shape[0]
    # 遍历，获取需要的值

    df.set_index('stock_number', inplace=True)

    for index in df.index:
        
        # 获取当前值
        value = float(df.at[index,'cur_value'])
        stock_name = df.at[index,'stock_name']
        last_down_count = int(df.at[index,'last_down_count'])
        # 选取合适的值，添加到界面中
        if (value <= max_value) and (value >= min_value) and (last_down_count > 3):
            add_item_to_check(stock_name, index, str(value),'00','00')

    '''print(df.columns)
    for index in range(row_num):
        # 获取当前值
        value = df.at[index,'cur_value']
        stock_number = df.at[index,'stock_number']
        
        # 选取合适的值，添加到界面中
        if (value <= max_value) and (value >= min_value):
            add_item_to_check('陈天海',stock_number,str(value),'00','00')
        #print(type(value))'''

def go_to_previous_screen(instance):
    #sm.current = sm.previous()
    #sm.switch_to()
    #print('back to previous screen')
    #print(my_curren_screen)
    show_check_screen(None)

def refresh_data(instance):
    interval_day = int(input_interval_day.text)
    get_interval_stock_info(interval_day)

def check_bind():
    btn_check_check.bind(on_release = show_check_screen)
    btn_check_recom.bind(on_release = show_recom_screen)
    btn_check_info.bind(on_release = show_info_screen)
    btn_check_other.bind(on_release = show_other_screen)
    btn_check_filter_ok.bind(on_release = refresh_filter_value)
    check_scroll_root.bind(minimum_height=check_scroll_root.setter('height'))

def recom_bind():
    btn_recom_check.bind(on_release = show_check_screen)
    btn_recom_recom.bind(on_release = show_recom_screen)
    btn_recom_info.bind(on_release = show_info_screen)
    btn_recom_other.bind(on_release = show_other_screen)
    recom_scroll_root.bind(minimum_height=recom_scroll_root.setter('height'))

def info_bind():
    btn_info_check.bind(on_release = show_check_screen)
    btn_info_recom.bind(on_release = show_recom_screen)
    btn_info_info.bind(on_release = show_info_screen)
    btn_info_other.bind(on_release = show_other_screen)

def other_bind():
    btn_other_back.bind(on_release = go_to_previous_screen)
    btn_other_refresh.bind(on_release = refresh_data)

def check_add_widget():
    check_head.add_widget(btn_check_check)
    check_head.add_widget(btn_check_recom)
    check_head.add_widget(btn_check_info)
    check_head.add_widget(btn_check_other)
    check_filter.add_widget(label_filter)
    check_filter.add_widget(input_min_value)
    check_filter.add_widget(label_minus)
    check_filter.add_widget(input_max_value)
    check_filter.add_widget(btn_check_filter_ok)
    check_scroll.add_widget(check_scroll_root)
    check_root.add_widget(check_head)
    check_root.add_widget(check_filter)
    check_root.add_widget(check_scroll)
    check_screen.add_widget(check_root)

def recom_add_widget():
    recom_head.add_widget(btn_recom_check)
    recom_head.add_widget(btn_recom_recom)
    recom_head.add_widget(btn_recom_info)
    recom_head.add_widget(btn_recom_other)
    recom_scroll.add_widget(recom_scroll_root)
    recom_root.add_widget(recom_head)
    recom_root.add_widget(recom_scroll)
    recom_screen.add_widget(recom_root)

def info_add_widget():
    info_head.add_widget(btn_info_check)
    info_head.add_widget(btn_info_recom)
    info_head.add_widget(btn_info_info)
    info_head.add_widget(btn_info_other)
    info_scroll.add_widget(info_scroll_root)
    info_root.add_widget(info_head)
    info_root.add_widget(info_scroll)
    info_screen.add_widget(info_root)

def other_add_widget():
    other_root.add_widget(btn_other_back)
    other_root.add_widget(input_interval_day)
    other_root.add_widget(btn_other_refresh)
    other_screen.add_widget(other_root)



def event_bind():
    check_bind()
    recom_bind()
    info_bind()
    other_bind()

def screen_add_widget():
    check_add_widget()
    recom_add_widget()
    info_add_widget()
    other_add_widget()

def ui_widget_process():
    event_bind()
    screen_add_widget()

class MainApp(App):
    def build(self):
        sm.transition = NoTransition()
        sm.add_widget(check_screen)
        sm.add_widget(recom_screen)
        sm.add_widget(info_screen)

        ui_widget_process()
        add_item_to_check('查看', '002518', '12','13','14')
        add_item_to_recom('推荐', '002518', '12','13','14')
        sm.switch_to(check_screen)
        return sm
        
def ui_process():
    MainApp().run()










