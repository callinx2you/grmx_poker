from collections import defaultdict


def title_control(pickup, titles):
    cards = defaultdict(int)                  # dict { idx: num_cards }
    meaning = defaultdict(lambda: 'OTHERS')   # dict { idx: name }
    i_meaning = defaultdict(lambda: -1)       # dict { name: idx }

    if pickup is None and titles is None:
        pickup = ['a', 'b', 'c', 'd']
        titles = [['a', 'b'], ['c', 'd']]
    elif pickup is not None and titles is None:
        titles = [ pickup[:2], pickup[2:]]
    elif pickup is None and titles is not None:
        d = []
        for t in titles:
            for m in t:
                if m not in d:
                    d.append(m)
        if len(d) != 4:
            raise Exception('cannot read explicit pickup members. stop.')
        pickup = d.copy()


    for i, pu in enumerate(pickup):
        if pu in meaning.values():
            raise Exception('picked-up member is duplicated. stop.')
        cards[i] = 3
        meaning[i] = pu
        i_meaning[pu] = i


    cnt = 4
    titles_enum = []
    for t in titles:
        title_enum = []
        for m in t:
            if m not in meaning.values():
                cards[cnt] = 2
                meaning[cnt] = m
                i_meaning[m] = cnt
                cnt += 1
            title_enum.append(i_meaning[m])
        titles_enum.append(title_enum)

    cards[-1] = 52 - sum(cards.values())
    meaning[-1] = 'OTHERS'
    i_meaning['OTHERS'] = -1

    if cnt > 6:
        raise Exception('too many members to calculate. stop.')

    return cnt, cards, meaning, titles_enum
