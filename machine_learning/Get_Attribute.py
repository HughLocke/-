#获取属性集
import requests
import os
import json
import pandas as pd
import numpy as np
import re
import tkinter
import redis

def Download(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "cookie": "trace_session_id=01780BAA-32DA-827A-E000-41305E6C57CE; _ntes_nuid=f8bbb12f899eca4343358658c9721c36; fingerprint=yrofufde0xoxgt4t; _ns=NS1.2.321854753.1581393458; mail_psc_fingerprint=1e5649e90792ce129b19267dd959b41a; usertrack=ezq0ZV6SjBgg014nDD4QAg==; NTES_CMT_USER_INFO=304785478%7C%E6%9C%89%E6%80%81%E5%BA%A6%E7%BD%91%E5%8F%8B0iaGx6%7Chttp%3A%2F%2Fcms-bucket.nosdn.127.net%2F2018%2F08%2F13%2F078ea9f65d954410b62a52ac773875a1.jpeg%7Cfalse%7CaHVnaF9sb2NrZUAxNjMuY29t; mp_MA-9ADA-91BF1A6C9E06_hubble=%7B%22sessionReferrer%22%3A%20%22https%3A%2F%2Fcampus.163.com%2Fapp%2Fdetail%2Findex%3FprojectId%3D27%26id%3D696%22%2C%22updatedTime%22%3A%201598546026572%2C%22sessionStartTime%22%3A%201598545861987%2C%22sendNumClass%22%3A%20%7B%22allNum%22%3A%208%2C%22errSendNum%22%3A%200%7D%2C%22deviceUdid%22%3A%20%22f29c780f-ea64-4c5f-bf8c-a7c128c91f04%22%2C%22persistedTime%22%3A%201583030395897%2C%22LASTEVENT%22%3A%20%7B%22eventId%22%3A%20%22da_screen%22%2C%22time%22%3A%201598546026572%7D%2C%22sessionUuid%22%3A%20%225825e994-5e87-493b-8b79-c2b06add2e50%22%7D; nts_mail_user=hugh_locke@163.com:-1:1; _ntes_nnid=f8bbb12f899eca4343358658c9721c36,1614089800954; _external_mark=direct; trace_session_id=01780714-16E8-4701-BE5B-4070F38E9931; back_url=https%3A%2F%2Fstzb.cbg.163.com%2Fcgi%2Fmweb%2Fuser%3F_mobile_tips%3D1; NTES_YD_PASSPORT=HmJJAfRME2dbElPo.xMzuJh5YU4j8j5If5r174t8OWkSUGQvUZBPoCjNpXyKKnjV4_wgydHtadcVIBgKL9toZtwJNOLSKnXK0kiQUxRlJuNEngbmVF2CIi8HdYsvn6Ul7Jb0xfoaGW2vRnrbI63fMJkc8RTwcfMeensXQQTks5_pp6070E6s81Z5HiwSELpuUdJH30tHMFNkYsYmgCw2bNvM6; P_INFO=18458390734|1615026496|1|cbg|00&99|null&null&null#zhj&330100#10#0|&0|null|18458390734; urs_share_login_token=yd.2b0c6d51108848339@163.com$5b566ac23e5d95504ad2f3efca91b5cc; is_log_active_stat=1; SID=4f7bead2-d7c1-40bc-9498-d9144c81cc10; NTES_YD_SESS=NWYx_Hgz2SbFe6YRnUcY6sHlfdKU9WxyHa48hrJdkJ7S_q13_H8IY.T4dzW99LTOiBNvWZpQcZX4tbRjsM9fgQJPrAwyOu_YiuSyW.RNTCQSjSVSNfsccAF4xv0PxXMDCXADZ2.XgZRknJ2jFVSYo2awJDJYbrPf3u6RGRrRKaBd3u784s0Uli7jo2SQ3cloKCUZZgZGBx51EimOHfBJosHp1gF5jZn6a; S_INFO=1615108049|1|0&60##|18458390734; sid=SrFFwsaX2EuRrKaqjvJ8L0u-6l-Ig1FxSB2mxRzj; login_id=8afc0e02-7f24-11eb-8f98-9958204ce9f5"
    }
    return requests.get(url, headers=head, timeout=60)

AttributeIndex = {}
AttributeNum = 0
#属性集的初始化
def AttributeInit():
    global AttributeNum
    AttributeNum = -1
    AttributeNum += 1;AttributeIndex['yuan_bao'] = int(AttributeNum)  #玉府
    AttributeNum += 1;AttributeIndex['jiang_ling'] = int(AttributeNum) #将令
    AttributeNum += 1;AttributeIndex['hufu'] = int(AttributeNum) #虎符
    AttributeNum += 1;AttributeIndex['honor'] = int(AttributeNum) #荣誉

#对属性集的完善
hero_id_state = {1:"弓",2:"步",3:"骑"}
hero_id_country = {1:"汉",2:"魏",3:"蜀",4:"吴",5:"群"}
#获取武将组
def Attribute_Hero(Account_info):
    global AttributeNum
    Hero_List = re.findall("{\\\"hit_range[^}]*}", Account_info)
    for Hero in Hero_List:
        print(Hero)
        heroJson = json.loads(Hero)
        #print(heroJson["hit_range"])
        '''quality = re.search("\\\"quality\\\":([^,]*)", Hero).group(1)
        if int(quality) != 5: continue #不考虑非五星武将
        name = re.search("\\\"name\\\":([^,]*)", Hero).group(1)
        name = name.strip(' ').strip('"')
        name = name.encode('utf-8').decode('unicode_escape') #姓名
        hero_state = re.search("\\\"hero_type\\\":([^,]*)", Hero).group(1) #步骑弓状态
        hero_state = hero_id_state[int(hero_state)]
        hero_country = re.search("\\\"country\\\":([^,]*)", Hero).group(1)  #国家
        hero_country = hero_id_country[int(hero_country)]
        if name != '侍卫': #侍卫都一样,其他的需要区分
            name = hero_country + hero_state + name #综合状态的姓名,赵云->蜀步赵云
        if name not in AttributeIndex:
            AttributeNum += 1
            AttributeIndex[name] = AttributeNum
        '''
#获取技能组
def Attribute_Skill(Account_info):
    global AttributeNum
    Skill_List = re.findall("{\\\"skill_type[^}]*}", Account_info)
    for Skill in Skill_List:
        name = re.search("\\\"name\\\":([^,]*)", Skill).group(1)
        name = name.strip(' ').strip('"')
        name = name.encode('utf-8').decode('unicode_escape')  # 姓名
        #print(name)
        if name not in AttributeIndex:
            AttributeNum += 1
            AttributeIndex[name] = AttributeNum

def AttributeSolve(Account_info):
    Account_info = Account_info["equip"]["equip_desc"]
    Attribute_Hero(Account_info)
    Attribute_Skill(Account_info)


#通过将每个id发送给服务器的方式 获取每个账号的详细信息
def PostAccount(pageurl,Accountid,Accounturl):
    head = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
        "Referer": Accounturl
    }
    datas = {
        "serverid":"1",
        "ordersn":Accountid,
        "view_loc":"equip_list",
    }
    datas["ordersn"] = Accountid
    html_post = requests.post(pageurl,data = datas,headers = head)
    if html_post:
        AttributeSolve(json.loads(html_post.text))

#取出每页的账号id并处理
def Pagework(page_info):
    #print('这页共有%d个武将' % len(page_info['result']))
    if 'result' not in page_info:
        print ("ERROR: result not in page_info")
        print(page_info.keys())
        return
    for tmp in page_info["result"]:
        id = tmp['game_ordersn']
        Accounturl = "https://stzb.cbg.163.com/cgi/mweb/equip/1/%(name)s?view_loc=equip_list" % {'name':id}
        pageurl = "https://stzb.cbg.163.com/cgi/api/get_equip_detail"
        PostAccount(pageurl,id,Accounturl)

def startload(pagestart,pageend):
    for now_page in range(int(pagestart), int(pageend) + 1):
        url = "https://stzb.cbg.163.com/cgi/api/query?anonymous_query=1&page=" + str(
            now_page)
        print(url)
        html = Download(url)
      #  if (html):
         #   Pagework(json.loads(html.text))


#进入ios账号的主页并且动态获取每个页面包含账号的id
def main():
    #pagestart = int(input('输入你想从哪页开始找'))
    #pageend = int(input('输入你想到哪页结束'))
    pagestart = 1
    pageend = 10
    conn = redis.Redis(host="127.0.0.1", port=6379, password="")
    AttributeInit()
    for now_page in range(pagestart,pageend + 1):
        url = "https://stzb.cbg.163.com/cgi/api/query?view_loc=equip_list&platform_type=1&order_by=selling_time%20DESC&page=" + str(now_page)
        html = Download(url)
        print('当前正在第%d页寻找' % now_page)
        if(html):
            Pagework(json.loads(html.text))
    f = open('../data/Attribute_Set.txt', 'w')
    for key in AttributeIndex: #输出获取到的属性集
        f.write(str(key) + '\t' + str(AttributeIndex[key]) + '\n')
    f.close()

if __name__ == '__main__':
    main()

