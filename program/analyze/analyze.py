import glob
import os
import pandas as pd
import numpy as np


avaliable_file_path = os.path.join(os.getcwd(),'program','analyze','data', 'avaliable_stock')
stock_info_file_path = os.path.join(os.getcwd(),'program','analyze','data', 'test')
result_file_path = os.path.join(os.getcwd(),'program','message')
result_path = os.path.join(os.getcwd(),'program','message', 'result.csv')
# stock_info_file_path 路劲下的文件数量
stock_info_number = len([lists for lists in os.listdir(stock_info_file_path) if os.path.isfile(os.path.join(stock_info_file_path, lists))])
# 定义一个 DataFrame 保存每支股票单独的信息
df_info = pd.DataFrame(columns = ['stock_number', 'stock_name', 'cur_value',\
     'max_value', 'min_value', 'mid_value', 'avg_value', 'last_down_count']) 

# 定义一个字典，保存公共的信息
dict_info = {}
# 定义一个列表，保存推荐的股票信息
list_reocom = []

# 对文件路径进行链接
def path_connect(base, current):
    return os.path.join(base, str(current))

#　四舍五入对一个浮点数据保留两位小数
def keep_two_decimal(data):
    value = int(data * 1000)
    unit = value % 10   # 获取个位上的数
    if(unit <= 4):
        data = int(data * 100) / 100
    else:
        data = int(data * 100 + 1) / 100
    return data


# 更新 df_info DataFrame 中的值
# row_index：行的索引，数值
# column_name：列的索引名称，字符串
# value：将要修改的值
def update_result(row_index, column_name, value):
    df_info.loc[row_index, column_name] = value

# 获取股票名称和股票代码，保存在 dict_info 中
def get_info_stock_title():
    # 定义两个列表，分别保存股票名称和代码
    list_name = []
    list_number = []
    # 打开沪深股票名称列表
    dict_tittle_sz_path = path_connect(avaliable_file_path, 'sz.txt')
    dict_tittle_sh_path = path_connect(avaliable_file_path, 'sh.txt')
    sz = open(dict_tittle_sz_path,'r',encoding='utf-8')
    sh = open(dict_tittle_sh_path,'r',encoding='utf-8')
    # str 转为 dict
    sz=eval(sz.read())
    sh=eval(sh.read())
    # 遍历两个交易所
    for key in sz:
        list_name.append(sz[key])
        list_number.append(key)
    for key in sh:
        list_name.append(sh[key])
        list_number.append(key)

    # 对值进行存储
    for index in range(len(list_name)):
        update_result(index, 'stock_number',list_number[index])
        update_result(index, 'stock_name',list_name[index])
    
    # 将 df_info 的索引改为股票代码
    df_info.set_index('stock_number', inplace=True)

# 获取股票的当前价格
def get_info_cur_value(df):
    last_column = df.iloc[-1:]
    cur_value = last_column['Close']
    # list 转 float，并去掉两位小数
    cur_value = int(float(cur_value) * 100) / 100
    # 返回
    return cur_value

def get_info_max_value(df):
    close_value = df['High']
    list_data = close_value.sort_values(ascending = True).tolist()
    return list_data[-1]

def get_info_min_value(df):
    close_value = df['Low']
    list_data = close_value.sort_values(ascending = True).tolist()
    return list_data[0]

# 获取股票涨跌的数据
# 定义一次'跌-涨'为一个数据
def get_calculate_up_down(data):
    # 涨跌的方向 0:跌 1:涨
    orientation = 0 # 随便赋的值
    # 某段事件内,连续涨的数量
    up_count = 0
    # 某段事件内,连续跌的数量
    down_count = 0
    # 所有数量 对应名称表示连续涨跌的数量,6表示大于等于6天的数量
    list_up_count = [0, 0, 0, 0, 0, 0]
    list_down_count = [0, 0, 0, 0, 0, 0]
    # 所有幅度 对应名称表示连续涨跌的幅度,6表示大于等于6天的幅度
    list_up_range = [0, 0, 0, 0, 0, 0]
    list_down_range = [0, 0, 0, 0, 0, 0]

    count = 0
    for index in range(1, len(data)):
        # 第一次判断涨跌方向
        if(1 == index):
            if(data[1] > data[0]):
                orientation = 1
            else:
                orientation = 0

        if(data[index] > data[index - 1]):  # 涨
            if(0 == orientation):   # 上次为跌
                list_down_count[down_count - 1] += 1
                if(down_count >= 6): 
                    list_down_range[5] += (data[index - 1 - down_count] / data[index - 1]) - 1
                else:
                    list_down_range[down_count - 1] += (data[index - 1 - down_count] / data[index - 1]) - 1
                down_count = 0
            
            up_count += 1
            orientation = 1
        elif(data[index] < data[index - 1]): # 跌
            #print(count)
            count+= 1
            if(1 == orientation):   # 上次为涨
                list_up_count[up_count - 1] += 1
                if(up_count >= 6):
                    list_up_range[5] += (data[index - 1] / data[index - 1 - up_count]) - 1
                else:
                    list_up_range[up_count - 1] += (data[index - 1] / data[index -1 - up_count]) - 1
                up_count = 0
            down_count += 1
            orientation = 0

        else:                               # 没有涨跌
            pass 
    #最后一次的处理
    if(0 != up_count):
        list_up_count[up_count - 1] += 1
        if(up_count >= 6):
            list_up_range[5] += (data[index] / data[index - up_count]) - 1
        else:
            list_up_range[up_count - 1] += (data[index] / data[index - up_count]) - 1
        up_count = 0
        
    elif(0 != down_count):
        list_down_count[down_count - 1] += 1
        if(down_count >= 6): 
            list_down_range[5] += (data[index - down_count] / data[index]) - 1
        else:
            list_down_range[down_count] += (data[index - down_count] / data[index - 1]) - 1
        down_count = 0    
    
    # 最后处理平均幅度
    for index in range(len(list_up_count)):
        if(list_up_count[index] == 0):
            list_up_range[index] = 0
        else:
            list_up_range[index] = keep_two_decimal(list_up_range[index] / list_up_count[index])
        
        if(list_down_count[index] == 0):
            list_down_range[index] = 0
        else:
            list_down_range[index] = keep_two_decimal(list_down_range[index] / list_down_count[index])

#获取最近连续下跌的天数
def get_calculate_last_down(data):
    result = 0
    for index in range(len(data) - 1, -1, -1):
        if(data[index] < data[index - 1]):
            result += 1
        elif(data[index] > data[index - 1]):
            break
        else:
            pass

    return result

# 计算一些参数，通过字典返回
def get_info_calculate(df):
    # 平均值，中值
    result = {'average_value':0.0, 'middle_value': 0.0,'last_down_count':0.0}
    # 获取数据，转换为 float 类型
    cur_value = df['Close'].tolist()
    for index in range(len(cur_value)):
        cur_value[index] = float(cur_value[index])
    # 计算平均值
    average_value = keep_two_decimal(np.mean(cur_value))
    result['average_value'] = average_value
    # 计算中位数
    middle_value = keep_two_decimal(np.median(cur_value))
    result['middle_value'] = middle_value 
    # 获取涨跌的数据
    test_data = [1,5,6,1,2,1,2,1,2,1,2,1,2,1,2,1,2]
    up_down = get_calculate_up_down(test_data)
    # 获取最近连续下跌的天数
    
    last_down_count = get_calculate_last_down(cur_value)
    result['last_down_count'] = last_down_count

    return result



# 遍历所有股票，提取可用信息，保存到 df_info 中，再保存到本地
def get_df_info():
    # 更新股票名称和代码
    get_info_stock_title()
    # 遍历信息文件夹
    info_dir = os.listdir(stock_info_file_path)
    for stock_file in info_dir:
        # 获取本地数据
        file_path = path_connect(stock_info_file_path, stock_file)
        csv_data = pd.read_csv(file_path,dtype=object)
        df_data = pd.DataFrame(csv_data)    # csv 转换为 DataFrame
        
        # 获取一些计算值
        cal_dict = get_info_calculate(df_data)

        # 获取索引(股票代码既索引)
        index = stock_file[:6]
        
        # 获取当前价格
        cur_value = get_info_cur_value(df_data)
        update_result(index,'cur_value',cur_value)
        # 最大值
        max_value = get_info_max_value(df_data)
        update_result(index,'max_value',max_value)
        # 最小值
        min_value = get_info_min_value(df_data)
        update_result(index,'min_value',min_value)
        # 最近连续下跌的天数
        last_down_count = cal_dict['last_down_count']
        update_result(index,'last_down_count',last_down_count)
        
        
    # 保存文件到本地
    df_info.to_csv(result_path,index = True)
    #print(df_info)

if __name__=="__main__":
    get_df_info()
    