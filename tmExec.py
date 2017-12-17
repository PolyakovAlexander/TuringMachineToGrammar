import sys
from collections import defaultdict


def check_tm(word):
    word = '$' + word + 'B' * (3 * len(word) + 3) + '@'
    print(word)
    word = list(word)
    tmDelta = defaultdict(tuple)

    with open('TuringMachine.txt', 'r') as f:
        for line in f:
            if line != '\n':
                line = line[:-1]
                splitted = line.split(',')
                tmDelta[(splitted[0], splitted[1])] = splitted[2:]

    pos = 1
    state = 'start'
    tmp = word
    tmp = tmp[:pos] + ['>'] + tmp[pos:]
    print(' '.join(tmp) + ' ' + state)
    while True:
        nextState = tmDelta[(state, word[pos])]
        if nextState == ():
            break
        state = nextState[0]
        word[pos] = nextState[1]
        pos = pos + 1 if nextState[2] == 'r' else pos - 1
        tmp = word
        tmp = tmp[:pos] + ['>'] + tmp[pos:]
        print(' '.join(tmp) + ' ' + state)

    return state

if __name__ == '__main__':
    check_tm(sys.argv[1])
