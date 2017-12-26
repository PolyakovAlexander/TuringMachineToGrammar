import sys
from collections import defaultdict

# Turing machine configuration
try:
    TM = open('TuringMachine.txt', 'r')
    delta_function = []
    start_state = 'start'
    final_states = {'final'}
    # need statesWithoutFinal without final one
    statesWithoutFinal = set()
    for line in TM:
        statesWithoutFinal.add(line.split(',')[0])
        delta_function.append(line[:-1].split(','))
    sigma_alphabet = ['0', '1']
    gamma_alphabet = sigma_alphabet + ['000', '001', '010', '011', '100', '101', '110', '111'] + \
        ['000#', '001#', '010#', '011#', '100#', '101#', '110#', '111#']
    eps = 'e'
except IOError:
    print('Couldn\'t read file with Turing machine')
    sys.exit(1)

res_grammar = defaultdict(list)

# 1 group
for terminal in sigma_alphabet:
    res_grammar["A1"] += ['[$ ' + start_state + ' ' + terminal + ' ' + terminal + ' @]']

for q, A, p, B, d in filter(lambda x: x[0] in statesWithoutFinal, delta_function):
    for a in sigma_alphabet:
        if A == '$' and d == 'r':
            for X in gamma_alphabet:
                # 2.1
                res_grammar['[' + q + ' $ ' + X + ' ' + a + ' @]'] += ['[$ ' + p + ' ' + X + ' ' + a + ' @]']
                # 5.1
                res_grammar['[' + q + ' $ ' + X + ' ' + a + ']'] += ['[$ ' + p + ' ' + X + ' ' + a + ']']
        else:
            if A == '@' and d == 'l':
                for X in gamma_alphabet:
                    # 2.4
                    res_grammar['[$ ' + X + ' ' + a + ' ' + q + ' @]'] += ['[$ ' + p + ' ' + X + ' ' + a + ' @]']
                    # 7.2
                    res_grammar['[' + X + ' ' + a + ' ' + q + ' @]'] += ['[' + p + ' ' + X + ' ' + a + ' @]']
            else:
                # X == A and Y == B
                if d == 'l':
                    # 2.2
                    res_grammar['[$ ' + q + ' ' + A + ' ' + a + ' @]'] += ['[' + p + ' $ ' + B + ' ' + a + ' @]']
                    # 5.2
                    res_grammar['[$ ' + q + ' ' + A + ' ' + a + ']'] += ['[' + p + ' $ ' + B + ' ' + a + ']']

                    for Z in gamma_alphabet:
                        for b in sigma_alphabet:
                            # 6.2
                            res_grammar['[' + Z + ' ' + b + '][' + q + ' ' + A + ' ' + a + ']'] += \
                                ['[' + p + ' ' + Z + ' ' + b + '][' + B + ' ' + a + ']']
                            # 6.4
                            res_grammar['[$ ' + Z + ' ' + b + '][' + q + ' ' + A + ' ' + a + ']'] += \
                                ['[$ ' + p + ' ' + Z + ' ' + b + '][' + B + ' ' + a + ']']
                            # 7.3
                            res_grammar['[' + Z + ' ' + b + '][' + q + ' ' + A + ' ' + a + ' @]'] += \
                                ['[' + p + ' ' + Z + ' ' + b + '][' + B + ' ' + a + ' @]']
                else:
                    # 2.3
                    res_grammar['[$ ' + q + ' ' + A + ' ' + a + ' @]'] += ['[$ ' + B + ' ' + a + ' ' + p + ' @]']

                    for Z in gamma_alphabet:
                        for b in sigma_alphabet:
                            # 5.3
                            res_grammar['[$ ' + q + ' ' + A + ' ' + a + '][' + Z + ' ' + b + ']'] += \
                                ['[$ ' + B + ' ' + a + '][' + p + ' ' + Z + ' ' + b + ']']
                            # 6.1
                            res_grammar['[' + q + ' ' + A + ' ' + a + '][' + Z + ' ' + b + ']'] += \
                                ['[' + B + ' ' + a + '][' + p + ' ' + Z + ' ' + b + ']']
                            # 6.3
                            res_grammar['[' + q + ' ' + A + ' ' + a + '][' + Z + ' ' + b + ' @]'] += \
                                ['[' + B + ' ' + a + '][' + p + ' ' + Z + ' ' + b + ' @]']

                    # 7.1
                    res_grammar['[' + q + ' ' + A + ' ' + a + ' @]'] += ['[' + B + ' ' + a + ' ' + p + ' @]']

for q in final_states:
    for X in gamma_alphabet:
        for a in sigma_alphabet:
            # 3
            res_grammar['[' + q + ' $ ' + X + ' ' + a + ' @]'] += [a]
            res_grammar['[$ ' + q + ' ' + X + ' ' + a + ' @]'] += [a]
            res_grammar['[$ ' + X + ' ' + a + ' ' + q + ' @]'] += [a]
            # 8
            res_grammar['[' + q + ' $ ' + X + ' ' + a + ']'] += [a]
            res_grammar['[$ ' + q + ' ' + X + ' ' + a + ']'] += [a]
            res_grammar['[' + q + ' ' + X + ' ' + a + ']'] = [a]
            res_grammar['[' + q + ' ' + X + ' ' + a + ' @]'] += [a]
            res_grammar['[' + X + ' ' + a + ' ' + q + ' @]'] += [a]

            # 9
            for b in sigma_alphabet:
                res_grammar[a + '[' + X + ' ' + b + ']'] += [a + b]
                res_grammar[a + '[' + X + ' ' + b + ' @]'] += [a  + b]
                res_grammar['[' + X + ' ' + a  + ']'+ b] += [a + b]
                res_grammar['[$ ' + X + ' ' + a + ']' + b] += [a + b]

# 4
for a in sigma_alphabet:
    res_grammar['[A1]'] += ['[$ ' + start_state + ' ' + a + ' ' + a + '][A2]']
    res_grammar['[A2]'] += ['[' + a + ' ' + a + '][A2]']
    res_grammar['[A2]'] += ['[' + a + ' ' + a + ' @]']

with open('grammarTypeOne.txt', 'w') as f:
    for k, v in res_grammar.items():
        for right in v:
            f.write(k + ' -> ' + right + '\n')
