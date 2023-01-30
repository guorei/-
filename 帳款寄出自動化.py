import requests
import pygsheets
import requests
from selenium import webdriver
import datetime
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



gc = pygsheets.authorize(service_account_file = 'C:/Users/\gtseng1/Downloads/elite-advice-370803-1d67b30a02f1.json')  #找api授權檔
survey_url = 'https://docs.google.com/spreadsheets/d/1SMbiVpGYMaM9H5Hu0gWJbAvUGRdnHx3ySDioe0OVzyM/edit?usp=sharing'    #自動化表單網址
sht = gc.open_by_url(survey_url)  #打開表單
wks = sht[2]                      #第三個帳款推播通知表單
total_list = wks.get_values('A2','I48')  #將所有市場A到I欄資料抓起來
print(total_list)  

#開始把資料登入各市場帳款表單

for i in total_list:
    if i[2] == 'Bi-weekly':  #根據不同週期抓原帳款表單不同位置的資訊
        payment_url = i[5]   #帳款網址位置
        payment_sht = gc.open_by_url(payment_url)    #打開帳款網址
        payment_wks = payment_sht.worksheet_by_title(i[0] + 'Payable')  #找到各家市場payable的表單
        payment_detail = payment_wks.get_col(2)             #抓想要的資訊
        payment_detail2 = payment_wks.get_values('R','T')
        payment_detail3 = payment_wks.get_values('V','X')
        total_payout = payment_wks.get_value('Z2')
        print(payment_detail2)
        inform_url = i[6]    #各家市場自動化更新網址
        inform_sht = gc.open_by_url(inform_url)  #打開自動化更新網址
        inform_wks = inform_sht[0]               #第一個sheet
        inform_wks.update_col(1, payment_detail) #依序將各項資料填入
        inform_wks.update_values('B1', payment_detail2)
        inform_wks.update_values('E1', payment_detail3)
        inform_wks.update_value('H2', total_payout)
    else:
        payment_url = i[5]   #帳款網址位置
        payment_sht = gc.open_by_url(payment_url)  #打開帳款網址
        payment_wks = payment_sht.worksheet_by_title(i[0] + 'Payable')  #找到各家市場payable的表單
        payment_detail = payment_wks.get_col(2)    #抓想要的資訊
        payment_detail2 = payment_wks.get_values('K','M')
        payment_detail3 = payment_wks.get_values('O','Q')
        total_payout = payment_wks.get_value('V2')
        print(payment_detail2)
        inform_url = i[6]   #各家市場自動化更新網址
        inform_sht = gc.open_by_url(inform_url)  #打開自動化更新網址
        inform_wks = inform_sht[0]               #第一個sheet
        inform_wks.update_col(1, payment_detail) #依序將各項資料填入
        inform_wks.update_values('B1', payment_detail2)
        inform_wks.update_values('E1', payment_detail3)
        inform_wks.update_value('H2', total_payout)
        

    if i[8] == '要':    #依照第9欄看是否要寄出通知
        token = i[7]   #抓授權碼
        message = i[3] + '~' + i[4] + i[1] + '的帳款已更新囉!\n詳細請點擊下方連結網址\n' + i[6] + '\n若有問題皆可以提出謝謝您!'    #寄出的訊息
        headers = { "Authorization": "Bearer " + token }  #官網給的格式
        data = { 'message': message }
        requests.post("https://notify-api.line.me/api/notify",
                        headers = headers, data = data)

    else:
        continue

print("帳款寄出完成")
'''
# LINE Notify 權杖
token = 'DXg5ZCm9eUJ8AOQNOKuxcwM63NvKxYboMX1R1uKcUrU'

# 要發送的訊息
message = '閉嘴腦殘'

# HTTP 標頭參數與資料
headers = { "Authorization": "Bearer " + token }
data = { 'message': message }

# 以 requests 發送 POST 請求
requests.post("https://notify-api.line.me/api/notify",
    headers = headers, data = data)
'''
