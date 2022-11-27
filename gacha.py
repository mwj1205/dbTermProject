import random

star1 = 78.5
star2 = 18.5
star3 = 3

star1_list = [10004101, 10005101, 20006101, 30004101, 30005101]

star2_list = [10003201, 20004201, 20005201, 30003201, 40002201, 50002201, 50001201]

star3_list = [10001301, 20001301, 20002301, 20003301, 30001301, 30002301, 40001301]

def rare_gacha():
    pick=random.random() * 100
    pick = round(pick, 1)

    if pick < star1: # 78.5% 미만
        cat = random.choice(star1_list)
        return cat
    elif pick >= star1 and pick < (star1 + star2):
        cat = random.choice(star2_list)
        return cat
    elif pick >= (star1 + star2) and pick < (star1 + star2 + star3):
        cat = random.choice(star3_list)
        return cat

def gacha_10last(): # 10연차 마지막은 2성 이상
    pick=random.random() * 100
    pick = round(pick, 1)

    if pick < 97:
        cat = random.choice(star2_list)
        return cat
    else:
        cat = random.choice(star3_list)
        return cat