# import left_recursion  # Import your left_recursion module

# def read_grammar_from_file(filepath):
#     grammar = {}
#     with open(filepath, "r", encoding="utf-8") as file:
#         for line in file:
#             if '->' in line:
#                 nt, rhs = line.strip().split('->')
#                 nt = nt.strip()
#                 productions = []
#                 for prod in rhs.split('|'):
#                     prod = prod.strip()
#                     # Treat ε as epsilon symbol; no change needed if directly written
#                     if prod == 'ε' or prod == '':
#                         productions.append(['ε'])
#                     else:
#                         productions.append(list(prod))
#                 grammar[nt] = productions
#     return grammar

# def convert_productions_list_to_str(grammar):
#     # Convert list of symbols back to string for left recursion module input
#     converted = {}
#     for nt, prods in grammar.items():
#         converted[nt] = [''.join(prod) for prod in prods]
#     return converted

# def convert_productions_str_to_list(grammar):
#     # Convert left recursion module output back to list of symbols
#     converted = {}
#     for nt, prods in grammar.items():
#         converted[nt] = [list(prod) if prod != 'ε' else ['ε'] for prod in prods]
#     return converted

# def compute_first(grammar):
#     first = {}
#     visited = set()
#     computing = set()

#     def first_of(symbol):
#         if symbol not in grammar:
#             # Terminal symbol
#             return {symbol}
#         if symbol in first:
#             return first[symbol]
#         if symbol in computing:
#             # Cycle detected; treat as empty to break infinite recursion
#             return set()
#         computing.add(symbol)
        
#         result = set()
#         for production in grammar[symbol]:
#             for sym in production:
#                 sym_first = first_of(sym)
#                 result |= (sym_first - {'ε'})
#                 if 'ε' not in sym_first:
#                     break
#             else:
#                 result.add('ε')
#         computing.remove(symbol)
#         first[symbol] = result
#         return result

#     for nt in grammar:
#         if nt not in first:
#             first_of(nt)
#     return first


# def compute_follow(grammar, first):
#     follow = {nt: set() for nt in grammar}
#     start_symbol = next(iter(grammar))
#     follow[start_symbol].add('$')
    
#     updated = True
#     while updated:
#         updated = False
#         for nt in grammar:
#             for production in grammar[nt]:
#                 for idx, symbol in enumerate(production):
#                     if symbol in grammar:
#                         rest = production[idx+1:]
#                         fset = set()
#                         for sym in rest:
#                             sym_first = first[sym] if sym in grammar else {sym}
#                             fset |= (sym_first - {'ε'})
#                             if 'ε' not in sym_first:
#                                 break
#                         else:
#                             fset |= follow[nt]
#                         if not fset.issubset(follow[symbol]):
#                             follow[symbol] |= fset
#                             updated = True
#     return follow

# def pretty_print(symbols):
#     return ', '.join(('∈' if s=='ε' else s) for s in sorted(symbols, key=lambda x: (x == 'ε', x)))

# if __name__ == "__main__":
#     grammar = read_grammar_from_file("grammar.txt")

#     # Convert list-of-symbols grammar to strings for left recursion removal
#     grammar_str = convert_productions_list_to_str(grammar)

#     # Remove left recursion
#     grammar_no_lr = left_recursion.remove_left_recursion(grammar_str)

#     # Convert back to list-of-symbols grammar for first/follow calculation
#     grammar_processed = convert_productions_str_to_list(grammar_no_lr)

#     # Compute First and Follow on processed grammar
#     first = compute_first(grammar_processed)
#     follow = compute_follow(grammar_processed, first)

#     print("FIRST sets:")
#     for nt in first:
#         print(f"First({nt}) = {{ {pretty_print(first[nt])} }}")
#     print("\nFOLLOW sets:")
#     for nt in follow:
#         print(f"Follow({nt}) = {{ {pretty_print(follow[nt])} }}")









# -*- coding: utf-8 -*-

import left_recursion  # must provide remove_left_recursion_if_any(path)

# ------------- IO -------------

def read_grammar_strings(filepath):
    """
    Read grammar where each line is: A -> α | β | ...
    Returns dict[str, list[str]] with productions as raw strings (ε kept literal).
    """
    grammar = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "->" not in line:
                continue
            A, rhs = line.split("->", 1)
            A = A.strip()
            prods = [p.strip() for p in rhs.split("|")]
            grammar[A] = prods
    return grammar

def tokenize_production(prod, nonterminals):
    """
    Longest-match tokenizer using known nonterminals (handles primes like A').
    Any unmatched character is treated as a single-character terminal.
    """
    if prod == "ε":
        return ["ε"]
    tokens = []
    i = 0
    nts_sorted = sorted(nonterminals, key=len, reverse=True)
    while i < len(prod):
        matched = False
        for nt in nts_sorted:
            L = len(nt)
            if prod[i:i+L] == nt:
                tokens.append(nt)
                i += L
                matched = True
                break
        if not matched:
            tokens.append(prod[i])
            i += 1
    return tokens

def strings_to_symbol_lists(grammar_str):
    """
    Convert dict[str, list[str]] -> dict[str, list[list[str]]] with tokenization by NT names.
    """
    nts = set(grammar_str.keys())
    out = {}
    for A, prods in grammar_str.items():
        out[A] = [tokenize_production(p, nts) for p in prods]
    return out

def symbol_lists_to_display(grammar_list):
    """
    Convert dict[str, list[list[str]]] to a printable string.
    """
    lines = []
    for A, prods in grammar_list.items():
        rhs = []
        for p in prods:
            if p == ["ε"]:
                rhs.append("ε")
            else:
                rhs.append("".join(p))
        lines.append(f"{A} -> {' | '.join(rhs)}")
    return "\n".join(lines)

# ------------- FIRST -------------

def compute_first(grammar):
    """
    grammar: dict[str, list[list[str]]] (symbols are NT names or terminals, ε literal)
    returns: dict[str, set[str]]
    """
    first = {}
    computing = set()

    def first_of(X):
        # Terminals (including ε): appear as symbols not in grammar keys
        if X not in grammar:
            return {X}
        if X in first:
            return first[X]
        if X in computing:
            # Break potential cycles; no new info added in this pass
            return set()
        computing.add(X)

        result = set()
        for production in grammar[X]:
            # ε production
            if production == ["ε"]:
                result.add("ε")
                continue
            nullable_prefix = True
            for sym in production:
                sym_first = first_of(sym) if sym in grammar else {sym}
                result |= (sym_first - {"ε"})
                if "ε" not in sym_first:
                    nullable_prefix = False
                    break
            if nullable_prefix:
                result.add("ε")
        computing.remove(X)
        first[X] = result
        return result

    for A in grammar:
        if A not in first:
            first_of(A)
    return first

# ------------- FOLLOW -------------

def compute_follow(grammar, first):
    """
    grammar: dict[str, list[list[str]]]
    first: dict[str, set[str]]
    returns: dict[str, set[str]]
    """
    follow = {A: set() for A in grammar}
    start = next(iter(grammar))
    follow[start].add("$")

    changed = True
    while changed:
        changed = False
        for A, prods in grammar.items():
            for prod in prods:
                n = len(prod)
                for i, B in enumerate(prod):
                    if B in grammar:
                        # Compute FIRST(beta) where beta = prod[i+1:]
                        beta = prod[i+1:]
                        add = set()
                        if beta:
                            j = 0
                            while j < len(beta):
                                sym = beta[j]
                                sym_first = first[sym] if sym in grammar else {sym}
                                add |= (sym_first - {"ε"})
                                if "ε" in sym_first:
                                    j += 1
                                else:
                                    break
                            else:
                                # all of beta can derive ε
                                add |= follow[A]
                        else:
                            # B at end of production
                            add |= follow[A]

                        if not add.issubset(follow[B]):
                            follow[B] |= add
                            changed = True
    return follow

# ------------- Pretty -------------

def pretty_set(S):
    return ", ".join(("∈" if x == "ε" else x) for x in sorted(S, key=lambda v: (v == "ε", v)))

# ------------- Orchestration -------------

def load_prepare_remove_lr_if_needed(filepath):
    """
    1) Ask left_recursion module to detect/remove LR from file.
    2) If it changed grammar, use the transformed grammar strings.
       Else, read original strings.
    3) Tokenize by nonterminal names for FIRST/FOLLOW.
    Returns: (grammar_list, changed, shown_text)
    """
    changed, transformed_str, report = left_recursion.remove_left_recursion_if_any(filepath)
    if changed:
        grammar_str = transformed_str
        shown_text = "\n".join(f"{A} -> {' | '.join(ps)}" for A, ps in grammar_str.items())
    else:
        grammar_str = read_grammar_strings(filepath)
        shown_text = "\n".join(f"{A} -> {' | '.join(ps)}" for A, ps in grammar_str.items())
    grammar_list = strings_to_symbol_lists(grammar_str)
    return grammar_list, changed, shown_text

if __name__ == "__main__":
    path = "grammar.txt"
    grammar, changed, shown = load_prepare_remove_lr_if_needed(path)

    print("Grammar after LR handling:")
    print(shown)

    first = compute_first(grammar)
    follow = compute_follow(grammar, first)

    print("\nFIRST sets:")
    for A in first:
        print(f"First({A}) = {{ {pretty_set(first[A])} }}")

    print("\nFOLLOW sets:")
    for A in follow:
        print(f"Follow({A}) = {{ {pretty_set(follow[A])} }}")
