if '__file__' in globals():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from collections import defaultdict


def eval_onestep(pi, V, env, gamma=0.9):
    delta = 0

    for state in env.states():
        action_probs = pi[state]
        new_v = 0

        for action, action_prob in action_probs.items():
            next_state = env.next_state(state, action)
            if next_state is not None:
                r = env.reward(state, action, next_state)
                new_v += action_prob * (r + gamma * V[next_state])

        delta = max(delta, abs(V[state] - new_v))
        V[state] = new_v

    return V, delta


def policy_eval(pi, V, env, gamma, threshold=0.001):
    while True:
        V, delta = eval_onestep(pi, V, env, gamma)
        if delta < threshold:
            break
    return V
