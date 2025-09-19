def remove_left_recursion(grammar):
    new_grammar = {}
    for non_terminal, productions in grammar.items():
        left_recursive = []
        non_left_recursive = []
        for prod in productions:
            if prod.startswith(non_terminal):
                left_recursive.append(prod[len(non_terminal):])
            else:
                non_left_recursive.append(prod)
        if left_recursive:
            new_non_terminal = non_terminal + "'"
            new_grammar[non_terminal] = []
            for prod in non_left_recursive:
                new_grammar[non_terminal].append(f"{prod}{new_non_terminal}")
            new_grammar[new_non_terminal] = []
            for prod in left_recursive:
                new_grammar[new_non_terminal].append(f"{prod}{new_non_terminal}")
            new_grammar[new_non_terminal].append("ε")
        else:
            new_grammar[non_terminal] = productions
    return new_grammar

def read_grammar_from_file(filepath):
    grammar = {}
    with open(filepath) as f:
        for line in f:
            if '->' in line:
                nt, rhs = line.strip().split("->")
                grammar[nt.strip()] = [prod.strip() for prod in rhs.split('|')]
    return grammar
