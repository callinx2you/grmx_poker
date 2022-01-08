from common.grmx_poker import GroovyMixPoker
from common.grmx_parser import grmx_parser, pickup_list, titles_list
from ch04.value_iter import value_iter
from ch04.policy_iter import get_greedy_policy


def print_policy(env, pi, V):
    print('#n y x policy')
    for k, v in pi.items():
        n, y, x = k
        print(n, y, x, pi[k][1], V[k])


def write_policy(env, pi, V, dst_name):
    with open(dst_name, 'w') as f:
        f.write('# enum members\n')
        for k, v in env.draw_meaning.items():
            f.write('# '+str(k)+': '+v+'\n')
        f.write('#\n')
        f.write('# enum titles\n')
        for i, v in enumerate(env.titles):
            f.write('# '+str(i)+': [')
            #f.write(str(v))
            for j in range(len(v)):
                if j:
                    f.write(', ')
                f.write(env.draw_meaning[v[j]])
            f.write(']\n')
        f.write('#\n')
        f.write('# result:\n')
        f.write('# n y x policy value\n')
        f.write('#   n: num of hand\n')
        f.write('#   y: title state so far in bit fashion\n')
        f.write('#   x: member state of hand in bit fashion\n\n')
        for k, v in pi.items():
            n, y, x = k
            f.write(str(n)+' '+str(y)+' '+str(x)+' ')
            f.write(env.action_meaning[int(pi[k][1])]+' ')
            f.write(str(V[k])+'\n')


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

    dst_name = 'grmx_policy_' + args.dst + '.txt'
    #print_policy(env, pi, V)
    write_policy(env, pi, V, dst_name)
