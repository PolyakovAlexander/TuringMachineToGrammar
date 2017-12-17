import sys
import json
from collections import defaultdict

# Turing machine configuration
try:
    TM = open('TuringMachine.txt', 'r')
    delta_function = []
    start_state = 'start'
    final_states = {'FINAL'}
    states = final_states.copy()
    for line in TM:
        states.add(line.split(',')[0])
        delta_function.append(line[:-1].split(','))
    sigma_alphabet = '01$@'
    gamma_alphabet = sigma_alphabet + 'BCDEX#%&'
    eps = 'e'
except IOError:
    print('Couldn\'t read file with Turing machine')
    sys.exit(1)

# Adding grammar rules
res_grammar = defaultdict(list)
res_grammar['A1'] += [start_state + ' A2']
res_grammar['A2'] += [a + a + ' A2' for a in sigma_alphabet] + ['A3']
res_grammar['A3'] += [eps + 'B' + ' A3'] + [eps]

for (q, C, p, D, _) in filter(lambda x: x[4] == 'r', delta_function):
    for a in sigma_alphabet + eps:
        res_grammar[q + ' ' + a + C] += \
        [a + D + ' ' + p]

for (q, C, p, D, _) in filter(lambda x: x[4] == 'l', delta_function):
    for a in sigma_alphabet + eps:
        for b in sigma_alphabet + eps:
            for E in gamma_alphabet:
                res_grammar[b + E + ' ' + q + ' ' + a + C] += \
                [p + ' ' + b + E + ' ' + a + D]

for final in final_states:
    res_grammar[final] += [eps]
    for a in sigma_alphabet + eps:
        for C in gamma_alphabet:
            res_grammar[a + C + ' ' + final] += [final + ' ' + a + ' ' + final]
            res_grammar[final + ' ' + a + C] += [final + ' ' + a + ' ' + final]

with open('grammar', 'w') as f:
    for k, v in res_grammar.items():
        for right in v:
            f.write(k + ' -> ' + right + '\n')