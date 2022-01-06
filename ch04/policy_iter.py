if '__file__' in globals():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from collections import defaultdict
from ch04.policy_eval import policy_eval


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


def policy_iter(env, gamma, threshold=0.001, is_render=True):
    pi = defaultdict(lambda: {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25})
    V = defaultdict(lambda: 0)

    while True:
        V = policy_eval(pi, V, env, gamma, threshold)
        new_pi = get_greedy_policy(V, env, gamma)

        if is_render:
            env.render_v(V, pi)

        if new_pi == pi:
            break
        pi = new_pi

    return pi