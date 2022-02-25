import argparse


def pickup_list(pickup_str):
    if pickup_str is None:
        return None#['TOWA', 'IBUKI', 'NOA', 'SAKI']

    elif pickup_str == 'HAround':
        return ['RINKU', 'MAHO', 'MUNI', 'REI']

    elif pickup_str == 'PPkey':
        return ['KYOKO', 'SHINOBU', 'YUKA', 'ESORA']

    elif pickup_str == 'PMaiden':
        return ['SAKI', 'IBUKI', 'TOWA', 'NOA']

    elif pickup_str == 'Merm4id':
        return ['RIKA', 'MARIKA', 'SAORI', 'DALIA']

    elif pickup_str == 'Rondo':
        return ['TSUBAKI', 'NAGISA', 'HIIRO', 'AOI']

    elif pickup_str == 'LLily':
        return ['MIYU', 'HARUNA', 'KURUMI', 'MIIKO']

    ret = pickup_str.split('-')

    s = set()
    for i in ret:
        s.add(i)

    if len(s) != 4:
        raise Exception('num of pickup members is not 4. stop.')
    return ret


def titles_list(titles_str, ):
    if titles_str is None:
        return None
    ret = []
    for i in titles_str:
        ret.append(i.split('-'))
    if len(ret) > 3:
        raise Exception('titles are too much. stop.')

    d = []
    for t in ret:
        for m in t:
            if m not in d:
                d.append(m)
    if len(d) > 7:
        raise Exception('members are too much. stop.')

    return ret


def grmx_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--pickup', help=
        '4 members or 1 unit picked up.                             '
        '  ex1.) TOWA-IBUKI-NOA-SAKI                                '
        '  ex2.) PMaiden                                            '
        , type=str)
    parser.add_argument(
        '--titles', help=
        'Members of titles.                                         '
        'ex.) TOWA-IBUKI IBUKI-NOA-SAKI                             '
        , type=str, nargs='*')
    parser.add_argument(
        '--no_reset', help='no RESET action (just DRAW)', action='store_true')
    parser.add_argument(
        '--dst', help='output text name. grmx_policy_${DST}.txt'
        , type=str, default='default')

    return parser.parse_args()
