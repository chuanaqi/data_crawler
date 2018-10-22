import requests
from lagou.conf.common import host,referer,proxies,user_agent,data_path,job_list
import time
import math
import pandas as pd
import random
# 获取请求结果
# kind 搜索关键字
# page 页码 默认是1
def get_json(kind, page=1,):
    # post请求参数
    param = {
        'first': 'true',
        'pn': page,
        'kd': kind
    }
    header = {
        'Host': host,
        'Referer': referer,
        'User-Agent': user_agent
    }

    # 请求的url
    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'

    delay_flag = False
    while delay_flag is False:
        # 每次抓取完成后,暂停一会,防止被服务器拉黑
        time.sleep(5)
        try:
            # 使用代理访问
            # response = requests.post(url, headers=header, data=param, proxies=random.choices(proxies)[0])
            # 不使用代理访问
            response = requests.post(url, headers=header, data=param)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                response = response.json()
                # 请求响应中的positionResult 包括查询总数 以及该页的招聘信息(公司名、地址、薪资、福利待遇等...)
                return response['content']['positionResult']
        except Exception as e:
            print(e)


    return None

def parse_job_list(job_list):
    # 爬取职位列表内的所有职位
    for kind in job_list:
        # 请求一次 获取总条数
        position_result = get_json(kind=kind)
        # 总条数
        total = position_result['totalCount']
        print('{}开发职位，招聘信息总共{}条.....'.format(kind, total))
        # 每页15条 向上取整 算出总页数
        page_total = math.ceil(total / 15)


        # 所有查询结果
        search_job_result = []
        # 为了节约效率 只爬去前100页的数据
        if page_total >= 100:
            page_total = 100
        for i in range(1, page_total+1):
            position_result = get_json(kind=kind, page=i)
            # print(position_result)
            # 当前页的招聘信息
            page_python_job = []
            for j in position_result['result']:
                python_job = []
                # 公司全名
                python_job.append(j['companyFullName'])
                # 公司简称
                python_job.append(j['companyShortName'])
                # 公司规模
                python_job.append(j['companySize'])
                # 融资
                python_job.append(j['financeStage'])
                # 所属区域
                python_job.append(j['district'])
                # 职称
                python_job.append(j['positionName'])
                # 要求工作年限
                python_job.append(j['workYear'])
                # 招聘学历
                python_job.append(j['education'])
                # 薪资范围
                python_job.append(j['salary'])
                # 福利待遇
                python_job.append(j['positionAdvantage'])
                # print(python_job)
                page_python_job.append(python_job)

            # 放入所有的列表中
            search_job_result += page_python_job
            print('第{}页数据爬取完毕, 目前职位总数:{}'.format(i, len(search_job_result)))
            output_csvfile(search_job_result,kind)
def output_csvfile(search_job_result,kind):
    # 将总数据转化为data frame再输出
    df = pd.DataFrame(data=search_job_result,
                      columns=['公司全名', '公司简称', '公司规模', '融资阶段', '区域', '职位名称', '工作经验', '学历要求', '工资', '职位福利'])
    df.to_csv(data_path + 'lagou_' + kind + '.csv', index=False, encoding='utf-8_sig')

if __name__ == '__main__':
    parse_job_list(job_list)