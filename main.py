from common.grmx_poker import GroovyMixPoker
from common.grmx_parser import grmx_parser, pickup_list, titles_list
from tools_dp.value_iter import value_iter, get_greedy_policy
from output_result import print_policy, write_policy


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

    dst_name = 'results/grmx_policy_' + args.dst + '.txt'
    #print_policy(env, pi, V)
    write_policy(env, pi, V, dst_name)
