import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from collections import defaultdict, deque
import numpy as np
from common.title_control import title_control


class GroovyMixPoker:
    def __init__(self, pickup=None,#['TOWA', 'IBUKI', 'NOA', 'SAKI'],
                 titles=None,
                        #[['TOWA', 'IBUKI'],
                        # ['IBUKI', 'NOA', 'SAKI']],
                 no_reset=False):

        # action control
        self.action_space = []
        self.action_meaning = {}
        if not no_reset: # has reset action
            self.action_space.append(0)
            self.action_meaning[0] = 'RESET'
        self.action_space.append(1)
        self.action_meaning[1] = 'DRAW'


        # title control
        self.unit_size, self.num_cards, self.draw_meaning, self.titles = title_control(pickup, titles)
        ### no title until Jun2021
        #self.titles = [[0, 1], [2, 3]]    # Jul2021 (no_reset)
        #self.titles = [[0, 1], [2, 3]]    # Aug2021 (no_reset)
        #self.titles = [[0, 1], [2, 3]]    # Sep2021
        #self.titles = [[0, 1], [2, 3], [3, 4, 5]]    # Oct2021
        #self.titles = [[0, 1], [1, 2, 3]] # Nov2021
        #self.titles = [[0, 1], [2, 3]]    # Jan2022

        self.init_states = self.gen_init_states()
        self.all_states = self.gen_all_states()

    def draw_probs(self, state):
        n, _, x = state
        probs = defaultdict(lambda: 0)
        for i in range(self.unit_size):
            probs[i] = self.num_cards[i] * (1 - x&1) / (52 - n)
            x >>= 1
        probs[-1] = 1 - sum(probs.values())
        return probs

    def update_title(self, x, y):
        for i, title in enumerate(self.titles):
            ok = True
            for a in title:
                if x&(1<<a) == 0:
                    ok = False
            if ok:
                y |= 1<<i
        return y

    def gen_init_states(self):
        seed_states = defaultdict(lambda: 0)
        seed_states[(0, 0, 0)] = 1.0
        init_num = 2
        while init_num:
            init_num -= 1
            tmp_states = defaultdict(lambda: 0)
            for s, p_state in seed_states.items():
                for card, p_card in self.draw_probs(s).items():
                    _n, _y, _x = s
                    _n += 1
                    if card != -1:
                        _x |= 1<<card
                    _y = self.update_title(_x, _y)
                    tmp_states[(_n, _y, _x)] += p_state * p_card
            seed_states = tmp_states
        return seed_states

    def gen_all_states(self):
        # 全ての状態の配列を返す
        d = []
        q = deque()
        for init_state, prob in self.init_states.items():
            q.append(init_state)
        while q:
            state = q.popleft()
            if state in d:
                continue
            d.append(state)
            for action in self.action_space:
                next_states = self.next_states(state, action)
                for next_state in next_states.keys():
                    if next_state in d:
                        continue
                    if next_state in q:
                        continue
                    q.append(next_state)
        return sorted(d)

    def states(self):
        for state in self.all_states:
            yield state

    def actions(self):
        return self.action_space

    def reset_state(self, state): # dict{next_state: prob} を返す
        d = defaultdict(lambda: 0)
        n, y, x = state
        if y+1 == 1<<len(self.titles):
            return d
        for init_state, prob in self.init_states.items():
            _n, _y, _x = init_state
            _y |= y
            if _y+1 == 1<<len(self.titles):
                _n, _x = 0, 0
            d[(_n, _y, _x)] += prob
        return d

    def next_states(self, state, action):#goal_stateのときのみ{}が返ってくる. それ以外は足して1になる
        d = defaultdict(lambda: 0)
        n, y, x = state
        if y+1 == 1<<len(self.titles):
            return d
        if action == 1: #DRAW
            for draw, prob in self.draw_probs(state).items():
                if prob == 0:
                    continue
                _n, _y, _x = n+1, y, x
                if draw != -1:
                    _x |= 1<<draw
                _y = self.update_title(_x, _y)
                if _y+1 == 1<<len(self.titles):
                    _n, _x = 0, 0
                _state = (_n, _y, _x)
                if _n == 7:
                    init_states = self.reset_state(_state)
                    for init_state, init_prob in init_states.items():
                        d[init_state] += prob * init_prob
                else:
                    d[_state] += prob
        else: #RESET
            init_states = self.reset_state(state)
            for init_state, init_prob in init_states.items():
                d[init_state] += init_prob
        return d

    def reward(self, state, action, next_state):
        return -1


if __name__ == "__main__":
    env = GroovyMixPoker()
    all_states = env.all_states
    print(all_states)
    print(len(all_states))
