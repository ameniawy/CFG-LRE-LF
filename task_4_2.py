
import argparse
from collections import defaultdict


def read_grammar(file_name):
    grammar = dict()
    with open(args.file, "r") as file:
        for line in file.readlines():
            rule_id, operands = line.split(':')
            operands = [operand.strip().split()
                        for operand in operands.strip().split("|")]
            grammar[rule_id.strip()] = operands

    return grammar


def get_common_prefix(rule):
    freq = defaultdict(int)
    for literal in rule:
        freq[literal[0]] += 1

    if freq:
        sorted_dict = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        if sorted_dict[0][1] > 1:
            return sorted_dict[0][0]

    return None


def left_factoring(grammar):
    changed = True
    while(changed):
        changed = False
        grammar_copy = grammar.copy()

        for rule_name, rule_values in grammar.items():
            common_prefix = get_common_prefix(rule_values)
            if common_prefix:
                changed = True
                new_rule_name = rule_name.strip() + '1'
                rule_array = []
                rule_array.append([common_prefix, new_rule_name])
                new_rule_array = []
                for rule_value in rule_values:
                    if rule_value[0] == common_prefix:
                        new_rule_array.append(rule_value[1:])
                    else:
                        rule_array.append(rule_value)

                grammar_copy[rule_name] = rule_array
                grammar_copy[new_rule_name] = new_rule_array

        grammar = grammar_copy
    return grammar


def output_factored_dict(file_name, grammar):
    output_file = open(file_name, 'w+')

    counter = len(grammar.keys())

    for rule_name, rule_values in grammar.items():
        counter -= 1
        line = rule_name + ' : ' + \
            ' | '.join([' '.join(rule_value) for rule_value in rule_values])

        if counter != 0:
            line += '\n'
        output_file.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    input_grammar = read_grammar(args.file)

    factored_grammar = left_factoring(input_grammar)

    output_factored_dict('task_4_2_result.txt', factored_grammar)
