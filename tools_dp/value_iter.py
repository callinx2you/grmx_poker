if '__file__' in globals():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from collections import defaultdict
from common.grmx_poker import GroovyMixPoker


def argmax(d):
    if d == {}:
        return -1
    max_value = max(d.values())
    max_key = -1
    for key, value in d.items():
        if value == max_value:
            max_key = key
    return max_key


def get_greedy_policy(V, env, gamma):
    pi = {}

    for state in env.states():
        action_values = {}

        for action in env.actions():
            next_states = env.next_states(state, action)
            value = 0
            for next_state, prob in next_states.items():
                r = env.reward(state, action, next_state)
                value += prob * (r + gamma * V[next_state])
            action_values[action] = value

        max_action = argmax(action_values)
        action_probs = {0: 0, 1: 0}
        action_probs[max_action] = 1.0
        pi[state] = action_probs

    return pi


def value_iter_onestep(env, gamma, V):
    delta = 0

    for state in env.states():
        action_values = []

        for action in env.actions():
            value = 0
            next_states = env.next_states(state, action)
            for next_state, prob in next_states.items():
                r = env.reward(state, action, next_state)
                value += prob * (r + gamma * V[next_state])
            action_values.append(value)

        if len(action_values) > 0:
            new_value = max(action_values)
            delta = max(delta, abs(new_value - V[state]))
            V[state] = new_value

    return V, delta


def value_iter(env, gamma, threshold=0.001):
    V = defaultdict(lambda: 0)

    while True:
        V, delta = value_iter_onestep(env, gamma, V)
        if delta < threshold:
            break
    return V


if __name__ == '__main__':
    env = GroovyMixPoker()
    gamma = 1
    threshold = 1e-3
    V = value_iter(env, gamma)
    pi = get_greedy_policy(V, env, gamma)

    print("#n y x policy")
    for k, v in pi.items():
        n, y, x = k
        print(n, y, x, "DRAW" if pi[k][1] else "RESET")#, V[k])
