# -*- coding=utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import requests
import base64
import json
import time

print('配置加载中..\n')
chrome_path = './chromedriver'
chrome_options = Options()  # 创建chrome设置
chrome_options.add_argument('--ignore-certificate-errors')  # 无视证书引发的错误
# chrome_options.add_argument('--headless')  # 无窗口模式
driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)  # 配置chrome设置


def find_ele(xpath):
    return driver.find_element_by_xpath(xpath)


def isElementPresent(value):
    try:
        driver.find_element_by_xpath(value)
    except NoSuchElementException as e:
        return False
    else:
        return True


print('正在打开页面...\n')
idp_url = r'http://10.24.68.238:8044/#/workbench/worker-flow'
driver.get(idp_url)
driver.maximize_window()
time.sleep(1)

# 登入
print('输入用户名及密码...\n')
find_ele('//*[@id="app"]/div/form/div[2]/div[1]/div/div/input').send_keys('admin')  # 用户名
find_ele('//*[@id="app"]/div/form/div[2]/div[2]/div/div/input').send_keys('bigtimes2020')  # 密码

# 处理验证码

print('正在获取验证码...\n')
#  使用get_attribute()方法获取对应属性的属性值，src属性值就是图片地址
captcha_url = find_ele('//*[@id="app"]/div/form/div[2]/div[3]/div/img').get_attribute('src')
# 通过requests发送一个get请求到图片地址，返回的响应就是图片内容
captcha_img = requests.get(captcha_url)
# 将图片的二进制内容转换为base64编码
captcha_encode = base64.b64encode(captcha_img.content)
captcha_decode = captcha_encode.decode()

print('正在识别验证码中的内容...\n')
baidu_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token=24.0b4d94986ebe9380527c19250bf9091b.' \
            '2592000.1613122921.282335-23021865'
baidu_body = {'image': captcha_decode}
baidu_header = {"Content-Type": "application/x-www-form-urlencoded"}
baidu_ai = requests.post(baidu_url, baidu_body, baidu_header)
ocr_response = baidu_ai.text
print('OCR文字识别接口响应内容：', ocr_response)
print('接口响应码：', baidu_ai.status_code, '\n')
ocr_content = json.loads(ocr_response)
captcha_content = ocr_content.get('words_result')[0].get('words')
print('已识别出验证码内容，登录中...\n')
find_ele('//*[@id="app"]/div/form/div[2]/div[3]/div/div/input').send_keys(captcha_content)

find_ele('//*[@id="app"]/div/form/button').click()  # 登录
print('登录成功！\n')

print('正在准备下载文件...\n')
driver.get(idp_url)
time.sleep(1)
find_ele('//*[@id="app"]/div/div[2]/div[2]/section/div/div/div[2]/div/div/div[1]/div/div[2]/div/button[2]/span'
         '/span').click()
time.sleep(1)
find_ele('//*[@id="app"]/div/div[2]/div[2]/section/div/div/div[3]/div/div/div[2]/form/div[1]/div/div/div/label[2]'
         '/span[2]').click()
time.sleep(0.5)
find_ele('//*[@id="app"]/div/div[2]/div[2]/section/div/div/div[3]/div/div/div[2]/form/div[2]/div/div/'
         '*[name()="svg"]').click()
time.sleep(1)
print('文件下载成功！\n')

driver.close()
