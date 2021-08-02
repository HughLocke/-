import requests
import json
#定义账号数据类型
PATH = "data/Account_tmp.txt"
ACCOUNT_DATA_PATH = "account_data/"
def Download(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    headers['cookie'] = '_ntes_nnid=89ef3e2db241fb37b29a463549e0f476,1615190773728; _ntes_nuid=89ef3e2db241fb37b29a463549e0f476; mail_psc_fingerprint=0d8e3a6dd4aaeec8e099717228a7a83d; _ns=NS1.2.434194780.1621943082; NTES_SESS=BGTJKM.0x4fhPdGyr1DJlMUzJAgGtzLbSVke6aL.wm.Z15ST1ltocJY9Q3gUEbVAFJXen7fCuzfQyjsjITLTXaQ0x_GX8rqv_ZWwoJ3DjMUY_6VLSZTUu8BOCgCwjF.l6BUgXNObtSC64zzK5lDPIsp7IUA2Z2NRx2JwqmAEQ7aeouojyU100aY8vU1fl2EGqr6dvVmxu33vJ; S_INFO=1625706604|0|3&80##|hugh_locke; P_INFO=hugh_locke@163.com|1625706604|1|mail163|00&99|zhj&1625704659&carddav#zhj&330100#10#0#0|&0|mailmaster_ios|hugh_locke@163.com; nts_mail_user=undefined:-1:0; _external_mark=direct; fingerprint=fgcxkxu1ae5jdpxi; urs_share_login_token=hugh_locke@163.com$f12e1c653a6c2e6d25609927e6421566; trace_session_id=017AF5CE-DCB6-5671-8783-461C9820C6A7; is_log_active_stat=1; sid=MwRqwVyuur0alb6ykFHs_SbeDODp4zIhp1y76ifl; login_id=9b06199c-f11a-11eb-8b74-7712f9382753'
    headers['cookie'] = 'trace_session_id=017B0548-F851-08B4-F200-A06ED541C381; _ntes_nnid=89ef3e2db241fb37b29a463549e0f476,1615190773728; _ntes_nuid=89ef3e2db241fb37b29a463549e0f476; mail_psc_fingerprint=0d8e3a6dd4aaeec8e099717228a7a83d; _ns=NS1.2.434194780.1621943082; nts_mail_user=undefined:-1:0; _external_mark=direct; fingerprint=fgcxkxu1ae5jdpxi; trace_session_id=017AF5CE-DCB6-5671-8783-461C9820C6A7; back_url=https%3A%2F%2Fstzb.cbg.163.com%2Fcgi%2Fmweb%2Fuser%3F_mobile_tips%3D1; NTES_YD_PASSPORT=9ts9FYwDU8T6OIrfrv.Xymhto3sbCHMol9o6pzKgPRYWIBoZIK0.mFq3AxSiieqE26vdSs9ObshEj0diuwOmKOvk3JuciexiCfgoIyWUka3xhMQuQ9e.DZlcDTPc5cTavzqOOb5vw4Z_uFT4cvc2NbHcQ.nAyt5Tz6Kh_eyrQ_SYywPeGKPCL1iSwVku02S9hRJ_6VTQjMCEGgA_O99rxup1T; P_INFO=18458390734|1627712352|1|cbg|00&99|null&null&null#zhj&330100#10#0|&0|null|18458390734; urs_share_login_token=yd.2b0c6d51108848339@163.com$5b566ac23e5d95504ad2f3efca91b5cc; is_log_active_stat=1; SID=877e4819-8060-4964-8e85-92e34ecbb073; NTES_YD_SESS=g_cp3o7GtZguegIcZD0BXSEmAIVhKCFFlxv6WkD9QDazP_OdPs6CJlGv9hu447Gr3IgpuAKVRAbvYyLFwt4oHVDTki2erXPJ3XzeulLgGqVBSI0urzNVUnf9AnHunNfxDbifAZlbHALQSDZF8mzJEZUiEyo.P21ihvO9AiEKukPTV.yYY6pz_PwnFqC7wLWSZ3dQr45FiB9jyw6iPvGub9AKOH81FAS.x; S_INFO=1627881271|1|0&60##|18458390734; sid=SjsEBv_2D6dPlmp7I3_NmTvVByLMtm0abgR0r0WG; login_id=85139bae-f350-11eb-93a7-d0de1e7f5a22'
    headers['cookie'] = 'trace_session_id=017B0548-F851-08B4-F200-A06ED541C381; _ntes_nnid=89ef3e2db241fb37b29a463549e0f476,1615190773728; _ntes_nuid=89ef3e2db241fb37b29a463549e0f476; mail_psc_fingerprint=0d8e3a6dd4aaeec8e099717228a7a83d; _ns=NS1.2.434194780.1621943082; nts_mail_user=undefined:-1:0; _external_mark=direct; fingerprint=fgcxkxu1ae5jdpxi; trace_session_id=017AF5CE-DCB6-5671-8783-461C9820C6A7; back_url=https%3A%2F%2Fstzb.cbg.163.com%2Fcgi%2Fmweb%2Fuser%3F_mobile_tips%3D1; NTES_YD_PASSPORT=9ts9FYwDU8T6OIrfrv.Xymhto3sbCHMol9o6pzKgPRYWIBoZIK0.mFq3AxSiieqE26vdSs9ObshEj0diuwOmKOvk3JuciexiCfgoIyWUka3xhMQuQ9e.DZlcDTPc5cTavzqOOb5vw4Z_uFT4cvc2NbHcQ.nAyt5Tz6Kh_eyrQ_SYywPeGKPCL1iSwVku02S9hRJ_6VTQjMCEGgA_O99rxup1T; P_INFO=18458390734|1627712352|1|cbg|00&99|null&null&null#zhj&330100#10#0|&0|null|18458390734; urs_share_login_token=yd.2b0c6d51108848339@163.com$5b566ac23e5d95504ad2f3efca91b5cc; usertrack=ezq0J2EHqWBSh3hCAxGwAg==; is_log_active_stat=1; SID=11a98636-c09c-4a2a-8b53-587f362a3ae3; NTES_YD_SESS=AKYqedrY5zzqANwAxbDglT9EaM4HKI1VPusqcYOgJOWyFjMNF3qU1P6sgeRHHh6tKGAwRv2DSv7s5azIdEHkiDO8Yp9xtLF1KLyxRPzA60DTbGlRtyZD.XrgvXiRXZruO7prv4P7ivzJbO4ICfy1Q4nTutVo5UM.OzAOZPJnxbnoSCSM5VI__7nIRuZ1tORIW8vdscLoYINKVF4UOmu5MQ22MiCmIvb_u; S_INFO=1627907528|1|0&60##|18458390734; sid=17l_6kFMVMBaFEi63EeNcRk3AitaUXWYhiCqbqoS; login_id=a7244617-f38d-11eb-97ba-9da5a01b6d8f'
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

