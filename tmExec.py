from collections import defaultdict

def checkTM(word):
    word = '$' + word + 'B' * (3 * len(word) + 3) + '@'
    print(word)
    word = list(word)
    tmDelta = defaultdict(tuple)

    with open('TuringMachine.txt', 'r') as f:
        for line in f:
            if line != '\n':
                line = line[:-1]
                splitted = line.split(',')
                tmDelta[(splitted[0], splitted[1])] = (splitted[2], splitted[3], splitted[4])

    pos = 1
    state = 'start'
    nextStateExist = True
    while nextStateExist:
        nextState = tmDelta[(state, word[pos])]
        if nextState == ():
            nextStateExist = False
            break
        state = nextState[0]
        word[pos] = nextState[1]
        pos = pos + 1 if nextState[2] == 'r' else pos - 1
        tmp = word.copy()
        tmp = tmp[:pos] + ['>'] + tmp[pos:]
        for item in tmp:
            print(item + ' ', end='')
        print(' ' + state + ' ' + word[pos])
    print(state)
    return state

if __name__ == '__main__':

    checkTM('101')
