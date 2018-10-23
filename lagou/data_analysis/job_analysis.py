import jieba
import pandas as pd
from pylab import *
from wordcloud import WordCloud
from lagou.data_analysis.CompareType import CompareType
from lagou.conf.common import data_path, job_parse_list,picture_path
mpl.rcParams['font.sans-serif'] = ['SimHei']
def data_clean(path):
    f = open(path,encoding='utf-8')
    # 读取数据
    df = pd.read_csv(f)
    # 数据清洗,剔除实习岗位
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
       if len(int_list) == 1:
           avg_salary.append(int_list[0])
           continue
       avg_wage = int_list[0]+(int_list[1]-int_list[0])/4
       avg_salary.append(avg_wage)
    df['月工资'] = avg_salary

    # 将学历不限的职位要求认定为最低学历:大专\
    df['学历要求'] = df['学历要求'].replace('不限','大专')
    return df
#工资直方图
def salary_histogram(df,job,show_type=True):
    plt.hist(df['月工资'])
    plt.xlabel('月薪 (k)')
    plt.ylabel('数量')
    if show_type is True:
        plt.title('{}工资直方图'.format(job))
        save_and_show_picture(picture_path+'job_histogram.jpg')
    else:
        plt.title(job)

    # 学历要求直方图
def work_year_requirement_histogram(df, job, show_type=True):
    plt.hist(df['工作经验'])
    plt.xlabel('工作年限')
    plt.ylabel('数量')
    if show_type is True:
        plt.title('{}工作年限要求直方图'.format(job))
        save_and_show_picture(picture_path + 'job_histogram.jpg')
    else:
        plt.title(job)
#公司分布饼形图
def company_distribution_pie_chart(df,job,show_type=True):
    # 绘制饼图并保存
    count = df['区域'].value_counts()
    plt.pie(count, labels=count.keys(), labeldistance=1.4, autopct='%2.1f%%')
    plt.axis('equal')  # 使饼图为正圆形
    plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
    if show_type is True:
        # plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
        plt.title('{}公司分布饼形图'.format(job))
        save_and_show_picture(picture_path+'pie_chart.jpg')
    else:
        plt.title(job)
#学历要求直方图
def educational_requirement_histogram(df,job,show_type=True):

    dict = {}
    for i in df['学历要求']:
        if i not in dict.keys():
            dict[i] = 0
        else:
            dict[i] += 1
    index = list(dict.keys())
    index.sort()
    num = []
    for i in index:
        num.append(dict[i])
    print(num)
    plt.bar(left=index, height=num, width=0.5)
    if show_type is True:
        plt.title('{}学历要求直方图'.format(job))
        save_and_show_picture(picture_path+'educational_requirement_histogram.jpg')
    else:
        plt.title(job)
#福利词云图
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
#各种职位比较图
def job_compare_chart(compare_type,job_list=[]):
    length = len(job_list)
    x = int(math.sqrt(length))+1
    y = x-1
    #去重
    job_list = list(set(job_list))
    job_list.sort()
    save_path = None
    suptitle = None
    wspace = 0.2
    hspace = 0.2
    for job in job_list:
        index = job_list.index(job)+1
        df = data_clean(data_path + 'lagou_{}.csv'.format(job))
        plt.subplot(x*100+y*10+index)
        if compare_type == CompareType.salary:
            salary_histogram(df,job,False)
            if suptitle is None:
                suptitle = '各职位薪资直方图比较'
                save_path = picture_path+suptitle+'.jpg'
            wspace = 0.8
            hspace = 0.8
        elif compare_type == CompareType.educational_requirement:
            educational_requirement_histogram(df,job,False)
            if suptitle is None:
                suptitle = '各职位学历要求直方图比较'
                save_path = picture_path+suptitle+'.jpg'
            wspace = 0.5
            hspace = 0.5
        elif compare_type == CompareType.company_distribution:
            company_distribution_pie_chart(df,job,False)
            if suptitle is None:
                suptitle = '各职位公司分布饼形图比较'
                save_path = picture_path+suptitle+'.jpg'

        elif compare_type == CompareType.work_years:
            work_year_requirement_histogram(df,job,False)
            if suptitle is None:
                suptitle = '各职位工作经验要求直方图比较'
                save_path = picture_path+suptitle+'.jpg'
            wspace = 0.8
            hspace = 0.8
        else:
            raise RuntimeError('未知CompareType')
        plt.suptitle(suptitle)

    save_and_show_picture(save_path,wspace,hspace)
def save_and_show_picture(path,x=0.2,y=0.2):
    plt.savefig(path)
    plt.subplots_adjust(wspace=x, hspace=y)
    plt.show()
if __name__ == '__main__':
    df = data_clean(data_path+'lagou_java.csv')
    # salary_histogram(df,'大数据')
    # company_distribution_pie_chart(df,'大数据')
    # educational_requirement_histogram(df,'大数据')
    # work_year_requirement_histogram(df,'java')
    # welfare_treatment_cloud_picture(df)
    job_compare_chart(CompareType.salary,job_parse_list)
    # print(CompareType.salary)