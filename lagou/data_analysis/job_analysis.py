import pandas as pd
from lagou.conf.common import data_path
from matplotlib import  pyplot as plt
import jieba
from wordcloud import WordCloud
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
def data_clean(path):
    # 读取数据
    df = pd.read_csv(path, encoding='utf-8')
    # 数据清洗,剔除实习岗位
    # print(df['职位名称'].str.contains('实习'))
    df.drop(df[df['职位名称'].str.contains('实习')].index, inplace=True)
    # print(df.describe())
    # 由于CSV文件内的数据是字符串形式,先用正则表达式将字符串转化为列表,再取区间的均值
    pattern = '\d+'
    df['work_year'] = df['工作经验'].str.findall(pattern)
    # 数据处理后的工作年限
    avg_work_year = []
    # 工作年限
    for i in df['work_year']:
       # 如果工作经验为'不限'或'应届毕业生',那么匹配值为空,工作年限为0
       if len(i) == 0:
           avg_work_year.append(0)
       # 如果匹配值为一个数值,那么返回该数值
       elif len(i) == 1:
           avg_work_year.append(int(''.join(i)))
       # 如果匹配值为一个区间,那么取平均值
       else:
           num_list = [int(j) for j in i]
           avg_year = sum(num_list)/len(num_list)
           avg_work_year.append(avg_year)
    df['工作经验'] = avg_work_year

    # 将字符串转化为列表,再取区间的前25%，比较贴近现实
    df['salary'] = df['工资'].str.findall(pattern)
    # 月薪
    avg_salary = []
    for k in df['salary']:
       int_list = [int(n) for n in k]
       avg_wage = int_list[0]+(int_list[1]-int_list[0])/4
       avg_salary.append(avg_wage)
    df['月工资'] = avg_salary

    # 将学历不限的职位要求认定为最低学历:大专\
    df['学历要求'] = df['学历要求'].replace('不限','大专')
    return df
#工资直方图
def job_histogram(df):
    plt.hist(df['月工资'])
    plt.xlabel('工资 (千元)')
    plt.ylabel('频数')
    plt.title("工资直方图")
    plt.savefig('薪资.jpg')
    plt.show()
#工资分布饼形图
def company_distribution_pie_chart(df):
    # 绘制饼图并保存
    count = df['区域'].value_counts()
    plt.pie(count, labels=count.keys(), labeldistance=1.4, autopct='%2.1f%%')
    plt.axis('equal')  # 使饼图为正圆形
    plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
    plt.savefig('pie_chart.jpg')
    plt.show()
#学历要求直方图
def educational_requirement_histogram(df):
    # {'本科': 1317, '大专': 93, '硕士': 65, '博士': 0}
    dict = {}
    for i in df['学历要求']:
        if i not in dict.keys():
            dict[i] = 0
        else:
            dict[i] += 1
    index = list(dict.keys())
    print(index)
    num = []
    for i in index:
        num.append(dict[i])
    print(num)
    plt.bar(left=index, height=num, width=0.5)
    plt.show()
def welfare_treatment_cloud_picture(df):
    # 绘制词云,将职位福利中的字符串汇总
    text = ''
    for line in df['职位福利']:
        text += line
        # 使用jieba模块将字符串分割为单词列表
    cut_text = ' '.join(jieba.cut(text))
    # color_mask = imread('cloud.jpg')  #设置背景图
    cloud = WordCloud(
        background_color='white',
        # 对中文操作必须指明字体
        font_path='../font/HYQiHei-25JF.ttf',
        # mask = color_mask,
        max_words=1000,
        max_font_size=1000
    ).generate(cut_text)

    # 保存词云图片
    cloud.to_file('word_cloud.jpg')
    plt.imshow(cloud)
    plt.axis('off')
    plt.show()
if __name__ == '__main__':
    df = data_clean(data_path+'lagou_python.csv')
    # job_histogram(df)
    # company_distribution_pie_chart(df)
    # educational_requirement_histogram(df)
    welfare_treatment_cloud_picture(df)