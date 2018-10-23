# data_crawler
python爬虫
## 拉勾职位信息爬取分析
### 结构图
```
lagou
│  __init__.py
│
├─conf
│      common.py #配置信息
│      __init__.py
│
├─crawler  爬取模块
│      job_crawler.py  #职位信息爬取并导出csv文件
│      __init__.py
│
├─data
│      #职位信息
│
└─data_analysis  分析模块
       job_analysis.py 数据清洗、分析、可视化
       CompareType.py 枚举 比较类型
```
### 职位信息爬爬取模块

1.获取报文原始数据
```
{
	'totalCount': 10213,
	'locationInfo': {
		'city': '北京',
		'district': None,
		'queryByGisCode': False,
		'businessZone': None,
		'locationCode': None,
		'isAllhotBusinessZone': False
	},
	'resultSize': 15,
	'queryAnalysisInfo': {
		'jobNature': None,
		'companyName': None,
		'positionName': 'python',
		'usefulCompany': False,
		'industryName': None
	},
	'strategyProperty': {
		'name': 'dm-csearch-useUserAllInterest',
		'id': 0
	},
	'hotLabels': None,
	'hiTags': None,
	'result': [{
		'companyId': 63714,
		'approve': 1,
		'jobNature': '全职',
		'workYear': '1-3年',
		'education': '本科',
		'city': '北京',
		'companyLogo': 'i/image/M00/59/0B/CgqKkVfWgPaAdaAxAAAq6WYoG_0975.png',
		'positionAdvantage': '技术大牛多,福利待遇好',
		'salary': '25k-40k',
		'positionLables': ['后端'],
		'industryLables': [],
		'businessZones': None,
		'industryField': '移动互联网,教育',
		'companyShortName': '粉笔网',
		'companyFullName': '北京粉笔蓝天科技有限公司',
		'adWord': 0,
		'score': 0,
		'positionId': 5232056,
		'positionName': 'Python开发工程师',
		'createTime': '2018-10-18 11:25:13',
		'financeStage': '不需要融资',
		'companySize': '150-500人',
		'companyLabelList': ['技能培训', '节日礼物', '年底双薪', '带薪年假'],
		'publisherId': 3028023,
		'district': '朝阳区',
		'longitude': '116.481162',
		'latitude': '39.996092',
		'formatCreateTime': '11:25发布',
		'hitags': None,
		'resumeProcessRate': 100,
		'resumeProcessDay': 2,
		'imState': 'today',
		'lastLogin': 1539835283000,
		'explain': None,
		'plus': None,
		'pcShow': 0,
		'appShow': 0,
		'deliver': 0,
		'gradeDescription': None,
		'promotionScoreExplain': None,
		'firstType': '开发|测试|运维类',
		'secondType': '后端开发',
		'isSchoolJob': 0,
		'subwayline': '15号线',
		'stationname': '望京东',
		'linestaion': '14号线东段_望京;14号线东段_阜通;14号线东段_望京南;15号线_望京东;15号线_望京',
		'thirdType': 'Python',
		'skillLables': ['后端']
	}]
}
```
