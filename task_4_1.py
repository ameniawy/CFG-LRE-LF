
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


def left_recursion_elemination(grammar):

    output_grammar = dict()
    for rule_name, rule_values in grammar.items():
        # First check for any substitution
        new_rules = []
        for rule_value in rule_values:
            if rule_value[0] in output_grammar.keys():
                for replacing_rule in output_grammar[rule_value[0]]:
                    new_rule = replacing_rule + rule_value[1:]
                    new_rules.append(new_rule)
            else:
                new_rules.append(rule_value)

        alphas = []
        betas = []

        for rule in new_rules:
            print("NEW RULES", rule, len(rule_name))
            if rule[0].strip() == rule_name:
                alphas.append(rule[1:])
            else:
                betas.append(rule)

        # if alphas list has elements
        if alphas:
            new_rule_name = rule_name.strip() + '1'
            betas_rules = [beta + [new_rule_name] for beta in betas]
            alphas_rules = [alpha + [new_rule_name] for alpha in alphas]
            alphas_rules.append(['epsilon'])
            output_grammar[rule_name.strip()] = betas_rules
            output_grammar[new_rule_name] = alphas_rules
        else:
            output_grammar[rule_name.strip()] = new_rules

    return output_grammar


def output_grammar(file_name, grammar):
    output_file = open(file_name, 'w+')

    counter = len(grammar.keys())

    for rule_name, rule_values in grammar.items():
        counter -= 1
        line = rule_name + ' : ' + \
            ' | '.join([' '.join(rule_value) for rule_value in rule_values])

        if counter != 0:
            line += '\n'
        output_file.write(line)
        print(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    input_grammar = read_grammar(args.file)

    fixed_grammar = left_recursion_elemination(input_grammar)

    output_grammar('task_4_1_result.txt', fixed_grammar)
