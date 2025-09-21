# def left_factoring(grammar):
#     changed = True
#     while changed:
#         changed = False
#         new_grammar = {}
        
#         for nt, productions in grammar.items():
#             prefixes = {}
#             for prod in productions:
#                 prefix = prod[0] if prod else ''
#                 if prefix in prefixes:
#                     prefixes[prefix].append(prod)
#                 else:
#                     prefixes[prefix] = [prod]

#             if any(len(prods) > 1 for prods in prefixes.values()):
#                 changed = True
#                 new_grammar[nt] = []
#                 for prefix, prods in prefixes.items():
#                     if len(prods) > 1:
#                         new_nt = nt + "'"
#                         new_grammar[nt].append(prefix + new_nt)
#                         new_prods = [prod[1:] if len(prod) > 1 else 'ε' for prod in prods]
#                         new_grammar[new_nt] = new_prods
#                     else:
#                         new_grammar[nt].append(prods[0])
#             else:
#                 new_grammar[nt] = productions
        
#         grammar = new_grammar
    
#     return grammar

# def read_grammar_from_file(filepath):
#     grammar = {}
#     with open(filepath) as f:
#         for line in f:
#             if '->' in line:
#                 nt, rhs = line.strip().split("->")
#                 grammar[nt.strip()] = [prod.strip() for prod in rhs.split('|')]
#     return grammar

# def pretty_print_grammar(grammar):
#     for nt, prods in grammar.items():
#         print(f"{nt} -> {' | '.join(prods)}")


# # Example usage
# if __name__ == "__main__":
#     grammar = read_grammar_from_file("grammar.txt")
#     factored_grammar = left_factoring(grammar)
#     pretty_print_grammar(factored_grammar)













# -*- coding: utf-8 -*-

from collections import defaultdict

def read_grammar_from_file(filepath):
    grammar = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "->" not in line:
                continue
            nt, rhs = line.split("->", 1)
            nt = nt.strip()
            prods = [p.strip() for p in rhs.split("|")]
            grammar[nt] = prods
    return grammar

def write_grammar_to_file(filepath, grammar):
    with open(filepath, "w", encoding="utf-8") as f:
        for nt, prods in grammar.items():
            f.write(f"{nt} -> {' | '.join(prods)}\n")

def longest_common_prefix(a, b):
    i = 0
    L = min(len(a), len(b))
    while i < L and a[i] == b[i]:
        i += 1
    return a[:i]

def left_factoring(grammar):
    """
    Perform left factoring on a grammar whose productions are strings.
    Returns a new grammar dict[str, list[str]].
    """
    changed = True
    G = {A: list(Ps) for A, Ps in grammar.items()}

    while changed:
        changed = False
        newG = {}
        for A, prods in G.items():
            # Group by LCP clusters
            clusters = []
            used = [False]*len(prods)
            for i in range(len(prods)):
                if used[i]:
                    continue
                base = prods[i]
                group = [base]
                used[i] = True
                for j in range(i+1, len(prods)):
                    if used[j]:
                        continue
                    lcp = longest_common_prefix(base, prods[j])
                    if lcp:
                        group.append(prods[j])
                        used[j] = True
                clusters.append(group)

            newG[A] = []
            for group in clusters:
                if len(group) == 1:
                    # nothing to factor
                    newG[A].append(group[0])
                    continue
                # find actual LCP across whole group
                lcp = group[0]
                for s in group[1:]:
                    lcp = longest_common_prefix(lcp, s)
                    if not lcp:
                        break
                if not lcp:
                    # no common prefix across all; keep as is
                    newG[A].extend(group)
                    continue

                changed = True
                A_dash = A + "'"
                # ensure unique A' name if already exists
                while A_dash in G or A_dash in newG:
                    A_dash += "'"

                newG[A].append(lcp + A_dash)

                suffixes = []
                for s in group:
                    suf = s[len(lcp):]
                    suffixes.append(suf if suf else "ε")

                # add/extend A' rules
                if A_dash not in newG:
                    newG[A_dash] = []
                newG[A_dash].extend(suffixes)

                # Add any productions not in this group that don't start with lcp
                # Actually already handled because clusters were disjoint

        G = newG

    return G

def pretty_print_grammar(grammar):
    return "\n".join(f"{A} -> {' | '.join(Ps)}" for A, Ps in grammar.items())

if __name__ == "__main__":
    G = read_grammar_from_file("grammar.txt")
    factored = left_factoring(G)
    print(pretty_print_grammar(factored))
