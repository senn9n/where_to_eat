import random
import yaml
import requests
import json


def read_food(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fs = yaml.safe_load(f.read())
    return fs


def select_where(dc):
    dc = list(dc)
    where = random.choice(dc)
    return where


def filter_foods(dc):
    result_dc = {k: v for k, v in dc.items() if v == 0}
    return result_dc


def filter_foods_before_today(dc):
    result_dc = {k: v for k, v in dc.items() if v != 0}
    return result_dc


def value_plus_one(dc1, dc2):
    for f in list(dc1):
        dc2[f] += 1


def rewrite_times(dc, filename):
    n = 6  # 保留n-1天记录
    d = {k: v for k, v in dc.items() if v >= n}
    if d:
        for i in range(len(d)):
            dc[list(d)[i]] = 0
    with open(filename, 'w', encoding='utf8') as f:
        yaml.dump(dc, f, allow_unicode=True)


def str_clean(dc):
    dc = {k: v for k, v in dc.items() if not v >= 6}
    sd = sorted(dc.items(), key=lambda x: x[1])
    s = str(sd).translate(str.maketrans('()', '（）', "[]'")).replace('）,', '）\n                   ')
    return s


def send_dd(info1, info2):
    url = ' '
    headers = {"Content-Type": "application/json ;charset=utf-8 "}
    data = {"msgtype": "text",
            "text": {"content": "今天去恰：{} \n最近恰了：{}".format(info1, info2)},
            "at": {
                "isAtAll": False
            }
            }
    r = requests.post(url, json.dumps(data), headers=headers)
    print(r.content)
    # b'{"errcode":0,"errmsg":"ok"}'


if __name__ == "__main__":
    foods = read_food('food.YAML')
    foods_filter = filter_foods(foods)
    foods_filter_bt = filter_foods_before_today(foods)
    value_plus_one(foods_filter_bt, foods)
    where_today = select_where(foods_filter)
    foods[where_today] += 1
    rewrite_times(foods, 'food.YAML')
    s1 = where_today
    s2 = str_clean(foods_filter_bt)
    send_dd(s1, s2)
    print("今天去恰：{} \n最近恰了：{}".format(s1, s2))
