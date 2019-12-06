import time
import re
import requests
from selenium import webdriver
from datetime import datetime

def get_password(filename='key.txt'):
    with open(filename,'r') as f:
        password = f.read().strip()
    return password

def get_check_code(html):
    # 正規劃方式
    check_code = re.search(r'CheckCode=\'(?P<code>\d*)\'', html).group('code')
    # check_code = html.split('CheckCode=\'')[-1].split('\'')[0]
    return check_code

driver = webdriver.Chrome()
driver.get('http://ntcbadm1.ntub.edu.tw/')

#login
driver.find_element_by_id('UserID').send_keys('11111111')
driver.find_element_by_id('PWD').send_keys(get_password())
driver.find_element_by_id('txtCheckCode').send_keys(get_check_code(driver.page_source))
driver.find_element_by_id('loginbtn').click()


# print(driver.current_url)

#查看網站loading完了沒
# for i in range(10):
#     state = driver.execute_script('return document.readyState')
#     print(state)
#get
time.sleep(3)
driver.find_element_by_class_name('ThemePanelMainItem').click()
time.sleep(3)
# driver.find_element_by_xpath('//*[@id="div_content"]/table/tbody/tr[3]/td[5]/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/a').click()
driver.find_element_by_link_text('個人請假缺曠記錄').click()
time.sleep(3)
now = datetime.now().strftime('%Y-%m-%d-%H-%H-%S')
driver.save_screenshot(f'{now}.png')
driver.close()


# Send

token = '1111111111:aaaaaaaaaa_aaaaaaaaaaa'
chat_id= '1111111'
requests.get(
    f'https://api.telegram.org/bot{token}/sendMessage', 
    params={
        'chat_id':chat_id,
        'text':f'您{now} 的缺況紀錄如下',
})

requests.post(
    f'https://api.telegram.org/bot{token}/sendPhoto', 
    params={
        'chat_id':chat_id,
    },
    files={
        'photo':open(f'{now}.png', 'rb'),
    }
)