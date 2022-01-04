from itertools import groupby
import matplotlib.pyplot as plt
import pandas as pd
import time
import openpyxl
import numpy as np
from matplotlib.font_manager import FontProperties
from pyecharts.charts import Bar
import matplotlib
import xlrd


# -*- coding: utf-8 -*-
def f(df):
    return df[2] - df[1] > 5


def drawpie(lj,counts):
    group_names = ['2~5', '5~10', '10~20', '20~30', '>30']
    y = counts.values
    explodes = [0,0,0,0.1,0.2]
    plt.pie(y, radius=0.8, labels=group_names, explode=explodes, autopct='%1.2f%%', pctdistance=0.9, labeldistance=1.2,
            textprops={'fontsize': 8, 'color': 'black'})
    plt.axis('equal')
    # plt.figure(figsize=(20, 6.5))
    # plt.legend(loc='upper right',bbox_to_anchor=(1.1,1.05),fontsize=10,borderaxespad=0.3)
    plt.savefig(str(lj).split('.')[0] + "饼.png")
    #plt.show()
    plt.close()

# 柱状图加数值
def drawZf(lj,counts):
    x = counts.index
    y = counts.values
    rects = plt.bar(x, y, width=0.35)
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=10, ha='center', va='bottom')

    font = FontProperties(fname=r"font/SimHei.ttf", size=14)
    plt.xlabel('区间', fontproperties=font)
    plt.ylabel('频数', fontproperties=font)
    plt.title(str(lj).replace("_", "月").split("/")[1].split(".")[0] + "日", fontproperties=font);
    plt.savefig(str(lj).split('.')[0] + "柱.png")  # 保存
    plt.close()




def continusFind(num_list):
    '''
    列表中连续数字段寻找
    '''
    num_list.sort()
    s = 1
    find_list = []
    have_list = []
    while s <= len(num_list) - 1:
        if num_list[s] - num_list[s - 1] == 1:
            flag = s - 1
            while num_list[s] - num_list[s - 1] == 1:
                s += 1
            find_list.append(num_list[flag:s])
            have_list += num_list[flag:s]
        else:
            s += 1


def listbdy(b):
    y = []
    i = 0
    for x in range(len(b) - 1):
        if (b[x] != 0.0):
            i = i + 1
        else:
            y.append(i)
            i = 0

    print(y)
    av = 0;
    sum = 0
    for yy in range(len(y) - 1):
        if (y[yy] > 600):
            av = av + y[yy]
            sum = sum + 1;
    x = av / sum
    print("平均持续时间" + str(x))
    print("最长持续时间" + str(max(y)))
    print("次数" + str(sum))


# 将0去掉
def listxy0(a):
    b = []
    try:
        for x in range(len(a) - 2):
            if (a[x] != a[x + 1] or a[x] != 0.0):
                b.append(a[x])
    except:
        print("抛异常")
    return b


def read(lj):
    result = pd.read_excel(lj, sheet_name=0)
    result1 = pd.read_excel(lj, sheet_name=1)
    Ldata = pd.concat([result['通道03(V)'], result1['通道03(V)']], join="outer")
    number_bins = [2, 5, 10, 20, 30,110]
    group_names = ['2~5', '5~10', '10~20','20~30', '>30']
    cuts = pd.cut(Ldata, number_bins, labels=group_names)
    counts = pd.value_counts(cuts)
    print(lj)
    sum = 0;
    ctrlc = counts.values
    for i in counts.values:
        sum = sum + i
    for i in ctrlc:
        print('{:.2%}'.format(i / sum))
    drawZf(lj, counts)
    drawpie(lj, counts)
    # 获取最大值
    # print(max(Ldata))

    # a = np.where(Ldata < 2, 0, Ldata)
    # list_a = listxy0(list(a))
    # listbdy(list_a)

#
def readsheet1(lj):
    result = pd.read_excel(lj)
    # bar=Bar()
    # bar.add_xaxis(result["索引"].to_list())
    # bar.add_yaxis("通道3",result["通道03(V)"].to_list())
    # bar.render("data/1.html")
    x=[]
    for a in result['时间']:
        x.append(str(a).split(' ')[1])
    font = FontProperties(fname=r"font/SimHei.ttf", size=14)
    plt.bar(result['索引'],result['通道03(V)'])
    #plt.xticks(range(len(result['时间']))[::10000],result['时间'][::10000],rotation=-60,ha="left",fontsize=10);
    plt.xticks(range(len(x))[::5000], x[::5000], rotation=-60, ha="left", fontsize=10);
    plt.xlabel('时间', fontproperties=font)
    plt.ylabel('通道3', fontproperties=font)
    plt.gcf().subplots_adjust(bottom=0.3)
    plt.title(str(lj).replace("_","月").split("/")[1].split(".")[0]+"日", fontproperties=font);
    plt.savefig(str(lj).split('.')[0]+"日" + ".png")
    #plt.show()
    plt.close()

def readsheetdouble(lj):
    result = pd.read_excel(lj, sheet_name=0)
    result1 = pd.read_excel(lj, sheet_name=1)
    y = pd.concat([result['通道03(V)'], result1['通道03(V)']], join="outer")
    xtime=pd.concat([result['时间'], result1['时间']], join="outer")
    xt = []
    for a in xtime:
        xt.append(str(a).split(' ')[1])
    x = range(len(y))
    # bar=Bar()
    # bar.add_xaxis(result["索引"].to_list())
    # bar.add_yaxis("通道3",result["通道03(V)"].to_list())
    # bar.render("data/1.html")
    font = FontProperties(fname=r"font/SimHei.ttf", size=14)
    plt.bar(x,y)
    plt.xticks(range(len(xt))[::10000], xt[::10000], rotation=-60, ha="left", fontsize=10);
    plt.xlabel('时间', fontproperties=font)
    plt.ylabel('通道3', fontproperties=font)
    plt.gcf().subplots_adjust(bottom=0.3)
    plt.title(str(lj).replace("_","月").split("/")[1].split(".")[0]+"日", fontproperties=font);
    plt.savefig(str(lj).split('.')[0]+"日" + ".png")
    plt.close()

def readsheet(lj):
    result = pd.read_excel(lj)
    Ldata = np.array(result['通道03(V)'])
    plt.plot()


    #画柱状图
    number_bins = [2, 5, 10, 20, 30, 110]
    group_names = ['2~5', '5~10', '10~20','10~30', '>30']
    cuts = pd.cut(Ldata, number_bins, labels=group_names)

    counts = pd.value_counts(cuts)
    print(lj)
    sum=0;
    ctrlc=counts.values
    for i in counts.values:
        sum=sum+i
    for i in ctrlc:
        print('{:.2%}'.format(i/sum))
    drawZf(lj , counts)
    drawpie(lj , counts)

    # counts.plot(kind='pie',autopct='%1.f%%', #饼图添加数值标签
    #            counterclock=False,#设置饼图顺时针
    #            textprops={'fontsize':8,'color':'black'})


    # print(lj+":")
    # 最大值
    # print(max(Ldata))


if __name__ == '__main__':
    #    dz=['data/7月15日.xlsx','data/7月16日.xlsx','data/7月17日.xlsx','data/7月18日.xlsx','data/7月19日.xlsx','data/7月20日.xlsx','data/7月21日.xlsx','data/7月22日.xlsx','data/7月23日.xlsx','data/7月24日.xlsx','data/7月25日.xlsx','data/7月26日.xlsx','data/7月27日.xlsx','data/7月28日.xlsx','data/7月29日.xlsx','data/7月30日.xlsx','data/7月31日.xlsx','data/8月1日.xlsx','data/8月2日.xlsx','data/8月3日.xlsx','data/8月4日.xlsx','data/8月5日.xlsx','data/8月6日.xlsx','data/8月7日.xlsx','data/8月8日.xlsx','data/8月9日.xlsx','data/8月11日.xlsx','data/8月10日.xlsx','data/8月12日.xlsx']
    #'data/9_17.xlsx', 'data/9_18.xlsx',
    dz = ['data/9_17.xlsx', 'data/9_18.xlsx','data/9_19.xlsx', 'data/9_20.xlsx', 'data/9_21.xlsx', 'data/9_22.xlsx',
          'data/9_23.xlsx', 'data/9_24.xlsx', 'data/9_25.xlsx', 'data/9_26.xlsx', 'data/9_27.xlsx', 'data/9_28.xlsx',
          'data/9_29.xlsx', 'data/9_30.xlsx', 'data/10_01.xlsx', 'data/10_02.xlsx', 'data/10_03.xlsx',
          'data/10_04.xlsx', 'data/10_05.xlsx', 'data/10_06.xlsx', 'data/10_07.xlsx', 'data/10_08.xlsx',
          'data/10_09.xlsx', 'data/10_10.xlsx', 'data/10_11.xlsx', 'data/10_12.xlsx', 'data/10_13.xlsx',
          'data/10_14.xlsx', 'data/10_15.xlsx', 'data/10_16.xlsx', 'data/10_17.xlsx', 'data/10_18.xlsx']

    readsheet('data/9_16.xlsx');
    #readsheet('data/10_19.xlsx');
    #readsheet1('data/9_16.xlsx');
    readsheet('data/10_19.xlsx');

    # #time.sleep(5);
    # readsheet1('data/10_19.xlsx');

    # for i in range(len(dz)):
    #     readsheetdouble(dz[i]);
    #     #read(dz[i]);
    #     time.sleep(5);
    #read(dz[30])
    for i in range(len(dz)):
        read(dz[i])
        time.sleep(5)
    # readsheet('data/10_19.xlsx')
    # lst = [2, 3, 5, 6, 7, 8,1, 11, 12, 13,15,27,28,29]
    #
    # #fun = lambda (i, v): v - i
    # fun = lambda x: x[1] - x[0]
    # for k, g in groupby(enumerate(lst), fun):
    #     print ([v for i, v in g])
