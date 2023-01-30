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
#elite-advice-370803-1d67b30a02f1.json
#coral-silicon-357507-03bb260c269b.json
survey_url = 'https://docs.google.com/spreadsheets/d/1SMbiVpGYMaM9H5Hu0gWJbAvUGRdnHx3ySDioe0OVzyM/edit?usp=sharing'    #連到自己的紀錄表單
backup_url = 'https://docs.google.com/spreadsheets/d/15ZCQzmNq3UIyEEJR7Jdpvym4UlIFeSYvne-yp90eGko/edit?usp=sharing'    #連到備份表單


sht = gc.open_by_url(survey_url)  #打開紀錄表單
wks = sht[0]             #第一個sheet
other_payments = sht[1]  #第二個sheet是補款紀錄
other_payments.clear()   #清除之前的補款紀錄
total_list = wks.get_values('A2','F48')  #將第一個sheet的A欄到F欄的參數存成list 等等跑網頁會用到
print(total_list)                        #檢查用 看有沒有空list出現




driver = webdriver.Chrome("C:/Users/gtseng1/Desktop/chromedriver.exe")   #打開自動瀏覽器


for i in range(len(total_list)):  #在70秒內成功登入後開始自動跑list迴圈  就可以放著ㄌ
    url = "https://restaurant.uberinternal.com/manager/payments?restaurantUUID=" + total_list[i][5] + '&start=' + total_list[i][3] + '&end=' + total_list[i][4] + '&rangeType=1'
    driver.get(url)
    wait = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[3]/div[3]/div[2]')))

    #把原先沒有顯示的明細點開
    find_tag_li = driver.find_elements(By.TAG_NAME, "li")  #找到所有網頁tag是li的東西(會存成list形式)
    trans_list = []                                        #等等存放網頁元素轉文字的地方
    for element in find_tag_li:                            #元素轉換成文字過程並加進trans_list
        trans_list.append(element.text)

    for text in trans_list:                          #從trans_list逐個尋找找到當中最後一排文字並index出來位置
        if '總金額' in text:
            stop_position = trans_list.index(text)
            break                                    #找到總金額的位置後跳出迴圈
        else:
            pass
    for k in range(stop_position):                   #透過總金額的位置按出原先隱藏的明細
        find_tag_li[k].click()


    all_data = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[3]/div[3]/div[2]')  #把大表全部抄下來
    all_data_list = all_data.text.split('\n')        #透過split去掉原先的空行間格並轉成list
    print(all_data_list)

    handling_fee = 0               #有些電匯補款不只一項
    Promotions_on_items = 0
    Ad_spends = 0
    for data in all_data_list:     #開始逐項檢查all_data_list
        temp_list = []
        if '商品優惠' in data:       #如果文字裡面有商品優惠則取代原先0元
            Promotions_on_items += float(all_data_list[all_data_list.index(data) + 1][2:])
        elif '廣告費用' in data:     #以此類推
            Ad_spends += float(all_data_list[all_data_list.index(data) + 1][2:])
        elif '匯款手續費' in data:   #匯款手續費有多筆因此要加總起來
            handling_fee += float(all_data_list[all_data_list.index(data) + 1][1:])
            all_data_list.remove(data)
        elif '總金額' in data:
            wks.update_value('G' + str(i + 2), all_data_list[all_data_list.index(data) + 1])
        elif '補款' in data:        #有補款的則記錄在第二頁資料表
            replenishment = all_data_list[all_data_list.index(data)].replace('）', '')      #把前面某某市場刪掉的處理
            temp_list.append(total_list[i][0])
            try:
                temp_list.append(replenishment[replenishment.index('_') + 1:])
            except ValueError:
                try:
                    temp_list.append(replenishment[replenishment.index('-') + 1:])
                except ValueError:
                    temp_list.append(replenishment)
            temp_list.append(all_data_list[all_data_list.index(data)+1])
            other_payments.append_table(values = temp_list)
    wks.update_value('H' + str(i + 2), Promotions_on_items)  #商品優惠寫入資料表
    wks.update_value('I' + str(i + 2), Ad_spends)            #廣告花費寫入資料表
    wks.update_value('J' + str(i + 2), handling_fee)         #加總完畢的匯款手續費寫入資料表
    wks.update_value('K' + str(i + 2), url)                  #網址寫入資料表

print('對帳完成!')


#備份作業
today = datetime.date.today()                           #查詢今天日期
num = today.isoweekday()                                #今天星期幾
last_sunday = today - datetime.timedelta(days = num)    #找出上禮拜天

backup_sht = gc.open_by_url(backup_url)                 #打開備份表單
backup_sht_list = backup_sht.worksheets()               #找出各個sheet的名稱
print(backup_sht_list)
check_list = []
for i in backup_sht_list:
    check_list.append(str(i)[12:22])
print(check_list)


if str(last_sunday) in check_list:                      #如果上禮拜天不在裡面就新建備份sheet
    pass
else:
    res = backup_sht.add_worksheet(str(last_sunday),  index = 0)    #新建名稱為上禮拜天
    res2 = backup_sht.add_worksheet(str(last_sunday) + '補款',  index = 1)
    backup_wks = backup_sht.worksheet_by_title(str(last_sunday))
    total_list2 = wks.get_values('A1','K45')            #將已更新好的資料全部放到備份sheet裡
    total_list3 = other_payments.get_values('A1','C1000')
    backup_wks.append_table(values = total_list2)
    backup_other_payments = backup_sht.worksheet_by_title(str(last_sunday) + '補款')
    backup_other_payments.append_table(values = total_list3)

print('備份完成')


sleep(600)


#沒有套迴圈的原程式
'''
#把原先沒有顯示的明細點開
find_tag_li = driver.find_elements(By.TAG_NAME, "li")  #找到所有網頁tag是li的東西(會存成list形式)
trans_list = []                                         #等等存放網頁元素轉文字的地方

for i in find_tag_li:                                  #元素轉換成文字過程並加進trans_list
    trans_list.append(i.text)

for i in trans_list:                          #從trans_list逐個尋找找到當中最後一排文字並index出來位置
    if '總金額' in i:
        stop_position = trans_list.index(i)
        break                                 #找到總金額的位置後跳出迴圈
    else:
        pass

for i in range(stop_position):                #透過總金額的位置按出原先隱藏的明細
    find_tag_li[i].click()

all_data = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[1]/div[2]/div[2]/div[2]/div/div[5]/div[2]')  #把大表全部抄下來
all_data_list = all_data.text.split('\n')   #透過split去掉原先的空行間格並轉成list
print(all_data_list)


handling_fee = 0
for i in all_data_list:
    temp_list = []
    if '商品優惠' in i:
        wks.update_value('H2', all_data_list[all_data_list.index(i) + 1])
    elif '廣告費用' in i:
        wks.update_value('I2', all_data_list[all_data_list.index(i) + 1])
    elif '匯款手續費' in i:
        handling_fee += int(all_data_list[all_data_list.index(i) + 1][1:])
    elif '總金額' in i:
        wks.update_value('G2', all_data_list[all_data_list.index(i) + 1])
    elif '補款' in i:
        temp_list.append(all_data_list[all_data_list.index(i)])
        temp_list.append(all_data_list[all_data_list.index(i)+1])
        other_payments.append_table(values = temp_list)

wks.update_value('J2', handling_fee)
        
'''



