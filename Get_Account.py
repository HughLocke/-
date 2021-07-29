import requests
import json
import pandas as pd
#定义账号数据类型
PATH = "data/Account_tmp.txt"
ACCOUNT_DATA_PATH = "account_data/"
def Download(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    headers['cookie'] = 'is_log_active_stat=1; _external_mark=direct; fingerprint=f1xkp8g6hhj6craj; trace_session_id=017AF27F-A083-70FF-F96E-D3903475E0D5; back_url=/cgi/mweb/pl/role?search_type=role&view_loc=equip_list; NTES_YD_SESS=5NefcEClr_5K.C7E20ALKuIEL60LcTL9_tWdZv3qvfHUbX4tbOxW2SeDYj8JJ_evMh5f8VoNCV.Dwlq7rsJi1NZypmkBv6b2M60B8Sq5euNzw74xjmrsBp.TtqUbNlugqqT8RhKyXLl_naVUgcBgfshPi0igFdHh4A.6cZBYEF86u5Y8lN4o42pPpW8UM0Auw_m_CJ6xrFBIE53cBPcKp06HxWdt81nIf; NTES_YD_PASSPORT=YN_4q0yTQBSyxkj0qQUzJc7PxhJp4rBv6Yixf0o5bCwFhziQhoRng7uMVTUmmBu3kxDtUOY4.Oj3LRtm8r4go4DpM28ImBTmWA5ihlFcpPMTjHK8KYBnZQSIZybIdIyPD0u44.dDrJQ64CPy69DBSQlm8InOMZJ6ovABDFsPIOEbBCjlkwKr.BmnNrykNIarM_WstK4gPYive5VX4YYvT8f9y; S_INFO=1627566121|0|3&80##|18458390734; P_INFO=18458390734|1627566121|1|cbg|00&99|null&null&null#zhj&330100#10#0|&0|null|18458390734; sid=EN2gse50AI5EH_dXFE0H1skz15fi6egT18cuPq9G; urs_share_login_token=yd.2b0c6d51108848339@163.com$5b566ac23e5d95504ad2f3efca91b5cc; login_id=c0b553d7-f072-11eb-a426-48652e1e6e4e'

    return requests.get(url, headers=headers, timeout=60)

#通过将每个id发送给服务器的方式 获取每个账号的详细信息
idMapping = {}
def PostAccount(pageurl,Accountid,Accounturl):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Referer": Accounturl
    }
    datas = {
        "serverid":"1",
        "ordersn":Accountid,
        "view_loc":"equip_list",
    }
    datas["ordersn"] = Accountid
    #print(datas["ordersn"])
    html_post = requests.post(pageurl,data = datas,headers = head)
    if html_post:
        if Accountid in idMapping:
            idMapping[Accountid] = True
            print("exist")
        else:
            path = ACCOUNT_DATA_PATH + Accountid + ".txt"
            f = open(path, 'w')
            f.write(html_post.text)
            f.close()

#取出每页的账号id并处理
def Pagework(page_info):
    #print('这页共有%d个武将' % len(page_info['result']))
    for tmp in page_info['result']:
        id = tmp['game_ordersn']
        Accounturl = "https://stzb.cbg.163.com/cgi/mweb/equip/1/%(name)s?view_loc=equip_list" % {'name':id}
        pageurl = "https://stzb.cbg.163.com/cgi/api/get_equip_detail"
        PostAccount(pageurl,id,Accounturl)

#进入ios账号的主页并且动态获取每个页面包含账号的id
def main():
  #  pagestart = int(input('输入你想从哪页开始找'))
    #pageend = int(input('输入你想到哪页结束'))
    pagestart = 1
    pageend = 150
    for now_page in range(pagestart,pageend + 1):
        url = "https://stzb.cbg.163.com/cgi/api/query?view_loc=equip_list&platform_type=1&order_by=selling_time%20DESC&page=" + str(now_page)
        html = Download(url)
        #print (html.text)
        print('当前正在第%d页寻找' % now_page)
        if(html):
            Pagework(json.loads(html.text))


if __name__ == '__main__':
    main()

