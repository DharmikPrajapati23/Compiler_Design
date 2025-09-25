# import left_recursion
# import left_factoring
# import first_follow

# def read_strings(filepath):
#     """
#     Read grammar as dict[str, list[str]] (string productions).
#     """
#     G = {}
#     with open(filepath, "r", encoding="utf-8") as f:
#         for line in f:
#             line = line.strip()
#             if not line or "->" not in line:
#                 continue
#             A, rhs = line.split("->", 1)
#             A = A.strip()
#             G[A] = [p.strip() for p in rhs.split("|")]
#     return G

# def normalize_and_prepare(filepath):
#     """
#     Step 1: Ensure LL(1) preconditions as much as possible:
#       - Remove left recursion (direct/indirect) via left_recursion.remove_left_recursion_if_any
#       - Left-factor using left_factoring.left_factoring
#     Returns:
#       grammar_str (dict[str, list[str]]),
#       notes (list[str]) describing transforms applied.
#     """
#     notes = []
#     # 1) Remove left recursion if any
#     changed_lr, G_lr, report = left_recursion.remove_left_recursion_if_any(filepath)
#     if changed_lr:
#         notes.append("Left recursion was detected and removed.")
#         G = G_lr
#     else:
#         notes.append("No left recursion detected.")
#         G = read_strings(filepath)

#     # 2) Left factoring
#     G_factored = left_factoring.left_factoring(G)
#     if G_factored != G:
#         notes.append("Left factoring applied.")
#     else:
#         notes.append("No left factoring needed.")
#     return G_factored, notes

# def strings_to_symbol_lists(grammar_str):
#     """
#     Use first_follow tokenizer that keeps multi-character NTs like A'.
#     """
#     return first_follow.strings_to_symbol_lists(grammar_str)

# def compute_first_follow(grammar_list):
#     first = first_follow.compute_first(grammar_list)
#     follow = first_follow.compute_follow(grammar_list, first)
#     return first, follow

# def first_of_alpha(alpha, first, grammar_list):
#     """
#     Compute FIRST of a sequence α (list of symbols), using already computed FIRST sets.
#     Returns a set of terminals plus possibly 'ε'.
#     """
#     if alpha == []:
#         return {"ε"}
#     out = set()
#     for sym in alpha:
#         sym_first = first[sym] if sym in grammar_list else {sym}
#         out |= (sym_first - {"ε"})
#         if "ε" not in sym_first:
#             break
#     else:
#         out.add("ε")
#     return out

# def nonterminals_and_terminals(grammar_list):
#     nts = list(grammar_list.keys())
#     nts_set = set(nts)
#     terms = set()
#     for A, prods in grammar_list.items():
#         for p in prods:
#             for s in p:
#                 if s == "ε":
#                     continue
#                 if s not in nts_set:
#                     terms.add(s)
#     terms.add("$")  # end-marker for table
#     return nts, sorted(terms, key=lambda v: (v == "ε", v))

# def build_ll1_table(grammar_str):
#     """
#     Main table construction:
#       - Convert to list-symbol grammar
#       - Compute FIRST/FOLLOW
#       - Build table M[A, a] based on rules
#     Returns:
#       table: dict[A][a] -> production (string),
#       conflicts: list of (A, a, old, new) where multiple entries collide,
#       first, follow, grammar_list
#     """
#     grammar_list = strings_to_symbol_lists(grammar_str)
#     first, follow = compute_first_follow(grammar_list)
#     nts, terms = nonterminals_and_terminals(grammar_list)

#     # Initialize table with empty entries
#     table = {A: {t: "" for t in terms} for A in nts}
#     conflicts = []

#     # For each production A -> α
#     for A, prods in grammar_str.items():
#         for prod in prods:
#             # Tokenize α using the same tokenizer to be consistent
#             alpha = grammar_list[A][prods.index(prod)]
#             # Compute FIRST(α)
#             F = first_of_alpha(alpha if alpha != ["ε"] else [], first, grammar_list)
#             # Rule: for each terminal a in FIRST(α)\{ε}, add A -> prod to M[A,a]
#             for a in sorted(F - {"ε"}):
#                 existing = table[A].get(a, "")
#                 if existing and existing != f"{A} -> {prod}":
#                     conflicts.append((A, a, existing, f"{A} -> {prod}"))
#                 table[A][a] = f"{A} -> {prod}"
#             # If ε in FIRST(α), for each b in FOLLOW(A), add A -> ε to M[A,b]
#             if "ε" in F:
#                 for b in sorted(follow[A]):
#                     # Include $ if present in FOLLOW
#                     existing = table[A].get(b, "")
#                     if existing and existing != f"{A} -> {prod}":
#                         conflicts.append((A, b, existing, f"{A} -> {prod}"))
#                     table[A][b] = f"{A} -> {prod}"

#     return table, conflicts, first, follow, grammar_list, terms

# def pretty_table(table, terms):
#     # Create a simple aligned text table
#     nts = list(table.keys())
#     col_w = {t: max(len(t), max(len(table[A][t]) for A in nts)) for t in terms}
#     row_w = max(len(A) for A in nts)
#     # Header
#     header = " " * (row_w + 3) + " | ".join(t.ljust(col_w[t]) for t in terms)
#     sep = "-" * len(header)
#     rows = [header, sep]
#     for A in nts:
#         row = A.ljust(row_w) + " | " + " | ".join(table[A][t].ljust(col_w[t]) for t in terms)
#         rows.append(row)
#     return "\n".join(rows)

# def pretty_sets(first, follow):
#     lines = ["FIRST sets:"]
#     for A, S in first.items():
#         shown = ", ".join(("∈" if x == "ε" else x) for x in sorted(S, key=lambda v: (v == "ε", v)))
#         lines.append(f"First({A}) = {{ {shown} }}")
#     lines.append("\nFOLLOW sets:")
#     for A, S in follow.items():
#         shown = ", ".join(("∈" if x == "ε" else x) for x in sorted(S, key=lambda v: (v == "ε", v)))
#         lines.append(f"Follow({A}) = {{ {shown} }}")
#     return "\n".join(lines)

# def construct_ll1(filepath="grammar.txt"):
#     # Step 1: Preconditions (remove LR, apply left factoring)
#     grammar_str, notes = normalize_and_prepare(filepath)
#     # Step 2 and 3: FIRST/FOLLOW then table
#     table, conflicts, first, follow, grammar_list, terms = build_ll1_table(grammar_str)
#     return grammar_str, notes, first, follow, table, conflicts, terms

# if __name__ == "__main__":
#     path = "grammar.txt"
#     grammar_str, notes, first, follow, table, conflicts, terms = construct_ll1(path)

#     print("Precondition checks:")
#     for n in notes:
#         print(f"- {n}")

#     print("\nGrammar used (after preprocessing if any):")
#     for A, Ps in grammar_str.items():
#         print(f"{A} -> {' | '.join(Ps)}")

#     print("\n" + pretty_sets(first, follow))

#     print("\nLL(1) Parsing Table (rows: Nonterminals, columns: Terminals incl. $):")
#     print(pretty_table(table, terms))

#     if conflicts:
#         print("\nConflicts detected (grammar is not LL(1)):")
#         for A, a, old, new in conflicts:
#             print(f"  M[{A}, {a}] has conflict between [{old}] and [{new}]")
#     else:
#         print("\nNo conflicts; grammar appears LL(1).")


# ---------------------------------------------------------------------







# import left_recursion
# import left_factoring
# import first_follow

# def read_strings(filepath):
#     """
#     Read grammar as dict[str, list[str]] (string productions).
#     """
#     G = {}
#     with open(filepath, "r", encoding="utf-8") as f:
#         for line in f:
#             line = line.strip()
#             if not line or "->" not in line:
#                 continue
#             A, rhs = line.split("->", 1)
#             A = A.strip()
#             G[A] = [p.strip() for p in rhs.split("|")]
#     return G

# def normalize_and_prepare(filepath):
#     """
#     Step 1: Ensure LL(1) preconditions as much as possible:
#       - Remove left recursion (direct/indirect) via left_recursion.remove_left_recursion_if_any
#       - Left-factor using left_factoring.left_factoring
#     Returns:
#       grammar_str (dict[str, list[str]]),
#       notes (list[str]) describing transforms applied.
#     """
#     notes = []
#     # 1) Remove left recursion if any
#     changed_lr, G_lr, report = left_recursion.remove_left_recursion_if_any(filepath)
#     if changed_lr:
#         notes.append("Left recursion was detected and removed.")
#         G = G_lr
#     else:
#         notes.append("No left recursion detected.")
#         G = read_strings(filepath)

#     # 2) Left factoring
#     G_factored = left_factoring.left_factoring(G)
#     if G_factored != G:
#         notes.append("Left factoring applied.")
#     else:
#         notes.append("No left factoring needed.")
#     return G_factored, notes

# def strings_to_symbol_lists(grammar_str):
#     """
#     Use first_follow tokenizer that keeps multi-character NTs like A'.
#     """
#     return first_follow.strings_to_symbol_lists(grammar_str)

# def compute_first_follow(grammar_list):
#     first = first_follow.compute_first(grammar_list)
#     follow = first_follow.compute_follow(grammar_list, first)
#     return first, follow

# def first_of_alpha(alpha, first, grammar_list):
#     """
#     Compute FIRST of a sequence α (list of symbols), using already computed FIRST sets.
#     Returns a set of terminals plus possibly 'ε'.
#     """
#     if alpha == []:
#         return {"ε"}
#     out = set()
#     for sym in alpha:
#         sym_first = first[sym] if sym in grammar_list else {sym}
#         out |= (sym_first - {"ε"})
#         if "ε" not in sym_first:
#             break
#     else:
#         out.add("ε")
#     return out

# def nonterminals_and_terminals(grammar_list):
#     nts = list(grammar_list.keys())
#     nts_set = set(nts)
#     terms = set()
#     for A, prods in grammar_list.items():
#         for p in prods:
#             for s in p:
#                 if s == "ε":
#                     continue
#                 if s not in nts_set:
#                     terms.add(s)
#     terms.add("$")  # end-marker for table
#     return nts, sorted(terms, key=lambda v: (v == "ε", v))

# def build_ll1_table(grammar_str):
#     """
#     Main table construction:
#       - Convert to list-symbol grammar
#       - Compute FIRST/FOLLOW
#       - Build table M[A, a] based on rules
#     Returns:
#       table: dict[A][a] -> production (string),
#       conflicts: list of (A, a, old, new) where multiple entries collide,
#       first, follow, grammar_list
#     """
#     grammar_list = strings_to_symbol_lists(grammar_str)
#     first, follow = compute_first_follow(grammar_list)
#     nts, terms = nonterminals_and_terminals(grammar_list)

#     # Initialize table with empty entries
#     table = {A: {t: "" for t in terms} for A in nts}
#     conflicts = []

#     # For each production A -> α
#     for A, prods in grammar_str.items():
#         for prod in prods:
#             # Tokenize α using the same tokenizer to be consistent
#             alpha = grammar_list[A][prods.index(prod)]
#             # Compute FIRST(α)
#             F = first_of_alpha(alpha if alpha != ["ε"] else [], first, grammar_list)
#             # Rule: for each terminal a in FIRST(α)\{ε}, add A -> prod to M[A,a]
#             for a in sorted(F - {"ε"}):
#                 existing = table[A].get(a, "")
#                 if existing and existing != f"{A} -> {prod}":
#                     conflicts.append((A, a, existing, f"{A} -> {prod}"))
#                 table[A][a] = f"{A} -> {prod}"
#             # If ε in FIRST(α), for each b in FOLLOW(A), add A -> ε to M[A,b]
#             if "ε" in F:
#                 for b in sorted(follow[A]):
#                     # Include $ if present in FOLLOW
#                     existing = table[A].get(b, "")
#                     if existing and existing != f"{A} -> {prod}":
#                         conflicts.append((A, b, existing, f"{A} -> {prod}"))
#                     table[A][b] = f"{A} -> {prod}"

#     return table, conflicts, first, follow, grammar_list, terms

# def pretty_table(table, terms):
#     # Create a simple aligned text table
#     nts = list(table.keys())
#     col_w = {t: max(len(t), max(len(table[A][t]) for A in nts)) for t in terms}
#     row_w = max(len(A) for A in nts)
#     # Header
#     header = " " * (row_w + 3) + " | ".join(t.ljust(col_w[t]) for t in terms)
#     sep = "-" * len(header)
#     rows = [header, sep]
#     for A in nts:
#         row = A.ljust(row_w) + " | " + " | ".join(table[A][t].ljust(col_w[t]) for t in terms)
#         rows.append(row)
#     return "\n".join(rows)

# def pretty_sets(first, follow):
#     lines = ["FIRST sets:"]
#     for A, S in first.items():
#         shown = ", ".join(("∈" if x == "ε" else x) for x in sorted(S, key=lambda v: (v == "ε", v)))
#         lines.append(f"First({A}) = {{ {shown} }}")
#     lines.append("\nFOLLOW sets:")
#     for A, S in follow.items():
#         shown = ", ".join(("∈" if x == "ε" else x) for x in sorted(S, key=lambda v: (v == "ε", v)))
#         lines.append(f"Follow({A}) = {{ {shown} }}")
#     return "\n".join(lines)

# def construct_ll1(filepath="grammar.txt"):
#     # Step 1: Preconditions (remove LR, apply left factoring)
#     grammar_str, notes = normalize_and_prepare(filepath)
#     # Step 2 and 3: FIRST/FOLLOW then table
#     table, conflicts, first, follow, grammar_list, terms = build_ll1_table(grammar_str)
#     return grammar_str, notes, first, follow, table, conflicts, terms



# def tokenize_input(s):
#     """
#     Tokenize input string as a sequence of single-character terminals.
#     If terminals in the grammar are multi-char tokens, replace this
#     with a scanner consistent with your terminal set.
#     """
#     return list(s)

# # def parse(ll1_table, grammar_str, terms, input_string, start_symbol=None, trace=True):
# #     """
# #     LL(1) predictive parser.
# #     - ll1_table: dict[A][a] -> "A -> α" or ""
# #     - grammar_str: dict[str, list[str]] (string productions)
# #     - terms: list of terminal symbols including "$"
# #     - input_string: raw string of terminals (no spaces). Will append "$".
# #     - start_symbol: defaults to first nonterminal in grammar_str
# #     Returns: (accepted: bool, steps: list of (stack_str, input_str, action_str))
# #     """
# #     nts = list(grammar_str.keys())
# #     if start_symbol is None:
# #         start_symbol = nts[0]
# #     # Build a consistent tokenizer for RHS to push symbols as in FIRST/FOLLOW
# #     grammar_list = strings_to_symbol_lists(grammar_str)
# #     # Map RHS strings to token lists using same tokenization
# #     rhs_tokenized = {}
# #     for A, prods in grammar_str.items():
# #         rhs_tokenized[A] = []
# #         for i, p in enumerate(prods):
# #             rhs_tokenized[A].append(grammar_list[A][i])  # list of symbols

# #     stack = ["$", start_symbol]
# #     w = tokenize_input(input_string) + ["$"]
# #     ip = 0

# #     steps = []
# #     def snap(action):
# #         if trace:
# #             steps.append(("".join(stack), "".join(w[ip:]), action))

# #     snap("init")
# #     while True:
# #         X = stack[-1]
# #         a = w[ip]
# #         # Accept
# #         if X == "$" and a == "$":
# #             snap("accept")
# #             return True, steps
# #         # Terminal match
# #         if X not in grammar_str:
# #             if X == a:
# #                 stack.pop()
# #                 ip += 1
# #                 snap(f"match '{a}'")
# #                 continue
# #             else:
# #                 snap(f"error: expected '{X}', got '{a}'")
# #                 return False, steps
# #         # Nonterminal: consult table
# #         entry = ll1_table.get(X, {}).get(a, "")
# #         if not entry:
# #             snap(f"error: M[{X}, {a}] is empty")
# #             return False, steps
# #         # entry is "X -> α"
# #         _, rhs = entry.split("->", 1)
# #         rhs = rhs.strip()
# #         stack.pop()
# #         if rhs != "ε":
# #             # Push α in reverse (tokenized)
# #             # Find which production index this maps to for tokenization
# #             # Use first matching production text under X
# #             candidates = grammar_str[X]
# #             try:
# #                 k = candidates.index(rhs)
# #                 symbols = rhs_tokenized[X][k]
# #             except ValueError:
# #                 # fallback: naive character push
# #                 symbols = list(rhs)
# #             for sym in reversed(symbols):
# #                 if sym != "ε":
# #                     stack.append(sym)
# #         snap(entry)


# def render_stack(items):
#     if not items:
#         return ""
#     view = items[:]
#     view[-1] = f"{view[-1]}_"
#     return " ".join(view)

# def render_input_tail(unread):
#     if not unread:
#         return ""
#     return " ".join([f"_{unread[0]}"] + unread[1:])

# def parse(ll1_table, grammar_str, terms, input_string, start_symbol=None, trace=True):
#     nts = list(grammar_str.keys())
#     if start_symbol is None:
#         start_symbol = nts[0]

#     grammar_list = strings_to_symbol_lists(grammar_str)
#     rhs_tokenized = {A: [] for A in grammar_str}
#     for A, prods in grammar_str.items():
#         for i, p in enumerate(prods):
#             rhs_tokenized[A].append(grammar_list[A][i])

#     # Start with only bottom marker, as requested
#     stack = ["$"]
#     w = list(input_string) + ["$"]
#     ip = 0

#     steps = []  # (stack, input, action)

#     def push_row(action):
#         if trace:
#             steps.append((render_stack(stack), render_input_tail(w[ip:]), action))

#     # Row 1: show only "$" and decide the first action using start symbol with current lookahead
#     a = w[ip]
#     entry = ll1_table.get(start_symbol, {}).get(a, "")
#     if not entry:
#         push_row(f"error: M[{start_symbol}, {a}] is empty")
#         return False, steps
#     push_row(entry)  # Show first action on initial "$" row
#     # Apply first production: push RHS then S on top of "$" (simulate S at top)
#     # Since the board shows "$" first row and "$ S" next, emulate by pushing S then expanding
#     # Or push S first, then RHS for that action
#     # We'll push S, then expand it immediately according to entry
#     stack.append(start_symbol)
#     # Apply entry X -> rhs to the S just pushed
#     _, rhs = entry.split("->", 1)
#     rhs = rhs.strip()
#     stack.pop()  # pop S
#     if rhs != "ε":
#         try:
#             k = grammar_str[start_symbol].index(rhs)
#             symbols = rhs_tokenized[start_symbol][k]
#         except ValueError:
#             symbols = list(rhs)
#         for sym in reversed(symbols):
#             if sym != "ε":
#                 stack.append(sym)

#     # Main loop: now proceed with standard steps:
#     while True:
#         X = stack[-1] if stack else None
#         a = w[ip]

#         # Accept when only "$" remains and lookahead is "$"
#         if stack == ["$"] and a == "$":
#             push_row("accept")
#             return True, steps

#         if not X:
#             push_row("error: stack empty")
#             return False, steps

#         if X not in grammar_str:
#             if X == a:
#                 push_row(f"pop '{a}'")
#                 stack.pop()
#                 ip += 1
#                 continue
#             else:
#                 push_row(f"error: expected '{X}', got '{a}'")
#                 return False, steps

#         entry = ll1_table.get(X, {}).get(a, "")
#         if not entry:
#             push_row(f"error: M[{X}, {a}] is empty")
#             return False, steps

#         push_row(entry)
#         # apply production
#         _, rhs = entry.split("->", 1)
#         rhs = rhs.strip()
#         stack.pop()
#         if rhs != "ε":
#             try:
#                 k = grammar_str[X].index(rhs)
#                 symbols = rhs_tokenized[X][k]
#             except ValueError:
#                 symbols = list(rhs)
#             for sym in reversed(symbols):
#                 if sym != "ε":
#                     stack.append(sym)



# if __name__ == "__main__":
#     path = "grammar.txt"
#     grammar_str, notes, first, follow, table, conflicts, terms = construct_ll1(path)

#     print("Precondition checks:")
#     for n in notes:
#         print(f"- {n}")

#     print("\nGrammar used (after preprocessing if any):")
#     for A, Ps in grammar_str.items():
#         print(f"{A} -> {' | '.join(Ps)}")

#     print("\n" + pretty_sets(first, follow))

#     print("\nLL(1) Parsing Table (rows: Nonterminals, columns: Terminals incl. $):")
#     print(pretty_table(table, terms))

#     if conflicts:
#         print("\nConflicts detected (grammar is not LL(1)):")
#         for A, a, old, new in conflicts:
#             print(f"  M[{A}, {a}] conflict between [{old}] and [{new}]")
#     else:
#         print("\nNo conflicts; grammar appears LL(1).")
#         try:
#             test_input = input("\nEnter input string to parse (without $): ").strip()
#         except EOFError:
#             test_input = ""
#         if test_input:
#             accepted, steps = parse(table, grammar_str, terms, test_input)
#             print("\nTrace (Stack | Input | Action):")
#             for st, inp, act in steps:
#                 print(f"{st:<20} | {inp:<20} | {act}")
#             print("\nResult:", "ACCEPTED" if accepted else "REJECTED")


# ---------------------------------------









import left_recursion
import left_factoring
import first_follow

def read_strings(filepath):
    """
    Read grammar as dict[str, list[str]] (string productions).
    """
    G = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "->" not in line:
                continue
            A, rhs = line.split("->", 1)
            A = A.strip()
            G[A] = [p.strip() for p in rhs.split("|")]
    return G

def normalize_and_prepare(filepath):
    """
    Step 1: Ensure LL(1) preconditions as much as possible:
      - Remove left recursion (direct/indirect) via left_recursion.remove_left_recursion_if_any
      - Left-factor using left_factoring.left_factoring
    Returns:
      grammar_str (dict[str, list[str]]),
      notes (list[str]) describing transforms applied.
    """
    notes = []
    # 1) Remove left recursion if any
    changed_lr, G_lr, report = left_recursion.remove_left_recursion_if_any(filepath)
    if changed_lr:
        notes.append("Left recursion was detected and removed.")
        G = G_lr
    else:
        notes.append("No left recursion detected.")
        G = read_strings(filepath)

    # 2) Left factoring
    G_factored = left_factoring.left_factoring(G)
    if G_factored != G:
        notes.append("Left factoring applied.")
    else:
        notes.append("No left factoring needed.")
    return G_factored, notes

def strings_to_symbol_lists(grammar_str):
    """
    Use first_follow tokenizer that keeps multi-character NTs like A'.
    """
    return first_follow.strings_to_symbol_lists(grammar_str)

def compute_first_follow(grammar_list):
    first = first_follow.compute_first(grammar_list)
    follow = first_follow.compute_follow(grammar_list, first)
    return first, follow

def first_of_alpha(alpha, first, grammar_list):
    """
    Compute FIRST of a sequence α (list of symbols), using already computed FIRST sets.
    Returns a set of terminals plus possibly 'ε'.
    """
    if alpha == []:
        return {"ε"}
    out = set()
    for sym in alpha:
        sym_first = first[sym] if sym in grammar_list else {sym}
        out |= (sym_first - {"ε"})
        if "ε" not in sym_first:
            break
    else:
        out.add("ε")
    return out

def nonterminals_and_terminals(grammar_list):
    nts = list(grammar_list.keys())
    nts_set = set(nts)
    terms = set()
    for A, prods in grammar_list.items():
        for p in prods:
            for s in p:
                if s == "ε":
                    continue
                if s not in nts_set:
                    terms.add(s)
    terms.add("$")  # end-marker for table
    return nts, sorted(terms, key=lambda v: (v == "ε", v))

def build_ll1_table(grammar_str):
    """
    Main table construction:
      - Convert to list-symbol grammar
      - Compute FIRST/FOLLOW
      - Build table M[A, a] based on rules
    Returns:
      table: dict[A][a] -> production (string),
      conflicts: list of (A, a, old, new) where multiple entries collide,
      first, follow, grammar_list
    """
    grammar_list = strings_to_symbol_lists(grammar_str)
    first, follow = compute_first_follow(grammar_list)
    nts, terms = nonterminals_and_terminals(grammar_list)

    # Initialize table with empty entries
    table = {A: {t: "" for t in terms} for A in nts}
    conflicts = []

    # For each production A -> α
    for A, prods in grammar_str.items():
        for prod in prods:
            # Tokenize α using the same tokenizer to be consistent
            alpha = grammar_list[A][prods.index(prod)]
            # Compute FIRST(α)
            F = first_of_alpha(alpha if alpha != ["ε"] else [], first, grammar_list)
            # Rule: for each terminal a in FIRST(α)\{ε}, add A -> prod to M[A,a]
            for a in sorted(F - {"ε"}):
                existing = table[A].get(a, "")
                if existing and existing != f"{A} -> {prod}":
                    conflicts.append((A, a, existing, f"{A} -> {prod}"))
                table[A][a] = f"{A} -> {prod}"
            # If ε in FIRST(α), for each b in FOLLOW(A), add A -> ε to M[A,b]
            if "ε" in F:
                for b in sorted(follow[A]):
                    # Include $ if present in FOLLOW
                    existing = table[A].get(b, "")
                    if existing and existing != f"{A} -> {prod}":
                        conflicts.append((A, b, existing, f"{A} -> {prod}"))
                    table[A][b] = f"{A} -> {prod}"

    return table, conflicts, first, follow, grammar_list, terms

def pretty_table(table, terms):
    # Create a simple aligned text table
    nts = list(table.keys())
    col_w = {t: max(len(t), max(len(table[A][t]) for A in nts)) for t in terms}
    row_w = max(len(A) for A in nts)
    # Header
    header = " " * (row_w + 3) + " | ".join(t.ljust(col_w[t]) for t in terms)
    sep = "-" * len(header)
    rows = [header, sep]
    for A in nts:
        row = A.ljust(row_w) + " | " + " | ".join(table[A][t].ljust(col_w[t]) for t in terms)
        rows.append(row)
    return "\n".join(rows)

def pretty_table_tabulate(table, terms):
    """
    Pretty LL(1) table using tabulate for console output.
    Returns a string. Requires: pip install tabulate
    """
    from tabulate import tabulate

    nts = list(table.keys())
    headers = ["NT \\ lookahead"] + terms
    data = []
    for A in nts:
        row = [A]
        for t in terms:
            cell = table[A].get(t, "")
            row.append(cell if cell else "")
        data.append(row)
    return tabulate(data, headers=headers, tablefmt="grid", stralign="left")



def ll1_table_as_rows(table, terms):
    """
    Return headers and rows for Streamlit st.table()/st.dataframe().
    headers: list[str]
    rows: list[list[str]]
    """
    nts = list(table.keys())
    headers = ["NT \\ lookahead"] + terms
    rows = []
    for A in nts:
        row = [A]
        for t in terms:
            row.append(table[A].get(t, ""))
        rows.append(row)
    return headers, rows




def pretty_sets(first, follow):
    lines = ["FIRST sets:"]
    for A, S in first.items():
        shown = ", ".join(("∈" if x == "ε" else x) for x in sorted(S, key=lambda v: (v == "ε", v)))
        lines.append(f"First({A}) = {{ {shown} }}")
    lines.append("\nFOLLOW sets:")
    for A, S in follow.items():
        shown = ", ".join(("∈" if x == "ε" else x) for x in sorted(S, key=lambda v: (v == "ε", v)))
        lines.append(f"Follow({A}) = {{ {shown} }}")
    return "\n".join(lines)

def construct_ll1(filepath="grammar.txt"):
    # Step 1: Preconditions (remove LR, apply left factoring)
    grammar_str, notes = normalize_and_prepare(filepath)
    # Step 2 and 3: FIRST/FOLLOW then table
    table, conflicts, first, follow, grammar_list, terms = build_ll1_table(grammar_str)
    return grammar_str, notes, first, follow, table, conflicts, terms



def tokenize_input(s):
    """
    Tokenize input string as a sequence of single-character terminals.
    If terminals in the grammar are multi-char tokens, replace this
    with a scanner consistent with your terminal set.
    """
    return list(s)

def parse(ll1_table, grammar_str, terms, input_string, start_symbol=None, trace=True):
    """
    LL(1) predictive parser.
    - ll1_table: dict[A][a] -> "A -> α" or ""
    - grammar_str: dict[str, list[str]] (string productions)
    - terms: list of terminal symbols including "$"
    - input_string: raw string of terminals (no spaces). Will append "$".
    - start_symbol: defaults to first nonterminal in grammar_str
    Returns: (accepted: bool, steps: list of (stack_str, input_str, action_str))
    """
    nts = list(grammar_str.keys())
    if start_symbol is None:
        start_symbol = nts[0]
    # Build a consistent tokenizer for RHS to push symbols as in FIRST/FOLLOW
    grammar_list = strings_to_symbol_lists(grammar_str)
    # Map RHS strings to token lists using same tokenization
    rhs_tokenized = {}
    for A, prods in grammar_str.items():
        rhs_tokenized[A] = []
        for i, p in enumerate(prods):
            rhs_tokenized[A].append(grammar_list[A][i])  # list of symbols

    stack = ["$", start_symbol]
    w = tokenize_input(input_string) + ["$"]
    ip = 0

    steps = []
    def snap(action):
        if trace:
            steps.append(("".join(stack), "".join(w[ip:]), action))

    snap("init")
    while True:
        X = stack[-1]
        a = w[ip]
        # Accept
        if X == "$" and a == "$":
            snap("accept")
            return True, steps
        # Terminal match
        if X not in grammar_str:
            if X == a:
                stack.pop()
                ip += 1
                snap(f"match '{a}'")
                continue
            else:
                snap(f"error: expected '{X}', got '{a}'")
                return False, steps
        # Nonterminal: consult table
        entry = ll1_table.get(X, {}).get(a, "")
        if not entry:
            snap(f"error: M[{X}, {a}] is empty")
            return False, steps
        # entry is "X -> α"
        _, rhs = entry.split("->", 1)
        rhs = rhs.strip()
        stack.pop()
        if rhs != "ε":
            # Push α in reverse (tokenized)
            # Find which production index this maps to for tokenization
            # Use first matching production text under X
            candidates = grammar_str[X]
            try:
                k = candidates.index(rhs)
                symbols = rhs_tokenized[X][k]
            except ValueError:
                # fallback: naive character push
                symbols = list(rhs)
            for sym in reversed(symbols):
                if sym != "ε":
                    stack.append(sym)
        snap(entry)



if __name__ == "__main__":
    path = "grammar.txt"
    grammar_str, notes, first, follow, table, conflicts, terms = construct_ll1(path)

    print("Precondition checks:")
    for n in notes:
        print(f"- {n}")

    print("\nGrammar used (after preprocessing if any):")
    for A, Ps in grammar_str.items():
        print(f"{A} -> {' | '.join(Ps)}")

    print("\n" + pretty_sets(first, follow))

    # print("\nLL(1) Parsing Table (rows: Nonterminals, columns: Terminals incl. $):")
    # print(pretty_table(table, terms))
    print("\nLL(1) Parsing Table (rows: Nonterminals, columns: Terminals incl. $):")
    try:
        print(pretty_table_tabulate(table, terms))
    except Exception:
        # Fallback to your existing monospace formatter
        print(pretty_table(table, terms))

    if conflicts:
        print("\nConflicts detected (grammar is not LL(1)):")
        for A, a, old, new in conflicts:
            print(f"  M[{A}, {a}] conflict between [{old}] and [{new}]")
    else:
        print("\nNo conflicts; grammar appears LL(1).")
        try:
            test_input = input("\nEnter input string to parse (without $): ").strip()
        except EOFError:
            test_input = ""
        if test_input:
            accepted, steps = parse(table, grammar_str, terms, test_input)
            print("\nTrace (Stack | Input | Action):")
            for st, inp, act in steps:
                print(f"{st:<20} | {inp:<20} | {act}")
            print("\nResult:", "ACCEPTED" if accepted else "REJECTED")



















