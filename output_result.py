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
