from common.grmx_poker import GroovyMixPoker
from common.grmx_parser import grmx_parser, pickup_list, titles_list
from ch04.value_iter import value_iter
from ch04.policy_iter import get_greedy_policy


def print_policy(pi, V):
    print("#n y x policy")
    for k, v in pi.items():
        n, y, x = k
        print(n, y, x, "DRAW" if pi[k][1] else "RESET", V[k])


if __name__ == '__main__':
    #
    # usage: $ python3 main.py -h
    #
    # args: --pickup, --titles, --no_reset
    #
    # more detail, please read common/grmx_parser.py
    #
    args = grmx_parser()
    pickup = pickup_list(args.pickup)
    titles = titles_list(args.titles)


    env = GroovyMixPoker(pickup, titles, args.no_reset)
    gamma = 1.0
    threshold = 1e-3
    V = value_iter(env, gamma)
    pi = get_greedy_policy(V, env, gamma)

    print_policy(pi, V)
