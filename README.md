---
title: ntub-abs-check
tags: python, note, bot,telegram
---
# ntub-abs-check

## chromedirver
* 下載chromedriver
* chromedriver.exe 放置路徑
```python=
C:\Users\ben\AppData\Local\Programs\Python\Python37-32
```
### 使用步驟
1. 到專案資料夾右鍵開啟 **Git bash**
2. 輸入 **pip install pipenv**
3. 輸入 **pipenv install selenium**
4. 執行虛擬環境：pipenv shell
5. 查看是否在虛擬環境中
```
$ which python
/c/Users/ben/.virtualenvs/ntub-abs-check-zYx6CQbe/Scripts/python
```

## main.py~ 
#### 爬蟲會依照不同網頁寫法而有所不同
### 自動開啟Chrome範例
```python=
import time
from selenium import webdriver

driver = webdriver.Chrome() 

driver.get('https://google.com') #開啟想要爬蟲的網頁
time.sleep(3)
driver.close()
```
### 將密碼放在另一個做讀檔的動作
```python=
def get_password(filename='key.txt'):
    with open(filename,'r') as f:
        password = f.read().strip()
    return password
```
### 針對特定id輸入資料
```python=
driver.find_element_by_id('UserID').send_keys('1111')
driver.find_element_by_id('PWD').send_keys(password)
```

### 觸發按鈕
```python=
driver.find_element_by_id('loginbtn').click()
driver.find_element_by_class_name('ThemePanelMainItem').click()
> (不推薦使用)
driver.find_element_by_xpath('//*[@id="div_content"]/table/tbody/tr[3]/td[5]/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/a').click()
```
### 抓取網頁原始碼資料
```python=
html = driver.page_source ->抓取所有網頁原始碼資料
```
#### 要抓取的範例
``` html=
<script type="text/javascript">
//<![CDATA[
CheckCode='83551';//]]>
</script>
```
```python=
check_code = html.split('CheckCode=\'')[-1].split('\'')[0]
```

##### 正規表示法
``` python=
check_code = re.search(r'CheckCode=\'(?P<code>\d*)\'', html).group('code')
```

### 看url
``` python=
driver.current_url
```
### 螢幕截圖存成照片檔
``` python=
from datetime import datetime
now = datetime.now().strftime('%Y-%m-%d-%H-%H-%S')
driver.save_screenshot(f'{now}.png')
```
### 關掉視窗
``` python=
driver.close()
```
## 注意事項
有時候網站還沒loading完會找不到特定元素
> 可以使用
``` python=
import time
time.sleep(3)
```

# Telegram
## 安裝
``` cmd=
pipenv install requests
```
## 建立Telegram Bot
1. 在Telegram中search BotFather 點選他
2. 輸入 /start
3. 輸入 /newbot
4. 輸入機器人名稱 ****_bot 範例:wei18_bot
5. 此時就會出現token 妥善保管
### 尋找chat_id
1. 先傳訊息給剛建立的bot
2. 在chrom搜尋 
```=
https://api.telegram.org/bot{Token}/getUpdates
```
* Token 為建立bot時所取得的(記得不用打{})
3. 此時會呈現chat_id
```html=
"from": {
          "id": 11111111, //就是這個
          "is_bot": false,
          "first_name": "aaa",
          "last_name": "a",
          "language_code": "zh-hans"
        },
```
 




## 系統查看曠課紀錄並且將結果傳到telegram案例
### 特別注意 UserID、PWD、token、chat_id 為敏感資訊在此都為無效代碼
```python=
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
    # 正規表示式
    check_code = re.search(r'CheckCode=\'(?P<code>\d*)\'', html).group('code')
    # check_code = html.split('CheckCode=\'')[-1].split('\'')[0]
    return check_code

driver = webdriver.Chrome()
driver.get('http://ntcbadm1.ntub.edu.tw/')

#login
driver.find_element_by_id('UserID').send_keys('1111')
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
```
