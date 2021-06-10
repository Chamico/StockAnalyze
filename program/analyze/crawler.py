#获取数据并以json文件的格式保存到本地
from urllib.request import urlopen,Request
import json
from bs4 import BeautifulSoup
import chardet
import os
import sys
import datetime,time
import re
from pandas_datareader import data, wb
import pandas as pd
import requests
import random
from multiprocessing import Pool

#os.path.abspath('./Data')   # 表示当前所处的文件夹的绝对路径
#os.path.abspath('..')  # 表示当前所处的文件夹上一级文件夹的绝对路径
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}


stock_info_file_path = os.path.join(os.getcwd(),'program','analyze','data', 'stock_info')
avaliable_file_path = os.path.join(os.getcwd(),'program','analyze','data', 'avaliable_stock')

'''
@ desc: 将datetime格式的内容转换成date格式的内容
@ para: cur_datetime (datatime 格式的内容)
@ return: cur_date (date 格式的内容)
'''
def datetime_to_date(cur_datetime):
    # 转换为 str 格式
    cur_datetime = str(cur_datetime)
    # 切片，获取有效内容
    cur_datetime = cur_datetime[:cur_datetime.find(' ')]
    # 转换为 date 格式
    cur_date = datetime.datetime.strptime(str(cur_datetime),'%Y-%m-%d').date()
    # 返回
    return cur_date

'''
@ desc: 对文件路径进行连接
@ para: base(之前的路径)
        current(当前的子路径)
@ return: None
'''
def path_connect(base, current):
    return os.path.join(base, str(current))

'''
@ desc: 判断股票的后缀，既在哪个交易所
        股票前两位：00为深圳交易所上市股票，30为创业板股票（深圳）
        60为上海交易所上市股票，68为科创板股票（上海）
@ para: base(之前的路径)
        current(当前的子路径)
@ return:   SZ(深圳交易所)
            SS(上海交易所)
'''
def get_exchange_tail(number):
    head = number[:2]
    if((head == '00') or (head == '30')):
        tail = '.SZ'
    elif((head == '60') or (head == '68')):
        tail = '.SS'
    return tail

'''
@ desc: 获取深圳交易所的当前上市公司名单，最终保存在 avaliable_stock 文件夹下的 sz.txt 中。剔除 *ST 和 ST 股票。
@ para: None
@ return: None
'''
def get_sz_avaliable():
    # 从网页上下载深圳交易所的所有可用股票 .xlsx文件 
    download_url = 'http://www.szse.cn/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=1110&TABKEY=tab1&random=0.41403321665554205'
    save_path = path_connect(avaliable_file_path, 'sz.xlsx')
    r = requests.get(download_url)
    with open(save_path, "wb") as code:
        code.write(r.content)
    
    # 打开 excel 文件
    # 获取股票代码
    number = pd.read_excel(save_path, sheet_name='A股列表',dtype = {'A股代码' : str}, usecols=[4])  # DataFrame 类型
    number = number['A股代码']  # Series 类型
    # 获取股票名称
    name = pd.read_excel(save_path, sheet_name='A股列表', usecols=[5])
    name = name['A股简称']

    # 创建空股票名称列表
    list_name = []
    # 创建空股票代码列表
    list_number = []
    # 创建股票代码：名称字典
    dict_stock = {}

    # 给上述两个列表中添加元素
    for key in name.keys():
        list_name.append(name[key])
    for key in number.keys():
        list_number.append(number[key])

    # 给字典赋值
    
    for i in range(len(list_name)): # list_name 和 list_number 的长度一样
        temp_name = list_name[i]
        if('*ST' == temp_name[0: 3]):
            pass
        elif('ST' ==temp_name[0: 2]):
            pass
        else:
            stock_type = str(list_number[i])[:2]
            if('30' == stock_type): #去掉创业板股票
                pass
            else:
                dict_stock.update({str(list_number[i]) : list_name[i]})
    
    # 保存字典到本地
    dict_tittle_sz_path = path_connect(avaliable_file_path, 'sz.txt')
    file = open(dict_tittle_sz_path,'w',encoding='utf-8')
    file.write(str(dict_stock))
    file.close();

'''
@ desc: 获取上海交易所的当前上市公司名单，最终保存在 avaliable_stock 文件夹下的 sh.txt 中。剔除 *ST 和 ST 股票。
@ para: None
@ return: None
'''
def get_sh_avaliable():
    url_path = 'http://www.sse.com.cn/market/sseindex/indexlist/s/i000002/const_list.shtml'
    req = Request(url=url_path, headers=headers) 
    html = urlopen(req).read()
    soup = BeautifulSoup(html)
    # 通过类的名称查找
    content = soup.select('.tablestyle')   
    # 转换为 字符串
    content = str(content)
    
    #删除多余的内容
    content = content.replace(' ','')
    content = content.replace('=','')
    content = content.replace('"','')
    content = content.replace('\n','')
    content = content.replace('\r','')
    content = content.replace('\t','')
    content = content.replace('</a>','')
    content = content.replace('</td>','')
    content = content.replace('</tr>','')
    content = content.replace('<tdclasstable3>','')
    content = content.replace('<trbgcolor#dbedf8>','')
    content = content.replace('<ahref/assortment/stock/list/stockdetails/company/index.shtml?COMPANY_CODE','')
    content = content.replace('&amp;PRODUCTID','')
    content = content.replace('target_blank>','')
    content = content.replace('<tdbgcolorwhiteclasstable3>','')
    content = content.replace('</table>]','')
    content = content.replace('[<tableclasstablestyle>','')
    content = content.replace('<trbgcolorwhite>','')
    content = content.replace('\xa0','')    # 如果股票名称只有三个汉字的时候，可能会一个这个字符作为填充，在此提前删除
    # 定义字典保存数据
    dict_stock = {}
    
     # 对信息进行遍历，获取有效的股票名称和代码
    while(0 != len(content)):
        # re.findall 方法能够以列表的形式返回全部匹配的字符串.
        # r标识代表后面是正则的语句
        # “d”是正则语法规则用来匹配0到9之间的数
        # +表示匹配多个连续的数字。
        d = re.findall(r'\d+',content)
        useless = str(d[0])
        # 删除无用的股票代码数字串
        content = content.replace(str(useless), '', 1)
        # 找到股票名称的位置索引
        left_brace_index = content.find('(')
        right_brace_index = content.find(')')
        # 获取股票名称
        name = content[0 : left_brace_index]
        number = content[left_brace_index + 1 : right_brace_index]
        # 删除这支股票信息
        content = content.replace(str(name)+ '(' + str(number) + ')', '', 1)

        # 将有效的股票名称和代码存入字典中
        if('*ST' == name[0: 3]):
            pass
        elif('ST' == name[0: 2]):
            pass
        else:
            stock_type = str(number)[:2]
            if('68' == stock_type): # 去掉科创板股票
                pass
            else:
                dict_stock.update({str(number) : name})

        #if(number == '688598'):
        #    print(content)

    # 保存字典到本地
    dict_tittle_sh_path = path_connect(avaliable_file_path, 'sh.txt')
    file = open(dict_tittle_sh_path,'w',encoding='utf-8')
    file.write(str(dict_stock))
    file.close()

def get_interval_stock_info(interval_day):
    interval_day = 10
    print('good interval', interval_day)

'''
@ desc: 获取A股当前所有上市公司名单，最终保存在 avaliable_stock 文件夹下。上海交易所(sh.txt)，深圳交易所(sz.txt)。
    该文件夹下的其他文件为此函数的临时文件。剔除 *ST 和 ST 股票。
@ para: None
@ return: None
'''
def get_avaliable_stock():
    get_sz_avaliable()
    get_sh_avaliable()

'''
@ desc: 根据可用的A股上市公司列表，在 stock_info 文件夹下对每支股票的有效性进行判断。删除已经退市的股票信息，
    新增新上市的股票信息。此函数执行后，保证 stock_info 文件下的每支股票都是有效的。
@ para: None
@ return: None
'''
def update_info_folder():
    avaliable_sz_path = path_connect(avaliable_file_path,'sz.txt')
    avaliable_sh_path = path_connect(avaliable_file_path, 'sh.txt')
    # 从本地文件中读取可用列表并转换为字典
    sz = eval(open(avaliable_sz_path,'r',encoding='utf-8').read())
    sh = eval(open(avaliable_sh_path,'r',encoding='utf-8').read())
    # 合并两个可用的字典，将合并的结果保存到 dict_ava 中
    sz.update(sh.copy())
    dict_ava = sz.copy()
    # 提取 dict_ava 中的股票代码，保存到 list_ava 中
    list_ava = []
    for key in dict_ava.keys():
        list_ava.append(key)
    # 获取本地已有的 csv 列表，保存在 list_local 中
    list_local = []
    info_dir = os.listdir(stock_info_file_path)
    for stock_file in info_dir:
        number = stock_file[0:stock_file.find('.')]     #获取股票代码
        list_local.append(number)
    
    # 将可用的股票和已有的股票列表做差集，获取需要新建和删除的文件列表
    add = list(set(list_ava).difference(set(list_local)))
    delete = list(set(list_local).difference(set(list_ava)))

    # 创建之前没有的股票文件并保存到本地
    
    if(len(add) != 0):
        end = datetime.datetime.now()
        tail = get_exchange_tail(add[0])
        start = (end - datetime.timedelta(days = 30))
        df = data.DataReader(str(add[0]) + tail, 'yahoo', start, end)
        df.drop(df.index, inplace=True)
        for index in add:
            file_path = path_connect(stock_info_file_path,index + '.csv')
            target = df
            target.to_csv(file_path, index = True)   # 保存到本地
    
    # 从本地删除已退市的股票
    if(len(delete) != 0):
        for delete_index in delete:
            file_path = path_connect(stock_info_file_path, delete_index + '.csv')
            os.remove(file_path)

'''
@ desc: 删除股票之前 interval 天的数据
        找得到相等的日期，就删除该日期之后的数据并返回，
        找不到，则输出信息（待补充），再返回，这样意味着数据会有部分丢失
@ para: interval(前 interval 天的天数)
        file：股票对象
@ return: stock：被清除之后的股票，可以直接和新的股票信息连接
'''   
def clear_stock_data(file, interval):
    # 处理时间
    end = datetime.datetime.now()
    # interval + 1：保证删除 delete_time 那一天的股票
    delete_time = (end - datetime.timedelta(days = interval)).date()
    # 将 DataFrame 的 index 转换为 list
    date_list = file.index.tolist()
    file.index.name = 'Date'
    
    if(len(date_list) != 0):
        # 将 string 格式的日期转为 date 格式
        local_min_date = datetime.datetime.strptime(date_list[0],'%Y-%m-%d').date()
        # 从后往前遍历 date
        for i in range(len(date_list) - 1, -1, -1):
            date_list[i] = date_list[i].replace(' 00:00:00','')
            cur_date = datetime.datetime.strptime(date_list[i],'%Y-%m-%d').date()
            if(delete_time >= cur_date):
                break

        # 删除多余的时间
        for i in range(i, len(date_list)):
            file.drop(date_list[i],axis = 0, inplace = True)
    return file

def get_new_date_info(number, interval):
    # 处理时间
    end = datetime.datetime.now()
    # interval + 1：保证删除 delete_time 那一天的股票
    start = datetime_to_date(end - datetime.timedelta(days = interval))
    # 将datetime格式的end，转换为date格式的 end，保证此转换在上一步计算之后，否则会影响起始日期的计算
    end = datetime_to_date(end)

    stock = data.DataReader(number + get_exchange_tail(number), 'yahoo', start, end)
    #对 stock 处理，获取其 index 并转换成合适的格式
    str_stock = str(stock.index)
    str_stock = str_stock.replace('\n','')
    str_stock = str_stock.replace(' ','')
    str_stock = str_stock.replace('\'','')
    left_brace = str_stock.find('[')
    right_brace = str_stock.find(']')
    str_stock = str_stock[left_brace + 1:right_brace]
    list_stock = str_stock.split(',')
    # 转换为 index
    stock_index = pd.Series({'Date':list_stock}).tolist()
    # 设置为新的的索引
    stock.set_index(stock_index,inplace = True)
    stock.index.name = 'Date'
    return stock

'''
@ desc: 获取每支股票的信息，并保存
@ para: interval(前 interval 天的天数)
@ return: None
'''   
def get_all_info(interval):
    # 获取文件夹路径
    info_dir = os.listdir(stock_info_file_path)

    for stock_file in info_dir:
        file_path = path_connect(stock_info_file_path, stock_file)
        str_number = stock_file[:stock_file.find('.')]
        csv_data = pd.read_csv(file_path, dtype=object, index_col = 0)
        local_data = pd.DataFrame(csv_data)    # csv 转换为 DataFrame
        local_data = clear_stock_data(local_data, interval)
        new_stock = get_new_date_info(str_number,interval)
        # 连接两个表
        local_data = local_data.append(new_stock)
        # 保存数据到本地
        local_data.to_csv(file_path, index = True)


'''
@ desc: 获取股票的信息
@ para: interval(前 interval 天的天数)
@ return: None
'''
def get_stock_info(interval):
    get_avaliable_stock()
    #print('avaliable finish')
    update_info_folder()
    #print('info_folder_finish')
    get_all_info(interval)

    
def act(interval,stock_file):
    #print(interval,stock_file)
    file_path = path_connect(stock_info_file_path, stock_file)
    str_number = stock_file[:stock_file.find('.')]
    csv_data = pd.read_csv(file_path, dtype=object, index_col = 0)
    local_data = pd.DataFrame(csv_data)    # csv 转换为 DataFrame
    local_data = clear_stock_data(local_data, interval)
    new_stock = get_new_date_info(str_number,interval)
    # 连接两个表
    local_data = local_data.append(new_stock)
    # 保存数据到本地
    local_data.to_csv(file_path, index = True)


   
def test():
    p = Pool(5) # 创建3个进程
    info_dir = os.listdir(stock_info_file_path)
    for stock_file in info_dir:
        p.apply(get_all_info,args=(1,))
    

if __name__=="__main__":
    #get_stock_info(2)
    test()