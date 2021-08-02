import re
import os
import json
ACCOUNT_DATA_PATH = "account_data/"

hero_id_state = {1:"弓",2:"步",3:"骑"}
hero_id_country = {1:"汉",2:"魏",3:"蜀",4:"吴",5:"群"}
class Account:
    id = "0"
    key_hero_num = 0 #核心数量
    score = 0        #分数
    price = 0
    name = ""
    key_hero = set() #核心
    team_value = {}   #队伍分
    team_exist = []  # 队伍数量
    team_rank = []    #红度高到低排序
    arms = 0
    def __init__(self):
        self.name = ""
        self.key_hero_num = 0
        self.score = 0
        self.price = 0
        self.key_hero = set()
        self.team_exist = []
        self.team_value = {}
        self.team_rank = []
        self.arms = 0
        for team_name in team_dict.keys():
            self.team_value[team_name] = 0
        pass

    def __lt__(self,other):
        #return sum(self.team_rank[:3]) > sum(other.team_rank[:3]) #前三队红度和
        return self.score > other.score  #综合分最高
        #return self.key_hero_num > other.key_hero_num #关键武将个数最多
        #return len(self.team_exist) > len(other.team_exist)
        #return self.arms > other.arms
Account_List = []
hero_score_dict = {"蜀步刘备":6,"汉弓张机":4,"吴弓吕蒙":6,"蜀骑关羽":3,"魏骑曹操":4,"蜀骑马岱":6,"吴步陆抗":2,"魏骑张辽":1,"蜀步关银屏":1,"蜀步魏延":2,
                        "群弓吕布":4,"群骑马超":5,"蜀弓诸葛亮":3,"蜀骑徐庶":2,"吴步陆逊":2,"吴弓孙权":2, "吴弓周瑜":1,"蜀步赵云":1,"魏弓王异":3, "吴步周泰": 2}
#hero_score_dict = {"蜀步刘备":6,"汉弓张机":3,"吴弓吕蒙":6,"蜀骑关羽":0,"魏骑曹操":6,"蜀骑马岱":6,"吴步陆抗":0,"魏骑张辽":0,"蜀步关银屏":0,"蜀步魏延":0,
              #          "群弓吕布":6,"群骑马超":6,"蜀弓诸葛亮":0,"蜀骑徐庶":0,"吴步陆逊":0,"吴弓孙权":0, "吴弓周瑜":0,"蜀步赵云":0,"魏弓王异":0, "吴步周泰": 0}
#hero_score_dict = {"蜀步刘备":1,"汉弓张机":0,"吴弓吕蒙":1,"蜀骑关羽":0,"魏骑曹操":0,"蜀骑马岱":2,"吴步陆抗":0,"魏骑张辽":0,"蜀步关银屏":0,"蜀步魏延":0,
 #                      "群弓吕布":0,"群骑马超":1,"蜀弓诸葛亮":0,"蜀骑徐庶":0,"吴步陆逊":0,"吴弓孙权":0, "吴弓周瑜":0,"蜀步赵云":0,"魏弓王异":0, "吴步周泰": 0}

key_hero_dict = ("蜀步刘备","汉弓张机","吴弓吕蒙","蜀骑关羽","魏骑曹操","蜀骑马岱","群弓吕布","群骑马超","蜀弓诸葛亮","吴弓孙权")

team_dict = {
             #"蜀骑": ["蜀骑关羽", "蜀骑马岱", "蜀骑徐庶"],
             #"嘟嘟": ["吴步陆逊", "吴弓吕蒙", "吴弓周瑜"],
             #"菜刀": ["群骑马超", "魏骑曹操", "魏骑张辽"],
             #"魏延菜刀": ["群骑马超", "魏骑曹操", "蜀步魏延"],
             #"蜀步": ["蜀步刘备", "蜀步赵云", "蜀步关银屏"],
             #"鬼吕流氓": ["群弓吕布", "汉弓张机", "吴弓孙权"],
             #"法刀": ["汉弓灵帝", "吴弓吕蒙", "汉弓张机"],
             #"变种蜀骑": ["蜀骑关羽", "蜀骑马岱", "群骑张绣"],
             #"张宁核弹": ["群步张宁", "吴弓吕蒙", "汉弓朱儁"],
             #"关银屏流氓": ["蜀步关银屏", "汉弓张机", "吴弓孙权"],
             #"魏智": ["魏骑荀彧", "魏骑郭嘉", "魏弓贾诩"],
	     #"狗法官": ["魏骑荀彧", "蜀骑法正", "蜀骑关羽"],
	     #"王异法刀": ["魏弓王异", "吴弓吕蒙", "魏骑曹操"],
	     #"周泰开荒": ["吴步周泰", "群弓甄洛", "吴步陆抗"],
             #"周泰刘备": ["吴步周泰", "蜀步刘备", "吴步陆抗"],
             #"周泰张机": ["吴步周泰", "汉弓张机", "吴步陆抗"],
             #"马超开荒": ["群骑马超", "群弓甄洛", "吴步陆抗"],
             #"马超魏延": ["群骑马超", "群弓甄洛", "蜀步魏延"],
             "马岱": ["蜀骑马岱"],
             "刘备": ["蜀步刘备"],
             "吕蒙": ["吴弓吕蒙"],
             "马超": ["群骑马超"]
}
hero_team_map = {}
team_map = {}
team_color = {}

def init():
    global hero_team_map
    for team_name in team_dict.keys():
        team = team_dict[team_name]
        for hero in team:
            hero_team_map[hero].append(team_name)
    for hero in hero_team_map.keys():
        team_list = hero_team_map[hero]
        for team in team_list:
            for team2 in team_list:
                if(team == team2):
                    continue
                team_map[team].append(team2)
    pass
def general_value(file_name, Account_info):
    global Account_List
    info = json.loads(Account_info)
    info = info["equip"]
    try:
   #     if int(info["pass_fair_show"]) == 1: #公示期
    #        return
 #       print(info["pass_fair_show"])
         a = 1
    except:
  #      print(info)
        return
    account = Account()
    account.price = int(info["price"]) / 100
    if(account.price > 20000): #账号价格阈值, 可根据需要改动
        return

    info = info["equip_desc"]
    info = json.loads(info)
    account.id = file_name
    try:
        account.name = info["name"]
        int(info["tenure"]["yue_ka_endtime"])
        #account.price -= int(info["tenure"]["yue_ka_endtime"])
       # account.price -= int(info["tenure"]["jiang_ling"]) / 20
       # account.price -= int(info["tenure"]["bind_yuan_bao"]) / 10
       # account.price -= int(info["tenure"]["hufu"]) / 20
        #account.price -= int(info["tenure"]["yuan_bao"] - info["tenure"]["bind_yuan_bao"]) / 20
        #account.price -= int(info["tenure"]["honor"]) / 10
       # account.price -= int(info["material"]["chi_zhu_shan_tie"]['value']) * 10
       # account.price -= int(info["material"]["xiao_ye_zi_tan"]['value']) * 10
    except: #武器
   #     print("wuqi")
        return
    Hero_List = info["card"]
    add_value = {}
    team_value = {}
    for Hero in Hero_List:
        quality = Hero["quality"]
        if int(quality) != 5: continue  # 不考虑非五星武将
        name = Hero["name"]
        # name = name.encode('utf-8').decode('unicode_escape')  # 姓名
        hero_state = Hero["hero_type"]  # 步骑弓状态
        hero_state = hero_id_state[int(hero_state)]
        hero_country = Hero["country"]  # 国家
        hero_country = hero_id_country[int(hero_country)]
        advance_num = Hero["advance_num"]  # 进阶状态
        name = hero_country + hero_state + name  # 综合状态的姓名,赵云->蜀步赵云

        if name not in add_value:
            add_value[name] = 0
        # print(name)
        addcount = min((int(advance_num) + 1), 6 - int(add_value[name]))
        add_value[name] += addcount
        #print(name)
        if name in key_hero_dict:
            account.key_hero_num += addcount
            account.key_hero.add(name)
            # print(name,addcount)
        if (name in hero_score_dict):
            account.score += hero_score_dict[name] * addcount
    team_merge = {}
    for team_name in team_dict.keys():
        team_list = team_dict[team_name]
        for hero in team_list:
            if hero in add_value:
                if team_name not in account.team_value:
                    account.team_value[team_name] = 0
                if team_name not in team_merge:
                    team_merge[team_name] = 0
                account.team_value[team_name] += add_value[hero]
                team_merge[team_name] |= (1 << team_list.index(hero))
    for team in team_merge.keys():
        if(team_merge[team] == ((1 << (len(team_dict[team]))) - 1)):
            account.team_exist.append(team)
    account.team_rank = list(account.team_value.values())
    account.team_rank.sort(reverse = True)
   # if len(account.key_hero) != len(key_hero_dict):
    #    return
    Skill_List = info["skill"]
    for Skill in Skill_List:
        name = Skill["name"]

    Gear_List = info["gear"]
    for Gear in Gear_List:
        name = Gear["name"]
        level_type = Gear["level_type"]
        phase = Gear["phase"]
        advance = Gear["advance"]
        if phase < 3: continue
        account.arms += 1
        # print(name, level_type, phase, advance)
      #  account.score += 1
    #print(account.id, account.price, account.score)
    account.score = int(account.score)
    Account_List.append(account)


if __name__ == '__main__':
    cnt = 0
    for root, dirs, files in os.walk(ACCOUNT_DATA_PATH):
        for f in files:
            with open(os.path.join(root,f)) as fp:
               # print(f)
                content = fp.read();
                general_value(f[:-4], content)
                cnt += 1
          #  break

    Account_List.sort()
    print(len(Account_List))
    for i in range(0,100):
        url = "https://stzb.cbg.163.com/cgi/mweb/equip/1/%(name)s?view_loc=equip_list" % {'name': Account_List[i].id}
        print(url, "价格: ", Account_List[i].price, "综合分: ", Account_List[i].score, "关键武将数: ", Account_List[i].key_hero_num, "前三对红度和: ",sum(Account_List[i].team_rank[:3]) - 9, "三阶武器数量: ", Account_List[i].arms, "姓名: ", Account_List[i].name)
        for team_name in Account_List[i].team_exist:
            print(team_name,int(Account_List[i].team_value[team_name]) - len(team_dict[team_name]),end="红|")
        print()
        print("缺少", end=": ")
        for team_name in key_hero_dict:
            if team_name not in Account_List[i].key_hero:
                print(team_name, end = "|")
        print()
        for team_name in Account_List[i].team_value.keys():
            value = Account_List[i].team_value[team_name]
            #print(team_name,value)
    #general_value(value_text)
