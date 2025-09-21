# def remove_left_recursion(grammar):
#     new_grammar = {}
#     for non_terminal, productions in grammar.items():
#         left_recursive = []
#         non_left_recursive = []
#         for prod in productions:
#             if prod.startswith(non_terminal):
#                 left_recursive.append(prod[len(non_terminal):])
#             else:
#                 non_left_recursive.append(prod)
#         if left_recursive:
#             new_non_terminal = non_terminal + "'"
#             new_grammar[non_terminal] = []
#             for prod in non_left_recursive:
#                 new_grammar[non_terminal].append(f"{prod}{new_non_terminal}")
#             new_grammar[new_non_terminal] = []
#             for prod in left_recursive:
#                 new_grammar[new_non_terminal].append(f"{prod}{new_non_terminal}")
#             new_grammar[new_non_terminal].append("ε")
#         else:
#             new_grammar[non_terminal] = productions
#     return new_grammar

# def read_grammar_from_file(filepath):
#     grammar = {}
#     with open(filepath) as f:
#         for line in f:
#             if '->' in line:
#                 nt, rhs = line.strip().split("->")
#                 grammar[nt.strip()] = [prod.strip() for prod in rhs.split('|')]
#     return grammar









# -*- coding: utf-8 -*-

from collections import defaultdict
import detect_left_recursion as detector  # your file from previous step

# ---------- IO ----------

def read_grammar_from_file(filepath):
    return detector.read_grammar_from_file(filepath)

def pretty_print_grammar(grammar):
    return "\n".join(f"{A} -> {' | '.join(prods)}" for A, prods in grammar.items())

def pretty_print_report(report):
    lines = []
    if report['has_direct']:
        lines.append("Direct Left Recursion found:")
        # for A, prods in report['direct'].items():
        #     lines.append(f"  {A}: " + " | ".join(prods))
    else:
        lines.append("No Direct Left Recursion.")
    if report['has_indirect']:
        lines.append("Indirect Left Recursion suspected (cycles in first-symbol graph):")
        # for A, cyc in report['indirect_cycles'].items():
        #     lines.append("  " + " -> ".join(cyc))
    else:
        lines.append("No Indirect Left Recursion detected.")
    return "\n".join(lines)

# ---------- Removal helpers ----------

def _remove_direct_left_recursion_for(A, prods):
    """
    Transform immediate LR on A’s productions.
    Returns (new_A_rules, (A_prime, A_prime_rules)) or (prods, None) if no direct LR.
    """
    alphas, betas = [], []
    for p in prods:
        if p.startswith(A):
            alphas.append(p[len(A):])
        else:
            betas.append(p)
    if not alphas:
        return prods, None
    A_prime = A + "'"
    new_A = [beta + A_prime for beta in betas] if betas else [A_prime]
    new_Ap = [alpha + A_prime for alpha in alphas] + ["ε"]
    return new_A, (A_prime, new_Ap)

def _eliminate_all_left_recursion(grammar):
    """
    Standard ordering algorithm to remove indirect then direct LR.
    grammar: dict[str, list[str]] with raw string productions.
    """
    nts = list(grammar.keys())
    G = {A: list(prods) for A, prods in grammar.items()}

    for i, Ai in enumerate(nts):
        # Expand Ai rules that begin with earlier Aj
        for j in range(i):
            Aj = nts[j]
            expanded = []
            for p in G[Ai]:
                if p.startswith(Aj):
                    suffix = p[len(Aj):]
                    for delta in G[Aj]:
                        expanded.append(delta + suffix)
                else:
                    expanded.append(p)
            G[Ai] = expanded
        # Remove immediate LR on Ai
        replaced, aprime = _remove_direct_left_recursion_for(Ai, G[Ai])
        G[Ai] = replaced
        if aprime:
            A_prime, rules = aprime
            # Insert or extend A' rules
            if A_prime not in G:
                G[A_prime] = rules
            else:
                G[A_prime].extend(rules)
    return G

# ---------- Public API ----------

def remove_left_recursion_if_any(filepath):
    """
    1) Read grammar
    2) Detect LR using detector
    3) If none: return (False, grammar, report)
    4) Else: eliminate all LR and return (True, transformed, report)
    """
    grammar = read_grammar_from_file(filepath)
    report = detector.detect_left_recursion(grammar)
    has_lr = report['has_direct'] or report['has_indirect']
    if not has_lr:
        return False, grammar, report
    transformed = _eliminate_all_left_recursion(grammar)
    return True, transformed, report

# ---------- CLI ----------

if __name__ == "__main__":
    path = "grammar.txt"
    changed, outG, rep = remove_left_recursion_if_any(path)
    print(pretty_print_report(rep))
    if changed:
        print("\nTransformed grammar (no left recursion):")
        print(pretty_print_grammar(outG))
    else:
        print("\nNo left recursion in the given grammar.")
