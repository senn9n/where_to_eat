import random
import yaml
from datetime import datetime
import requests
import json


def read_food(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fs = yaml.safe_load(f.read())
    return fs


def select_where(dc):
    dc = list(dc)
    where = random.sample(dc, 1)
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


def rewrite_times(dc):
    """
    s = sum(dc.values())
    dayOfWeek = datetime.now().weekday()
    if dayOfWeek == 0 or s >= 7:
        dc.update({k: 0 for k in dc})
    """
    n = 6  # 保留n-1天记录
    d = {k: v for k, v in dc.items() if v == n}
    if d:
        dc[list(d)[0]] = 0
    with open('food.YAML', 'w', encoding='utf8') as f:
        yaml.dump(dc, f, allow_unicode=True)


def str_clean(dc):
    sd = sorted(dc.items(), key=lambda x: x[1])
    s = str(sd).replace('[', '').replace(']', '').replace(r"'", '')
    return s


def send_dd(info1, info2):
    url = ' '  # 此处为钉钉机器人推送api
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
    foods = read_food('food.yaml')
    rewrite_times(foods)
    foods_filter = filter_foods(foods)
    foods_filter_bt = filter_foods_before_today(foods)
    value_plus_one(foods_filter_bt, foods)
    where_today = select_where(foods_filter)
    foods[where_today[0]] += 1
    rewrite_times(foods)
    send_dd(where_today[0], list(foods_filter_bt))
    s1 = where_today[0]
    s2 = str_clean(foods_filter_bt)
    print("今天去恰：{} \n最近恰了：{}".format(s1, s2))
