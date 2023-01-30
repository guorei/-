import pygsheets
import requests
from selenium import webdriver
import datetime
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import shutil
import os
import datetime
import glob



uuid = ['6b0d8076-2a6d-4448-8236-5c1c2e2cd974', 'f4f688b1-a3a4-434b-aed4-90e23a5d838c', 'c0b10663-53a3-4f50-b402-e0e90e796a92', '3590bbf3-c349-4518-aea5-6fdbe8baf1ee',
        'b76cb4cf-ec72-5392-9189-d88201d4ff5a', '2ee70dee-d0cc-4806-a51f-f67ffe0b71dd', 'fc553480-a7f4-4d1b-b5f0-87a7fd489eba', '786526c0-aa9e-4ab7-8de1-99b30afa648e',
        'da76615f-cb88-44c3-9ebb-122584c50c22', '11de20d5-103f-446d-b837-ccc470bd6c2c', 'a3ac0589-940e-49bd-989c-2ac74313ce93', '19d67976-dff4-4709-b5b9-b4ea62fa03cc',
        '4263a635-0988-4fc0-92ff-6551539fe3c5', '4e003a61-7cf0-493a-a3c5-789032e74dd1', 'f587a10b-0250-420c-94e2-210554bead63', 'c37a313e-e99d-43f9-8a8a-438692682882',
        'b759a562-ef36-4b8b-b3b1-0a3438efbcae', 'efaccec4-74d5-5960-b900-934958642d23', '57060c6e-8227-4418-a12f-6bc943cb4f76', '283be6de-e3a5-50de-a57f-3997f95c6575',
        'c05af3e4-97ac-49b9-8f3a-bd6e35759f81', 'b7eb730b-e025-5d92-ae1c-fcc052c5f770', '6b92c13e-74ab-5ecb-8b6a-6f18bea36bd3', 'a723e187-9ed4-5d09-8f67-6476ecee1c46',
        '0eefc9b2-e3b2-5c09-b821-05ab831e99da', '01bc658d-6455-52c5-b4f4-a4a3c2fd2955',
        '4ec775f2-3c16-5805-a203-ac2ad83604a5', '993b2b4c-08a4-5ad9-b39e-c6faf207560c', 'e320ec65-0adf-5cbe-afb7-e2a36bfab382', '8d244e56-82f1-59bb-98a3-8635d1f04e31',
        '4a9e51a8-8c9b-5310-8e4b-9501cd2f57b9', '81d3da59-1b2d-5bdc-a1ba-88b5c938b470', 'c85569a6-9605-585f-ab6c-0ffd7710e73b',
        'b5d0431b-09e8-52da-936a-8af0fcf6e731', '293cb6c2-29c1-5591-8048-c5bdb2cdca37', 'f8739ebd-d5ab-5cb3-a620-52ae5dc76565', 'e73bea7c-80a8-50b2-b6ee-2c9f1f92bd05',
        '44c3b35a-bc1c-522d-a4cf-477969a2c043', '5b18a139-dca5-5b8a-a1ab-672789768a0e', 'e356d160-4c13-517b-8f76-d8e2abebeabe', '8bf91cec-22f0-5602-86cc-975dce578637',
        'e52a369c-76ea-5d5e-9f43-408c67ffff7f', '237082a4-6332-51fc-a409-2bf43b31fe63', '51a26d27-f75d-5265-8bd8-b82bec14757e']
#上面是各市場的uuid，有市場需要新增直接加在最後面即可,已關的市場記得刪掉
#目前記錄到大湳



driver = webdriver.Chrome("C:/Users/gtseng1/Desktop/chromedriver.exe")   #打開自動瀏覽器
driver.maximize_window()    #最大化視窗，不然可能遮到按鈕他會跑不動

today = datetime.date.today()    #查詢今天日期，以此來當作資料夾的名稱
path = 'C:/Users/gtseng1/Downloads/' + str(today)    #預計要建立的資料夾路徑
if not os.path.isdir(path):    #如果沒有同名稱資料夾就建立
    os.makedirs(path)


for i in uuid:    #每個市場跑回圈
    url = 'https://restaurant.uberinternal.com/manager/menumaker/' + i + '/overview'     #市場的菜單連結
    driver.get(url)    #輸入網址，下面的程式碼是等下載的那個按鈕跑出來
    wait1 = WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/main/div/div[2]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/button')))
    find_button1 = driver.find_elements(By.XPATH, '/html/body/div/div/div[1]/main/div/div[2]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/button')
    print(find_button1)        #檢查用
    print('這是按鈕')
    print(i)
    find_button1[0].click()    #按鈕加載完就點擊

    wait2 = WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[1]/div[1]/button')))
    find_button2 = driver.find_elements(By.XPATH, '/html/body/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[1]/div[1]/button')    #再等他第二個按鈕跑出來
    find_button2[0].click()    #按鈕加載完就點擊
    sleep(5)    #等他菜單下載

    list_of_files = glob.glob('C:/Users/gtseng1/Downloads/*.xlsx')    #找下載資料夾裡的所有xlsx檔案
    latest_file = max(list_of_files, key=os.path.getctime)    #找裡面最新的那個
    shutil.move(latest_file, path)    #移動到日期的那個資料夾裡

sleep(600)





#沒有套迴圈的原程式
'''
url = 'https://restaurant.uberinternal.com/manager/menumaker/6b0d8076-2a6d-4448-8236-5c1c2e2cd974/overview'
driver.get(url)
wait1 = WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.ID, 'bui11__anchor')))
find_button1 = driver.find_elements(By.ID, 'bui11__anchor')
find_button1[0].click()

wait2 = WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[1]/div[1]/button')))
find_button2 = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[1]/div[1]/button')
find_button2[0].click()

list_of_files = glob.glob('C:/Users/gtseng1/Downloads/*.xlsx')
latest_file = max(list_of_files, key=os.path.getctime)


shutil.move(latest_file, path)
'''



