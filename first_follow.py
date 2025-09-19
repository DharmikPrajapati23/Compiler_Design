import left_recursion  # Import your left_recursion module

def read_grammar_from_file(filepath):
    grammar = {}
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            if '->' in line:
                nt, rhs = line.strip().split('->')
                nt = nt.strip()
                productions = []
                for prod in rhs.split('|'):
                    prod = prod.strip()
                    # Treat ε as epsilon symbol; no change needed if directly written
                    if prod == 'ε' or prod == '':
                        productions.append(['ε'])
                    else:
                        productions.append(list(prod))
                grammar[nt] = productions
    return grammar

def convert_productions_list_to_str(grammar):
    # Convert list of symbols back to string for left recursion module input
    converted = {}
    for nt, prods in grammar.items():
        converted[nt] = [''.join(prod) for prod in prods]
    return converted

def convert_productions_str_to_list(grammar):
    # Convert left recursion module output back to list of symbols
    converted = {}
    for nt, prods in grammar.items():
        converted[nt] = [list(prod) if prod != 'ε' else ['ε'] for prod in prods]
    return converted

def compute_first(grammar):
    first = {}
    visited = set()
    computing = set()

    def first_of(symbol):
        if symbol not in grammar:
            # Terminal symbol
            return {symbol}
        if symbol in first:
            return first[symbol]
        if symbol in computing:
            # Cycle detected; treat as empty to break infinite recursion
            return set()
        computing.add(symbol)
        
        result = set()
        for production in grammar[symbol]:
            for sym in production:
                sym_first = first_of(sym)
                result |= (sym_first - {'ε'})
                if 'ε' not in sym_first:
                    break
            else:
                result.add('ε')
        computing.remove(symbol)
        first[symbol] = result
        return result

    for nt in grammar:
        if nt not in first:
            first_of(nt)
    return first


def compute_follow(grammar, first):
    follow = {nt: set() for nt in grammar}
    start_symbol = next(iter(grammar))
    follow[start_symbol].add('$')
    
    updated = True
    while updated:
        updated = False
        for nt in grammar:
            for production in grammar[nt]:
                for idx, symbol in enumerate(production):
                    if symbol in grammar:
                        rest = production[idx+1:]
                        fset = set()
                        for sym in rest:
                            sym_first = first[sym] if sym in grammar else {sym}
                            fset |= (sym_first - {'ε'})
                            if 'ε' not in sym_first:
                                break
                        else:
                            fset |= follow[nt]
                        if not fset.issubset(follow[symbol]):
                            follow[symbol] |= fset
                            updated = True
    return follow

def pretty_print(symbols):
    return ', '.join(('∈' if s=='ε' else s) for s in sorted(symbols, key=lambda x: (x == 'ε', x)))

if __name__ == "__main__":
    grammar = read_grammar_from_file("grammar.txt")

    # Convert list-of-symbols grammar to strings for left recursion removal
    grammar_str = convert_productions_list_to_str(grammar)

    # Remove left recursion
    grammar_no_lr = left_recursion.remove_left_recursion(grammar_str)

    # Convert back to list-of-symbols grammar for first/follow calculation
    grammar_processed = convert_productions_str_to_list(grammar_no_lr)

    # Compute First and Follow on processed grammar
    first = compute_first(grammar_processed)
    follow = compute_follow(grammar_processed, first)

    print("FIRST sets:")
    for nt in first:
        print(f"First({nt}) = {{ {pretty_print(first[nt])} }}")
    print("\nFOLLOW sets:")
    for nt in follow:
        print(f"Follow({nt}) = {{ {pretty_print(follow[nt])} }}")
