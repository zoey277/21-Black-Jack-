import random
import twenty_one
from tqdm import tqdm

FILE = '100.csv'
GAMES = 100
INITIAL_CHIPS = 100
BET = 10


class Person:
    """
    将庄闲共同的属性放在此类中
    生成庄家
    """
    card = []
    value = 0

    @classmethod
    def reset(cls):
        cls.card = []
        cls.value = 0


class Player(Person):
    """生成闲家"""
    bet = BET  # 赌注
    chips = INITIAL_CHIPS  # 初始筹码

    def __init__(self):
        super().__init__()
        self.strategy_choice = None  # 根据策略表选择的策略
        self.option_lst = []  # 存放每局的策略，方便记录

    def restart(self):
        super().reset()
        self.bet = BET
        self.strategy_choice = None
        self.option_lst = []

    @classmethod
    def reset(cls):
        cls.chips = INITIAL_CHIPS


class Game:
    flag = []  # 用1、0记录每一局的胜负，存入列表中。反映游戏总局数、胜利局数、输赢趋势变化
    chip_change_ls = []
    strategy_data = {  # 记录使用每个策略的[胜利次数, 总次数]，可以得到各自的胜率
        'stand': [0, 0],
        'hit': [0, 0],
        'double': [0, 0],
        'surrender': [0, 0]
    }

    def __init__(self):
        self.status = True  # 游戏状态。为False时结束该局游戏
        self.cards = twenty_one.shuffle_cards()  # 每次都重新打乱了牌，有点浪费计算资源，不过随机效果更好
        self.func_dic = {  # 功能字典，需要的时候调用对应的函数。替换了条件判断过程
            'stand': self.stand,
            'double': self.double,
            'hit': self.hit,
            'surrender': self.surrender
        }

    def run(self):
        """单局游戏主流程"""
        self.start()
        self.make_option()
        self.func_dic.get(xian.strategy_choice)()
        if self.status:
            self.compare()
        xian.restart()
        zhuang.reset()

    @staticmethod
    def get_card(person, n: int):
        """person随机取n张牌"""
        for t in range(n):
            num = random.randint(0, len(game.cards) - 1)
            add_card = game.cards[num]
            person.card.append(add_card)
            game.cards.remove(add_card)
        person.value = twenty_one.value(person.card)

    @staticmethod
    def start():
        """开局庄闲各取两张牌"""
        game.get_card(xian, 2)
        game.get_card(zhuang, 2)

    @staticmethod
    def make_option():
        """根据策略表做选择"""
        options = ['stand', 'surrender']  # 任何条件都可以选择停牌和弃牌
        if xian.value < 21:
            options.append('hit')
            if xian.chips >= xian.bet * 2:
                options.append('double')
        xian.strategy_choice = twenty_one.strategy(zhuang, xian, options)

    @staticmethod
    def stand():
        """停牌"""
        xian.option_lst.append('stand')

    @staticmethod
    def double():
        """赌注加倍，同时要一张牌"""
        xian.option_lst.append('double')
        xian.bet = xian.bet * 2
        game.get_card(xian, 1)
        if xian.value > 21:
            game.fail()

    @staticmethod
    def hit():
        """博牌，点数允许的话可以一直要牌"""
        xian.option_lst.append('hit')
        game.get_card(xian, 1)
        if xian.value > 21:
            game.fail()
        elif xian.value == 21:
            xian.chips += xian.bet * 2  # 幸运21点可得三倍回报，此处加上额外的两倍
            game.win()
        else:
            game.make_option()
            # （规则）选择hit之后就不能double了
            if xian.strategy_choice == 'double':
                xian.strategy_choice = 'hit'
            # 从功能字典中获取对应的函数名并执行
            game.func_dic.get(xian.strategy_choice)()

    @staticmethod
    def surrender():
        """弃牌"""
        xian.option_lst.append('surrender')
        game.fail()

    @staticmethod
    def compare():
        """比较庄闲点数，分出胜负"""
        while zhuang.value < 17:  # 庄家点数小于17必须要牌
            game.get_card(zhuang, 1)
            if zhuang.value > 21:
                game.win()
        if game.status:
            if zhuang.value >= xian.value:  # 点数相等也算庄家赢
                game.fail()
            else:
                game.win()

    @staticmethod
    def win():
        xian.chips += xian.bet  # 赢得赌注数量的筹码
        Game.chip_change_ls.append(xian.chips)  # 记录闲家的筹码
        Game.flag.append(1)  # 表示赢了一局
        for opt in xian.option_lst:  # 使用策略的数量都加一
            Game.strategy_data[opt] = [i + 1 for i in Game.strategy_data[opt]]
        game.status = False  # 改变状态，结束本局游戏

    @staticmethod
    def fail():
        xian.chips -= xian.bet
        Game.chip_change_ls.append(xian.chips)
        Game.flag.append(0)
        for opt in xian.option_lst:
            Game.strategy_data[opt][1] += 1
        game.status = False

    @classmethod
    def reset(cls):
        cls.flag = []
        cls.chip_change_ls = []
        cls.strategy_data = {'stand': [0, 0], 'hit': [0, 0], 'double': [0, 0], 'surrender': [0, 0]}


def write_data(data):
    with open(FILE, 'a') as fr:
        fr.write(str(data) + '\n')


if __name__ == '__main__':
    all_flag_ls, all_chips_change_ls, all_strategy_data_ls_from_dic = [], [], []
    for num_of_Games in tqdm(range(1, GAMES + 1)):
        zhuang = Person()
        xian = Player()
        while xian.chips > 0:
            game = Game()
            game.run()
            game = Game()  # 不改变类属性，再次生成一个game实例
        # print(sum([Game.chip_change_ls[i] - Game.chip_change_ls[i - 1] for i in range(len(flag)) if i > 0 and flag[i] == 1]) - 1000)

        all_flag_ls.append(Game.flag)
        all_chips_change_ls.append(Game.chip_change_ls)
        all_strategy_data_ls_from_dic.append(Game.strategy_data)

        Person.reset()  # 玩家输光了所有赌注，离场，游戏结束。重置所有类属性后游戏重新开始，玩家进场。
        Player.reset()
        Game.reset()

    # print(all_flag_ls)
    # print(all_chips_change_ls)
    # print(all_strategy_data_ls_from_dic)

    write_data(all_flag_ls)
    write_data(all_chips_change_ls)
    write_data(all_strategy_data_ls_from_dic)
