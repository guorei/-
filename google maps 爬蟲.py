import googlemaps
import pandas as pd
import time
import requests, json, csv
from urllib.parse import urlencode




api_key = 'AIzaSyDbX4S6KBFoxfWkjr0jRSFvDqn3YirunAE'
gmaps = googlemaps.Client(key = 'AIzaSyDbX4S6KBFoxfWkjr0jRSFvDqn3YirunAE')


#在這裡加想要搜尋的行政區
#距離為方圓幾公尺
cities = ['臺北市', '台北市淡水區', '台北市信義區',
          '新北市永和區', '新北市中和區', '新北市樹林區', '新北市板橋區', '新北市土城區', '新北市三重區', '新北市蘆洲區', '新北市新店區', '新北市新莊區', '新北市汐止區', 
          '臺中市', '臺中市豐原區',
          '台南東興公園', '台南市安平區', '台南市北區',
          '高雄市', '高雄市三民區', '高雄市左營區']
rad = [5000, 3000, 3000,
       3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 5000,
       10000, 5000,
       10000, 5000, 5000,
       10000, 5000, 5000]


ids = []    #收集搜尋到的商家id list


#依照想要查找的行政區開始搜尋商店
for i in range(len(cities)):
    results = []    #收集結果list
    geocode_result = gmaps.geocode(cities[i])
    loc = geocode_result[0]['geometry']['location']    #用geocode轉換成經緯度來搜尋
    query_result = gmaps.places_nearby(keyword = "市場", location = loc, radius = rad[i])    #搜尋
    results.extend(query_result['results'])       #把搜尋結果加到結果list
    while query_result.get('next_page_token'):    #如果有超過20筆資料就繼續尋找收集
        time.sleep(2)
        query_result = gmaps.places_nearby(page_token = query_result['next_page_token'])
        results.extend(query_result['results'])
    print("找到以" + cities[i] + "為中心半徑" + str(rad[i]) +"公尺的市場數量: " + str(len(results)))
    for place in results:    #收集餐廳id
        ids.append(place['place_id'])


stores_info = []
#去除重複id
ids = list(set(ids)) 
for id in ids:
    stores_info.append(gmaps.place(place_id = id, language = 'zh-TW')['result'])



#根據收集到的餐廳id進一步收集詳細資料
for i in stores_info:
    review = ''
    opening_hours = ''
    try:     #把營業時間整理成句子
        for k in i['opening_hours']['weekday_text']:
            opening_hours += k + ','
        i['opening_hours'] = opening_hours
    except KeyError:
        pass
    try:     #把顧客評論整理成句子
        for z in i['reviews']:
            review += z['relative_time_description'] + '-' + z['author_name'] + '：' + z['text'] + '\n'
        i['reviews'] = review
    except KeyError:
        pass
    try:     #整理縣市與行政區
        for x in i['address_components']:
            if x['types'] == ['administrative_area_level_3', 'political']:     #看有沒有行政區
                district = x['long_name']
            elif x['types'] == ['administrative_area_level_1', 'political']:   #看有沒有縣市分層
                municipal = x['long_name']
        i['address_components'] = municipal + district
    except KeyError:
        pass

output = pd.DataFrame.from_dict(stores_info)   #將收集到的資訊整理近pandas
data = output[['name', 'address_components', 'vicinity', 'opening_hours', 'formatted_phone_number', 'rating', 'user_ratings_total', 'reviews', 'url', 'website']]


#存成csv檔
data.to_csv("C:/Users/gtseng1/Desktop/output.csv", index = False)


'''
#寫入csv檔案
with open('C:/Users/gtseng1/Desktop/gongguan_new_details.csv', 'w', newline='', errors = 'ignore') as csvfile:
    writer = csv.writer(csvfile)
    for i in stores_info:
        writer.writerow(i)
    csvfile.close()
'''




