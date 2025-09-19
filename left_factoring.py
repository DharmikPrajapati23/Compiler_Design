def left_factoring(grammar):
    changed = True
    while changed:
        changed = False
        new_grammar = {}
        
        for nt, productions in grammar.items():
            prefixes = {}
            for prod in productions:
                prefix = prod[0] if prod else ''
                if prefix in prefixes:
                    prefixes[prefix].append(prod)
                else:
                    prefixes[prefix] = [prod]

            if any(len(prods) > 1 for prods in prefixes.values()):
                changed = True
                new_grammar[nt] = []
                for prefix, prods in prefixes.items():
                    if len(prods) > 1:
                        new_nt = nt + "'"
                        new_grammar[nt].append(prefix + new_nt)
                        new_prods = [prod[1:] if len(prod) > 1 else 'ε' for prod in prods]
                        new_grammar[new_nt] = new_prods
                    else:
                        new_grammar[nt].append(prods[0])
            else:
                new_grammar[nt] = productions
        
        grammar = new_grammar
    
    return grammar

def read_grammar_from_file(filepath):
    grammar = {}
    with open(filepath) as f:
        for line in f:
            if '->' in line:
                nt, rhs = line.strip().split("->")
                grammar[nt.strip()] = [prod.strip() for prod in rhs.split('|')]
    return grammar

def pretty_print_grammar(grammar):
    for nt, prods in grammar.items():
        print(f"{nt} -> {' | '.join(prods)}")


# Example usage
if __name__ == "__main__":
    grammar = read_grammar_from_file("grammar.txt")
    factored_grammar = left_factoring(grammar)
    pretty_print_grammar(factored_grammar)
