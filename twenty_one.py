import random
import pandas as pd
from crypto.Random import get_random_bytes  # pycryptodome 库


def shuffle_cards():
    """返回打乱除去鬼的八副牌"""
    desigh = ['♠', '♥', '♣', '♦']  # 表示黑桃、红桃、梅花、方块
    num = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    cards = [i + j for i in desigh for j in num for k in range(10)]
    random_bytes = get_random_bytes(random.randint(1, 101))
    sd = int.from_bytes(random_bytes, byteorder='big')
    random.seed(sd)
    random.shuffle(cards)
    return cards


def value(cards):
    """计算牌面点数的总和。
    A可以算作1点，也可算作11点，取总点数大而不超过21的数值"""
    value_dic = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                 '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
    sum_of_value = sum([value_dic.get(i[1:]) for i in cards])
    for i in cards:
        if sum_of_value > 21 and i[1:] == 'A':
            sum_of_value += -10
    return sum_of_value


strategy_dic = pd.read_csv('strategy_table.csv').to_dict(orient='dict')


def strategy(zhuang, xian, option):
    """获取最佳策略，可不看"""
    xian_card = f'{xian.card[1][1]},{xian.card[0][1]}'
    if xian_card[-1] == 'A':
        xian_card = xian_card[::-1]
    # 闲家点数小于8，博牌（牌面中无A）
    if xian.value <= 8 and 'A' not in xian_card:
        return 'hit'
    # 闲家点数大于17，停牌（除'A,6', 'A,7'）
    elif xian.value >= 17 and xian_card not in ['A,6', 'A,7']:
        return 'stand'
    else:
        # 首先通过庄家明牌索引
        zhuang_card = zhuang.card[0][1:]
        if zhuang_card in 'JQK':
            zhuang_card = '10'
        possible = strategy_dic[zhuang_card]

        # 如果可以用闲家牌面索引（两张牌中有‘A’，或者点数相同），没有就用点数
        if xian_card in possible:
            opt = possible.get(xian_card, 'error')
        else:
            opt = possible.get(str(xian.value), 'error')

        # 出现两种选择，如果前者可以就返回第一种策略
        if '/' in opt:
            opts = opt.split('/')
            return opts[0] if opts[0] in option else opts[1]
        elif opt in option:
            return opt
        else:
            return 'stand'
