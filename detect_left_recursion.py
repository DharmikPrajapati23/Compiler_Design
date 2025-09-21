from collections import defaultdict, deque

def read_grammar_from_file(filepath):
    """
    Reads grammar from a text file with lines like:
      A -> aB | b | Axy | ε
    Returns a dict[str, list[str]] with productions as raw strings (no tokenization).
    """
    grammar = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or '->' not in line:
                continue
            nt, rhs = line.split("->", 1)
            nt = nt.strip()
            prods = [p.strip() for p in rhs.split("|")]
            grammar[nt] = prods
    return grammar

def has_direct_left_recursion(grammar):
    """
    Direct left recursion: A -> A α
    Returns a dict NT -> list of left-recursive productions (strings) for quick reporting.
    """
    dlr = {}
    for A, prods in grammar.items():
        lr = [p for p in prods if p.startswith(A)]
        if lr:
            dlr[A] = lr
    return dlr  # empty dict means none

def build_first_symbol_graph(grammar):
    """
    Build a graph of nonterminals by first-symbol dependency.
    Edge A -> B exists if A has a production starting with nonterminal B.
    This is used to detect indirect left recursion via cycles reachable from A back to A.
    """
    graph = defaultdict(set)
    nts = set(grammar.keys())
    for A, prods in grammar.items():
        for p in prods:
            if not p:
                continue
            X = p[0]  # first character/symbol
            # If multi-letter nonterminals exist (e.g., Expr), adjust detection:
            # Here we assume single-letter nonterminals (consistent with your current project).
            if X in nts:
                graph[A].add(X)
    return graph

def has_indirect_left_recursion(grammar):
    """
    Indirect left recursion exists if there is a path A =>* A via first-symbol dependencies.
    Returns a dict NT -> True for NTs that participate in a left-recursive cycle.
    Also returns example cycle paths for reporting.
    """
    graph = build_first_symbol_graph(grammar)
    nts = list(grammar.keys())
    participates = {}
    cycles = {}

    def find_cycle(start):
        # DFS with path stack to find a cycle returning to start
        stack = [(start, [start])]
        visited_local = set()
        while stack:
            node, path = stack.pop()
            if node in visited_local:
                continue
            visited_local.add(node)
            for nxt in graph[node]:
                if nxt == start:
                    return path + [nxt]
                if nxt not in path:
                    stack.append((nxt, path + [nxt]))
        return None

    for A in nts:
        cycle = find_cycle(A)
        if cycle:
            participates[A] = True
            cycles[A] = cycle
    return participates, cycles

def detect_left_recursion(grammar):
    """
    Returns a structured report:
      {
        'has_direct': bool,
        'direct': {A: [productions]},
        'has_indirect': bool,
        'indirect_participants': {A: True ...},
        'indirect_cycles': {A: [cycle nodes ...]}
      }
    """
    direct = has_direct_left_recursion(grammar)
    indirect_flags, indirect_cycles = has_indirect_left_recursion(grammar)
    return {
        'has_direct': bool(direct),
        'direct': direct,
        'has_indirect': bool(indirect_flags),
        'indirect_participants': indirect_flags,
        'indirect_cycles': indirect_cycles
    }

def pretty_print_report(report):
    lines = []
    if report['has_direct']:
        lines.append("Direct Left Recursion found:")
        
    else:
        lines.append("No Direct Left Recursion.")
    if report['has_indirect']:
        lines.append("Indirect Left Recursion suspected (cycles in first-symbol graph):")
        
    else:
        lines.append("No Indirect Left Recursion detected by first-symbol dependency.")
    return "\n".join(lines)

if __name__ == "__main__":
    # Example usage on grammar.txt
    path = "grammar.txt"
    G = read_grammar_from_file(path)
    report = detect_left_recursion(G)
    print(pretty_print_report(report))
