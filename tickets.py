# -*- coding: utf-8 -*-
"""
@author: ppy2790
"""
from splinter.browser import Browser
from time import sleep
import traceback
import time, sys

class huoche(object):
	"""docstring for huoche"""
	driver_name=''
	executable_path=''
	#用户名，密码
	username = u"12306用户名"
	passwd = u"12306密码"
	# cookies值得自己去找, 下面两个分别是上海, 太原南
	starts = u"%u4E0A%u6D77%2CSHH"
	ends = u"%u592A%u539F%2CTYV"
	# 时间格式2018-01-19
	dtime = u"2018-01-19"
	# 车次，选择第几趟，0则从上之下依次点击
	order = 0
	###乘客名
	users = [u"你的名字"]
	##席位
	xb = u"二等座"
	pz=u"成人票"

	"""网址"""
	ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
	login_url = "https://kyfw.12306.cn/otn/login/init"
	initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
	buy="https://kyfw.12306.cn/otn/confirmPassenger/initDc"
	login_url='https://kyfw.12306.cn/otn/login/init'
	
	def __init__(self):
		self.driver_name='chrome'
		self.executable_path='/usr/local/bin/chromedriver'

	def login(self):
		self.driver.visit(self.login_url)
		# 填充密码
		self.driver.fill("loginUserDTO.user_name", self.username)
		# sleep(1)
		self.driver.fill("userDTO.password", self.passwd)
		print u"等待验证码，自行输入..."
		while True:
			if self.driver.url != self.initmy_url:
				sleep(1)
			else:
				break

	def start(self):
		self.driver=Browser(driver_name=self.driver_name,executable_path=self.executable_path)
		self.driver.driver.set_window_size(1400, 1000)
		self.login()
		# sleep(1)
		self.driver.visit(self.ticket_url)
		try:
			print u"购票页面开始..."
			# sleep(1)
			# 加载查询信息
			self.driver.cookies.add({"_jc_save_fromStation": self.starts})
			self.driver.cookies.add({"_jc_save_toStation": self.ends})
			self.driver.cookies.add({"_jc_save_fromDate": self.dtime})

			self.driver.reload()

			count=0
			if self.order!=0:
				while self.driver.url==self.ticket_url:
					self.driver.find_by_text(u"查询").click()
					count += 1
					print u"循环点击查询... 第 %s 次" % count
					# sleep(1)
					try:
						self.driver.find_by_text(u"预订")[self.order - 1].click()
					except Exception as e:
						print e
						print u"还没开始预订"
						continue
			else:
				while self.driver.url == self.ticket_url:
					self.driver.find_by_text(u"查询").click()
					count += 1
					print u"循环点击查询... 第 %s 次" % count
					# sleep(0.8)
					try:
						for i in self.driver.find_by_text(u"预订"):
							i.click()
							sleep(1)
					except Exception as e:
						print e
						print u"还没开始预订 %s" %count
						continue
			print u"开始预订..."
			# sleep(3)
			# self.driver.reload()
			sleep(1)
			print u'开始选择用户...'
			for user in self.users:
				self.driver.find_by_text(user).last.click()

			print u"提交订单..."
			sleep(1)
			# self.driver.find_by_text(self.pz).click()
			# self.driver.find_by_id('').select(self.pz)
			# # sleep(1)
			# self.driver.find_by_text(self.xb).click()
			# sleep(1)
			self.driver.find_by_id('submitOrder_id').click()
			# print u"开始选座..."
			# self.driver.find_by_id('1D').last.click()
			# self.driver.find_by_id('1F').last.click()

			sleep(1.5)
			print u"确认选座..."
			self.driver.find_by_id('qr_submit_id').click()

		except Exception as e:
			print e

cities= {'成都':'%u6210%u90FD%2CCDW',
'重庆':'%u91CD%u5E86%2CCQW',  
'北京':'%u5317%u4EAC%2CBJP',
'广州':'%u5E7F%u5DDE%2CGZQ', 
'杭州':'%u676D%u5DDE%2CHZH',
'宜昌':'%u5B9C%u660C%2CYCN',
'郑州':'%u90D1%u5DDE%2CZZF',
'深圳':'%u6DF1%u5733%2CSZQ',
'西安':'%u897F%u5B89%2CXAY',
'大连':'%u5927%u8FDE%2CDLT',
'武汉':'%u6B66%u6C49%2CWHN',
'上海':'%u4E0A%u6D77%2CSHH',
'南京':'%u5357%u4EAC%2CNJH',
'合肥':'%u5408%u80A5%2CHFH'}

if __name__ == '__main__':
	huoche=huoche()
	huoche.starts=cities[sys.argv[1]]
	huoche.ends = cities[sys.argv[2]]
	huoche.dtime = sys.argv[3]
	huoche.start()
