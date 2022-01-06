from collections import defaultdict, deque
import numpy as np


class GroovyMixPoker:
    def __init__(self):
        self.action_space = [0, 1]
        self.action_meaning = {
            0: "RESET",
            1: "DRAW",
        }
        self.num_cards = {
            0: 3,
            1: 3,
            2: 3,
            3: 3,
            4: 40,
        }
        self.draw_meaning = {
            0: "TOWA",
            1: "IBUKI",
            2: "NOA",
            3: "SAKI",
            4: "OTHERS",
        }
        self.init_states = {
            (2, 0,  0):    40*39/52/51,
            
            (2, 0,  1): 2* 40* 3/52/51,
            (2, 0,  2):     3* 2/52/51,
            (2, 0,  4): 2* 40* 3/52/51,
            (2, 0,  8):     3* 2/52/51,
            (2, 0, 16): 2* 40* 3/52/51,
            (2, 0, 32):     3* 2/52/51,
            (2, 0, 64): 2* 40* 3/52/51,
            (2, 0,128):     3* 2/52/51,
            
            (2, 1,  5): 2*  3* 3/52/51,
            (2, 0, 17): 2*  3* 3/52/51,
            (2, 0, 20): 2*  3* 3/52/51,
            (2, 0, 65): 2*  3* 3/52/51,
            (2, 0, 68): 2*  3* 3/52/51,
            (2, 2, 80): 2*  3* 3/52/51,
        }
        self.all_states = self.gen_all_states()
    
    def draw_probs(self, state):
        n, _, x = state
        probs = defaultdict(lambda: 0)
        s = 0
        for i in range(4):
            probs[i] = 3 - (x % 4)
            s       += x % 4
            x //= 4
        probs[4] = 40 - (n - s)
        for i in range(5):
            probs[i] /= 52 - n
        return probs
    
    def update_title(self, x, y):
        s = [0] * 4
        for i in range(4):
            s[i] = (x%4 + 3)//4
            x //= 4
        if s[0] and s[1]:
            y |= 1
        if s[1] and s[2] and s[3]:
            y |= 2
        return y

    def gen_all_states(self):
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
        if y == 3:#is_goal
            return d
        for init_state, prob in self.init_states.items():
            _n, _y, _x = init_state
            _y |= y
            if _y == 3:
                _n, _x = 0, 0
            d[(_n, _y, _x)] += prob
        return d
    
    def next_states(self, state, action):#goal_stateのときのみ{}が返ってくる. それ以外は足して1になる
        d = defaultdict(lambda: 0)
        n, y, x = state
        if y == 3:
            return d
        if action == 1: #DRAW
            for draw, prob in self.draw_probs(state).items():
                if prob == 0:
                    continue
                _n, _y, _x = n+1, y, x
                if draw < 4:
                    _x += 1<<(draw<<1)
                _y = self.update_title(_x, _y)
                if _y == 3:
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
