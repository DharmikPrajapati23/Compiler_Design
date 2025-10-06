# # lro.py
# # -*- coding: utf-8 -*-

# from collections import defaultdict, deque

# # ---------- IO and tokenization ----------

# def read_strings(filepath):
#     """
#     Read grammar where each line is: A -> α | β | ...
#     Returns dict[str, list[str]] with string productions (ε kept literal).
#     """
#     G = {}
#     with open(filepath, "r", encoding="utf-8") as f:
#         for line in f:
#             line = line.strip()
#             if not line or "->" not in line:
#                 continue
#             A, rhs = line.split("->", 1)
#             A = A.strip()
#             prods = [p.strip() for p in rhs.split("|")]
#             G[A] = prods
#     return G

# def tokenize_production(prod, nonterminals):
#     """
#     Longest-match tokenizer over known nonterminals; fallback 1-char terminals.
#     """
#     if prod == "ε":
#         return ["ε"]
#     toks = []
#     i = 0
#     nts = sorted(nonterminals, key=len, reverse=True)
#     while i < len(prod):
#         matched = False
#         for nt in nts:
#             L = len(nt)
#             if prod[i:i+L] == nt:
#                 toks.append(nt)
#                 i += L
#                 matched = True
#                 break
#         if not matched:
#             toks.append(prod[i])
#             i += 1
#     return toks

# def to_symbol_lists(Gstr):
#     nts = set(Gstr.keys())
#     Glst = {}
#     for A, prods in Gstr.items():
#         Glst[A] = [tokenize_production(p, nts) for p in prods]
#     return Glst

# # ---------- Augmentation ----------

# def augment_grammar(Gstr):
#     """
#     Add a new start S' with S' -> S where S is the first key.
#     Returns augmented string-grammar and start symbols (S_dash, S).
#     """
#     if not Gstr:
#         raise ValueError("Empty grammar.")
#     S = next(iter(Gstr))
#     S_dash = S + "'"
#     while S_dash in Gstr:
#         S_dash += "'"
#     Gaug = {S_dash: [S]}
#     Gaug.update(Gstr)
#     return Gaug, S_dash, S

# # ---------- LR(0) items ----------

# def items_for(A, prod_syms):
#     """
#     Generate LR(0) items as tuples (A, tuple(prod_syms), dot_pos).
#     """
#     p = tuple(prod_syms)
#     for i in range(len(p)+1):
#         yield (A, p, i)

# def is_nonterminal(X, Glst):
#     return X in Glst

# def closure(I, Glst):
#     """
#     I: set of items (A, prod_tuple, dot_pos)
#     Glst: dict[str, list[list[str]]]
#     """
#     changed = True
#     I = set(I)
#     while changed:
#         changed = False
#         to_add = []
#         for (A, p, dot) in I:
#             if dot < len(p):
#                 X = p[dot]
#                 if is_nonterminal(X, Glst):
#                     for prod in Glst[X]:
#                         it = (X, tuple(prod), 0)
#                         if it not in I:
#                             to_add.append(it)
#         if to_add:
#             I.update(to_add)
#             changed = True
#     return I

# def goto(I, X, Glst):
#     """
#     Move dot over symbol X.
#     """
#     J = set()
#     for (A, p, dot) in I:
#         if dot < len(p) and p[dot] == X:
#             J.add((A, p, dot+1))
#     if not J:
#         return set()
#     return closure(J, Glst)




# def symbol_order(Glst):
#     """
#     Return an ordered list of symbols for GOTO expansion:
#     nonterminals in dict insertion order, then terminals in sorted order.
#     """
#     nts = list(Glst.keys())
#     nts_set = set(nts)
#     terms = set()
#     for A, prods in Glst.items():
#         for p in prods:
#             for s in p:
#                 if s != "ε" and s not in nts_set:
#                     terms.add(s)
#     terms = sorted(terms, key=str)
#     return nts + terms

# def canonical_collection(Glst, S_dash):
#     # I0
#     start_prod = Glst[S_dash][0]
#     I0 = closure({(S_dash, tuple(start_prod), 0)}, Glst)

#     states = [I0]
#     trans = {}
#     work = deque([0])

#     ordered_symbols = symbol_order(Glst)

#     while work:
#         i = work.popleft()
#         I = states[i]
#         for X in ordered_symbols:
#             J = goto(I, X, Glst)
#             if not J:
#                 continue
#             # Check for existing
#             for idx, st in enumerate(states):
#                 if st == J:
#                     trans[(i, X)] = idx
#                     break
#             else:
#                 states.append(J)
#                 j = len(states) - 1
#                 trans[(i, X)] = j
#                 work.append(j)
#     return states, trans


# # ---------- Pretty printing ----------

# def item_to_str(item):
#     A, p, dot = item
#     syms = list(p)
#     syms.insert(dot, "•")
#     return f"{A} -> {' '.join(syms) if syms else '•'}"

# def state_to_str(idx, I, nt_index, prod_index):
#     lines = [f"I{idx}:"]
#     def item_key(it):
#         A, p, dot = it
#         return (nt_index.get(A, 1_000_000),
#                 prod_index.get((A, p), 1_000_000),
#                 dot)
#     for it in sorted(I, key=item_key):
#         lines.append("  " + item_to_str(it))
#     return "\n".join(lines)


# def build_order_indices(Gaug):
#     """
#     Returns:
#       nt_index: dict[NT] -> rank by appearance in Gaug keys (S', S, A, ...)
#       prod_index: dict[(NT, tuple(prod_syms))] -> rank by appearance within NT
#     """
#     nt_index = {A: i for i, A in enumerate(Gaug.keys())}
#     # Tokenize to build consistent prod keys
#     Glst_tmp = to_symbol_lists(Gaug)
#     prod_index = {}
#     for A, prods in Glst_tmp.items():
#         for k, p in enumerate(prods):
#             prod_index[(A, tuple(p))] = k
#     return nt_index, prod_index




# def transitions_to_str(trans):
#     by_src = defaultdict(list)
#     for (i, X), j in trans.items():
#         by_src[i].append((X, j))
#     lines = ["\nGOTO transitions:"]
#     for i in sorted(by_src.keys()):
#         moves = ", ".join(f"on {X} -> I{j}" for X, j in sorted(by_src[i], key=lambda t: (t[0] != "$", str(t[0]))))
#         lines.append(f"  I{i}: {moves}")
#     return "\n".join(lines)

# # ---------- Orchestration ----------

# def build_lr0(filepath="grammar.txt"):
#     Gstr = read_strings(filepath)
#     Gaug, S_dash, S = augment_grammar(Gstr)
#     Glst = to_symbol_lists(Gaug)
#     states, trans = canonical_collection(Glst, S_dash)
#     return Gaug, Glst, S_dash, S, states, trans








# # ---------- LR(0) Table ----------

# def collect_terminals_nonterminals(Glst):
#     nts = list(Glst.keys())
#     nts_set = set(nts)
#     terms = set()
#     for A, prods in Glst.items():
#         for p in prods:
#             for s in p:
#                 if s != "ε" and s not in nts_set:
#                     terms.add(s)
#     return nts, sorted(terms, key=str)

# def build_lr0_table(Glst, S_dash, states, trans):
#     """
#     Returns:
#       ACTION: dict[i][a] -> 's j' | 'r A->α' | 'acc' | ''
#       GOTO:   dict[i][A] -> j | ''
#       conflicts: list of (i, symbol, old, new)
#     """
#     nts, terms = collect_terminals_nonterminals(Glst)
#     # Include end-marker for ACTION only
#     action_terms = terms + ["$"]

#     ACTION = {i: {a: "" for a in action_terms} for i in range(len(states))}
#     GOTO   = {i: {A: "" for A in nts} for i in range(len(states))}
#     conflicts = []

#     # Map transitions for easy lookup
#     # trans[(i, X)] = j already provided

#     # Fill shift and goto from transitions
#     for (i, X), j in trans.items():
#         if X in nts:  # nonterminal
#             if GOTO[i][X] != "" and GOTO[i][X] != j:
#                 conflicts.append((i, X, f"{GOTO[i][X]}", f"{j}"))
#             GOTO[i][X] = j
#         else:  # terminal
#             # shift on terminal X
#             old = ACTION[i].get(X, "")
#             new = f"s {j}"
#             if old and old != new:
#                 conflicts.append((i, X, old, new))
#             ACTION[i][X] = new

#     # Fill reduces and accept from items
#     for i, I in enumerate(states):
#         for (A, p, dot) in I:
#             if dot == len(p):  # complete item
#                 if A == S_dash:
#                     # Accept on $
#                     old = ACTION[i].get("$", "")
#                     new = "acc"
#                     if old and old != new:
#                         conflicts.append((i, "$", old, new))
#                     ACTION[i]["$"] = new
#                 else:
#                     # reduce A -> p on all terminals (LR(0) reduces on all lookaheads)
#                     prod_str = " ".join(p) if p else "ε"
#                     new = f"r {A}->{prod_str}"
#                     for a in ACTION[i].keys():
#                         old = ACTION[i][a]
#                         if old and old != new:
#                             conflicts.append((i, a, old, new))
#                         ACTION[i][a] = new

#     return ACTION, GOTO, terms, nts, conflicts

# def lr0_table_to_text(ACTION, GOTO, terms, nts):
#     """
#     Render a combined table with ACTION (terminals + $) and GOTO (nonterminals).
#     """
#     action_cols = terms + ["$"]
#     goto_cols = [A for A in nts if A != nts[0]]  # usually exclude S' in GOTO
#     headers = ["State"] + action_cols + goto_cols
#     rows = []
#     for i in range(len(ACTION)):
#         row = [f"I{i}"]
#         row += [ACTION[i].get(a, "") for a in action_cols]
#         row += [GOTO[i].get(A, "") for A in goto_cols]
#         rows.append(row)

#     # Pretty print with column widths
#     col_w = [max(len(h), max(len(str(r[c])) for r in rows)) for c, h in enumerate(headers)]
#     def fmt_row(vals):
#         return " | ".join(str(v).ljust(col_w[k]) for k, v in enumerate(vals))
#     sep = "-+-".join("-"*w for w in col_w)

#     lines = [fmt_row(headers), sep]
#     for r in rows:
#         lines.append(fmt_row(r))
#     return "\n".join(lines)






# def lr0_parse(input_string, ACTION, GOTO, terms, nts, states, Glst, S_dash):
#     """
#     Parse the input string using the LR(0) tables.
#     Prints a step-by-step trace: state stack | input | action.
#     """
#     stack = [0]  # always holds state numbers
#     w = list(input_string) + ['$']
#     ip = 0

#     trace = []

#     while True:
#         state = stack[-1]
#         lookahead = w[ip]
#         action = ACTION[state].get(lookahead, "")

#         # Prepare strings for pretty trace display
#         stack_str = " ".join(map(str, stack))
#         input_str = "".join(w[ip:])
#         act_str = action

#         trace.append((stack_str, input_str, act_str))

#         if action == "":
#             trace.append((stack_str, input_str, "ERROR"))
#             break
#         elif action.startswith("s "):  # shift
#             next_state = int(action[2:])
#             stack.append(lookahead)
#             stack.append(next_state)
#             ip += 1
#         elif action == "acc":
#             break
#         elif action.startswith("r "):  # reduce
#             # parse "r A->α"
#             prod = action[2:]
#             A, rhs = prod.split("->")
#             A = A.strip()
#             rhs_syms = rhs.strip().split()
#             if rhs_syms == ['ε']:
#                 m = 0
#             else:
#                 m = 2 * len(rhs_syms)
#             # Pop 2*|α| (state,symbol) pairs
#             for _ in range(m):
#                 stack.pop()
#             state_t = stack[-1]
#             stack.append(A)
#             next_state = GOTO[state_t][A]
#             stack.append(next_state)
#         else:
#             trace.append((stack_str, input_str, "ERROR"))
#             break

#     return trace



# def compute_first_follow(Glst):
#     nts = list(Glst.keys())
#     first = {X: set() for X in Glst}
#     changed = True
#     nts_set = set(nts)
#     while changed:
#         changed = False
#         for A in Glst:
#             for prod in Glst[A]:
#                 k = 0
#                 while k < len(prod):
#                     sym = prod[k]
#                     if sym == "ε":
#                         if "ε" not in first[A]:
#                             first[A].add("ε")
#                             changed = True
#                         break
#                     elif sym not in nts_set:
#                         if sym not in first[A]:
#                             first[A].add(sym)
#                             changed = True
#                         break
#                     else:
#                         added = first[sym] - {"ε"}
#                         if not added.issubset(first[A]):
#                             first[A].update(added)
#                             changed = True
#                         if "ε" not in first[sym]:
#                             break
#                     k += 1
#                 else:
#                     if "ε" not in first[A]:
#                         first[A].add("ε")
#                         changed = True
#     follow = {A: set() for A in Glst}
#     start_nt = list(Glst.keys())[1] if len(Glst) > 1 else list(Glst.keys())[0]
#     follow[start_nt].add('$')
#     changed = True
#     while changed:
#         changed = False
#         for A in Glst:
#             for prod in Glst[A]:
#                 for i, sym in enumerate(prod):
#                     if sym not in nts_set:
#                         continue
#                     after = prod[i+1:]
#                     fs = set()
#                     if after:
#                         k = 0
#                         while k < len(after):
#                             T = after[k]
#                             if T not in nts_set:
#                                 fs.add(T)
#                                 break
#                             else:
#                                 fs.update(first[T] - {"ε"})
#                                 if "ε" not in first[T]:
#                                     break
#                             k += 1
#                         else:
#                             fs.add("ε")
#                     else:
#                         fs.add("ε")
#                     if "ε" in fs:
#                         fs.discard("ε")
#                         if not follow[A].issubset(follow[sym]):
#                             follow[sym].update(follow[A])
#                             changed = True
#                     if not fs.issubset(follow[sym]):
#                         follow[sym].update(fs)
#                         changed = True
#     return first, follow

# def build_slr1_table(Glst, S_dash, states, trans):
#     nts, terms = collect_terminals_nonterminals(Glst)
#     action_terms = terms + ["$"]
#     first, follow = compute_first_follow(Glst)
#     ACTION = {i: {a: "" for a in action_terms} for i in range(len(states))}
#     GOTO   = {i: {A: "" for A in nts} for i in range(len(states))}
#     conflicts = []
#     # shift/goto transitions as in LR(0)
#     for (i, X), j in trans.items():
#         if X in nts:
#             GOTO[i][X] = j
#         else:
#             ACTION[i][X] = f"s {j}"
#     # REDUCE only for lookaheads in FOLLOW(A)
#     for i, I in enumerate(states):
#         for (A, p, dot) in I:
#             if dot == len(p):  # complete item
#                 if A == S_dash:
#                     ACTION[i]["$"] = "acc"
#                 else:
#                     prod_str = " ".join(p) if p else "ε"
#                     new = f"r {A}->{prod_str}"
#                     for a in follow[A]:
#                         old = ACTION[i][a]
#                         if old and old != "" and old != new:
#                             conflicts.append((i, a, old, new))
#                         ACTION[i][a] = new
#     return ACTION, GOTO, terms, nts, conflicts, follow



# if __name__ == "__main__":
#     # Build canonical LR(0) artifacts
#     Gaug, Glst, S_dash, S, states, trans = build_lr0("grammar.txt")

#     # Ordering indices so states print as: S', S, A ... and productions in file order
#     nt_index, prod_index = build_order_indices(Gaug)

#     print("Augmented grammar:")
#     for A, prods in Gaug.items():
#         print(f"{A} -> {' | '.join(prods)}")

#     print("\nCanonical LR(0) item sets:")
#     for i, I in enumerate(states):
#         print(state_to_str(i, I, nt_index, prod_index))

#     print(transitions_to_str(trans))

#     # ---- LR(0) parsing table ----
#     ACTION, GOTO, terms, nts, lr0_conflicts = build_lr0_table(Glst, S_dash, states, trans)
#     print("\nLR(0) Parsing Table")
#     print(lr0_table_to_text(ACTION, GOTO, terms, nts))
#     if lr0_conflicts:
#         print("\nLR(0) Conflicts:")
#         for i, sym, old, new in lr0_conflicts:
#             print(f"  State I{i}, on '{sym}': {old} vs {new}")
#     else:
#         print("\nNo conflicts in LR(0) table.")

#     # ---- SLR(1) parsing table ----
#     SLR_ACTION, SLR_GOTO, slr_terms, slr_nts, slr_conflicts, follow = build_slr1_table(Glst, S_dash, states, trans)
#     print("\nSLR(1) Parsing Table")
#     print(lr0_table_to_text(SLR_ACTION, SLR_GOTO, slr_terms, slr_nts))
#     if slr_conflicts:
#         print("\nSLR(1) Conflicts:")
#         for i, sym, old, new in slr_conflicts:
#             print(f"  State I{i}, on '{sym}': {old} vs {new}")
#     else:
#         print("\nNo conflicts in SLR(1) table.")

#     print("\nFOLLOW sets (for SLR(1)):")
#     for A in follow:
#         shown = ", ".join(sorted(follow[A]))
#         print(f"Follow({A}) = {{ {shown} }}")


#     # ---- Decide which traces to show ----
#     lr0_ok = (len(lr0_conflicts) == 0)
#     slr_ok = (len(slr_conflicts) == 0)

#     if not lr0_ok and not slr_ok:
#         print("\nBoth LR(0) and SLR(1) tables have conflicts. Parsing is disabled.")
#     else:
#         try:
#             inp = input("\nEnter input string to parse (without $): ").strip()
#         except EOFError:
#             inp = ""
#         if inp:
#             if lr0_ok:
#                 print("\nUsing LR(0) table for parsing")
#                 trace0 = lr0_parse(inp, ACTION, GOTO, terms, nts, states, Glst, S_dash)
#                 print("\n[LR(0) Trace] {:<24} | {:<18} | {}".format("STATE STACK", "INPUT", "ACTION"))
#                 print("-"*78)
#                 for stack_str, input_str, act in trace0:
#                     print("{:<24} | {:<18} | {}".format(stack_str, input_str, act))
#             else:
#                 print("\nLR(0) table has conflicts; skipping LR(0) parse.")

#             if slr_ok:
#                 print("\nUsing SLR(1) table for parsing")
#                 trace1 = lr0_parse(inp, SLR_ACTION, SLR_GOTO, slr_terms, slr_nts, states, Glst, S_dash)
#                 print("\n[SLR(1) Trace] {:<24} | {:<18} | {}".format("STATE STACK", "INPUT", "ACTION"))
#                 print("-"*80)
#                 for stack_str, input_str, act in trace1:
#                     print("{:<24} | {:<18} | {}".format(stack_str, input_str, act))
#             else:
#                 print("\nSLR(1) table has conflicts; skipping SLR(1) parse.")






























# lro.py
# -*- coding: utf-8 -*-

from collections import defaultdict, deque

# ---------- IO and tokenization ----------

def read_strings(filepath):
    G = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "->" not in line:
                continue
            A, rhs = line.split("->", 1)
            A = A.strip()
            prods = [p.strip() for p in rhs.split("|")]
            G[A] = prods
    return G


def tokenize_production(prod, nonterminals):
    # ε is empty RHS
    if prod == "ε" or prod == "":
        return []  # empty production
    toks = []
    i = 0
    nts = sorted(nonterminals, key=len, reverse=True)
    while i < len(prod):
        matched = False
        for nt in nts:
            L = len(nt)
            if prod[i:i+L] == nt:
                toks.append(nt)
                i += L
                matched = True
                break
        if not matched:
            toks.append(prod[i])
            i += 1
    return toks



def to_symbol_lists(Gstr):
    nts = set(Gstr.keys())
    Glst = {}
    for A, prods in Gstr.items():
        Glst[A] = [tokenize_production(p, nts) for p in prods]
    return Glst

# ---------- Augmentation ----------

def augment_grammar(Gstr):
    """
    Add a new start S' with S' -> S where S is the first key.
    Returns augmented string-grammar and start symbols (S_dash, S).
    """
    if not Gstr:
        raise ValueError("Empty grammar.")
    S = next(iter(Gstr))
    S_dash = S + "'"
    while S_dash in Gstr:
        S_dash += "'"
    Gaug = {S_dash: [S]}
    Gaug.update(Gstr)
    return Gaug, S_dash, S

# ---------- LR(0) items ----------

def items_for(A, prod_syms):
    """
    Generate LR(0) items as tuples (A, tuple(prod_syms), dot_pos).
    """
    p = tuple(prod_syms)
    for i in range(len(p)+1):
        yield (A, p, i)

def is_nonterminal(X, Glst):
    return X in Glst

def closure(I, Glst):
    """
    I: set of items (A, prod_tuple, dot_pos)
    Glst: dict[str, list[list[str]]]
    """
    changed = True
    I = set(I)
    while changed:
        changed = False
        to_add = []
        for (A, p, dot) in I:
            if dot < len(p):
                X = p[dot]
                if is_nonterminal(X, Glst):
                    for prod in Glst[X]:
                        it = (X, tuple(prod), 0)
                        if it not in I:
                            to_add.append(it)
        if to_add:
            I.update(to_add)
            changed = True
    return I

def goto(I, X, Glst):
    """
    Move dot over symbol X.
    """
    J = set()
    for (A, p, dot) in I:
        if dot < len(p) and p[dot] == X:
            J.add((A, p, dot+1))
    if not J:
        return set()
    return closure(J, Glst)




def symbol_order(Glst):
    """
    Return an ordered list of symbols for GOTO expansion:
    nonterminals in dict insertion order, then terminals in sorted order.
    """
    nts = list(Glst.keys())
    nts_set = set(nts)
    terms = set()
    for A, prods in Glst.items():
        for p in prods:
            for s in p:
                if s != "ε" and s not in nts_set:
                    terms.add(s)
    terms = sorted(terms, key=str)
    return nts + terms

def canonical_collection(Glst, S_dash):
    # I0
    start_prod = Glst[S_dash][0]
    I0 = closure({(S_dash, tuple(start_prod), 0)}, Glst)

    states = [I0]
    trans = {}
    work = deque([0])

    ordered_symbols = symbol_order(Glst)

    while work:
        i = work.popleft()
        I = states[i]
        for X in ordered_symbols:
            J = goto(I, X, Glst)
            if not J:
                continue
            # Check for existing
            for idx, st in enumerate(states):
                if st == J:
                    trans[(i, X)] = idx
                    break
            else:
                states.append(J)
                j = len(states) - 1
                trans[(i, X)] = j
                work.append(j)
    return states, trans


# ---------- Pretty printing ----------
def item_to_str(item):
    A, p, dot = item
    syms = list(p)
    syms.insert(dot, "•")
    body = ' '.join(syms) if syms else '•'
    # For completed empty production, show A -> ε • or A -> • ? Usually A -> • means start of empty;
    # Use a clearer print for empty:
    if len(p) == 0:
        # dot can be 0 only; completed equals dot==0
        if dot == 0:
            return f"{A} -> •"  # canonical; optional: f"{A} -> ε •"
    return f"{A} -> {body}"


def state_to_str(idx, I, nt_index, prod_index):
    lines = [f"I{idx}:"]
    def item_key(it):
        A, p, dot = it
        return (nt_index.get(A, 1_000_000),
                prod_index.get((A, p), 1_000_000),
                dot)
    for it in sorted(I, key=item_key):
        lines.append("  " + item_to_str(it))
    return "\n".join(lines)


def build_order_indices(Gaug):
    """
    Returns:
      nt_index: dict[NT] -> rank by appearance in Gaug keys (S', S, A, ...)
      prod_index: dict[(NT, tuple(prod_syms))] -> rank by appearance within NT
    """
    nt_index = {A: i for i, A in enumerate(Gaug.keys())}
    # Tokenize to build consistent prod keys
    Glst_tmp = to_symbol_lists(Gaug)
    prod_index = {}
    for A, prods in Glst_tmp.items():
        for k, p in enumerate(prods):
            prod_index[(A, tuple(p))] = k
    return nt_index, prod_index




def transitions_to_str(trans):
    by_src = defaultdict(list)
    for (i, X), j in trans.items():
        by_src[i].append((X, j))
    lines = ["\nGOTO transitions:"]
    for i in sorted(by_src.keys()):
        moves = ", ".join(f"on {X} -> I{j}" for X, j in sorted(by_src[i], key=lambda t: (t[0] != "$", str(t[0]))))
        lines.append(f"  I{i}: {moves}")
    return "\n".join(lines)

# ---------- Orchestration ----------

def build_lr0(filepath="grammar.txt"):
    Gstr = read_strings(filepath)
    Gaug, S_dash, S = augment_grammar(Gstr)
    Glst = to_symbol_lists(Gaug)
    states, trans = canonical_collection(Glst, S_dash)
    return Gaug, Glst, S_dash, S, states, trans








# ---------- LR(0) Table ----------
def collect_terminals_nonterminals(Glst):
    nts = list(Glst.keys())
    nts_set = set(nts)
    terms = set()
    for A, prods in Glst.items():
        for p in prods:
            for s in p:
                if s != "ε" and s not in nts_set:
                    terms.add(s)
    return nts, sorted(terms, key=str)


def build_lr0_table(Glst, S_dash, states, trans):
    """
    Returns:
      ACTION: dict[i][a] -> 's j' | 'r A->α' | 'acc' | ''
      GOTO:   dict[i][A] -> j | ''
      conflicts: list of (i, symbol, old, new)
    """
    nts, terms = collect_terminals_nonterminals(Glst)
    # Include end-marker for ACTION only
    action_terms = terms + ["$"]

    ACTION = {i: {a: "" for a in action_terms} for i in range(len(states))}
    GOTO   = {i: {A: "" for A in nts} for i in range(len(states))}
    conflicts = []

    # Map transitions for easy lookup
    # trans[(i, X)] = j already provided

    # Fill shift and goto from transitions
    for (i, X), j in trans.items():
        if X in nts:  # nonterminal
            if GOTO[i][X] != "" and GOTO[i][X] != j:
                conflicts.append((i, X, f"{GOTO[i][X]}", f"{j}"))
            GOTO[i][X] = j
        else:  # terminal
            # shift on terminal X
            old = ACTION[i].get(X, "")
            new = f"s {j}"
            if old and old != new:
                conflicts.append((i, X, old, new))
            ACTION[i][X] = new

    # Fill reduces and accept from items
    for i, I in enumerate(states):
        for (A, p, dot) in I:
            if dot == len(p):
                if A == S_dash:
                    ACTION[i]["$"] = "acc"
                else:
                    prod_str = " ".join(p) if len(p) > 0 else "ε"
                    new = f"r {A}->{prod_str}"
                    for a in ACTION[i].keys():
                        old = ACTION[i][a]
                        if old and old != new:
                            conflicts.append((i, a, old, new))
                        ACTION[i][a] = new


    return ACTION, GOTO, terms, nts, conflicts

def lr0_table_to_text(ACTION, GOTO, terms, nts):
    """
    Render a combined table with ACTION (terminals + $) and GOTO (nonterminals).
    """
    action_cols = terms + ["$"]
    goto_cols = [A for A in nts if A != nts[0]]  # usually exclude S' in GOTO
    headers = ["State"] + action_cols + goto_cols
    rows = []
    for i in range(len(ACTION)):
        row = [f"I{i}"]
        row += [ACTION[i].get(a, "") for a in action_cols]
        row += [GOTO[i].get(A, "") for A in goto_cols]
        rows.append(row)

    # Pretty print with column widths
    col_w = [max(len(h), max(len(str(r[c])) for r in rows)) for c, h in enumerate(headers)]
    def fmt_row(vals):
        return " | ".join(str(v).ljust(col_w[k]) for k, v in enumerate(vals))
    sep = "-+-".join("-"*w for w in col_w)

    lines = [fmt_row(headers), sep]
    for r in rows:
        lines.append(fmt_row(r))
    return "\n".join(lines)






def lr0_parse(input_string, ACTION, GOTO, terms, nts, states, Glst, S_dash):
    """
    Parse the input string using the LR(0) tables.
    Prints a step-by-step trace: state stack | input | action.
    """
    stack = [0]  # always holds state numbers
    w = list(input_string) + ['$']
    ip = 0

    trace = []

    while True:
        state = stack[-1]
        lookahead = w[ip]
        action = ACTION[state].get(lookahead, "")

        # Prepare strings for pretty trace display
        stack_str = " ".join(map(str, stack))
        input_str = "".join(w[ip:])
        act_str = action

        trace.append((stack_str, input_str, act_str))

        if action == "":
            trace.append((stack_str, input_str, "ERROR"))
            break
        elif action.startswith("s "):  # shift
            next_state = int(action[2:])
            stack.append(lookahead)
            stack.append(next_state)
            ip += 1
        elif action == "acc":
            break
        elif action.startswith("r "):  # reduce
            # parse "r A->α"
            prod = action[2:]
            A, rhs = prod.split("->")
            A = A.strip()
            rhs_syms = rhs.strip().split()
            if rhs_syms == ['ε']:
                m = 0
            else:
                m = 2 * len(rhs_syms)
            # Pop 2*|α| (state,symbol) pairs
            for _ in range(m):
                stack.pop()
            state_t = stack[-1]
            stack.append(A)
            next_state = GOTO[state_t][A]
            stack.append(next_state)
        else:
            trace.append((stack_str, input_str, "ERROR"))
            break

    return trace


def compute_first_follow(Glst):
    nts = list(Glst.keys())
    first = {X: set() for X in Glst}
    nts_set = set(nts)
    changed = True
    while changed:
        changed = False
        for A in Glst:
            for prod in Glst[A]:
                if len(prod) == 0:
                    if "ε" not in first[A]:
                        first[A].add("ε")
                        changed = True
                    continue
                k = 0
                while k < len(prod):
                    sym = prod[k]
                    if sym not in nts_set:
                        if sym not in first[A]:
                            first[A].add(sym)
                            changed = True
                        break
                    else:
                        added = first[sym] - {"ε"}
                        if not added.issubset(first[A]):
                            first[A].update(added)
                            changed = True
                        if "ε" not in first[sym]:
                            break
                    k += 1
                else:
                    if "ε" not in first[A]:
                        first[A].add("ε")
                        changed = True
    follow = {A: set() for A in Glst}
    start_nt = list(Glst.keys())[1] if len(Glst) > 1 else list(Glst.keys())[0]
    follow[start_nt].add('$')
    changed = True
    while changed:
        changed = False
        for A in Glst:
            for prod in Glst[A]:
                for i, sym in enumerate(prod):
                    if sym not in nts_set:
                        continue
                    after = prod[i+1:]
                    fs = set()
                    if after:
                        k = 0
                        while k < len(after):
                            T = after[k]
                            if T not in nts_set:
                                fs.add(T)
                                break
                            else:
                                fs.update(first[T] - {"ε"})
                                if "ε" not in first[T]:
                                    break
                            k += 1
                        else:
                            fs.add("ε")
                    else:
                        fs.add("ε")
                    if "ε" in fs:
                        fs.discard("ε")
                        if not follow[A].issubset(follow[sym]):
                            follow[sym].update(follow[A])
                            changed = True
                    if not fs.issubset(follow[sym]):
                        follow[sym].update(fs)
                        changed = True
    return first, follow


def build_slr1_table(Glst, S_dash, states, trans):
    nts, terms = collect_terminals_nonterminals(Glst)
    action_terms = terms + ["$"]
    first, follow = compute_first_follow(Glst)
    ACTION = {i: {a: "" for a in action_terms} for i in range(len(states))}
    GOTO   = {i: {A: "" for A in nts} for i in range(len(states))}
    conflicts = []
    # shift/goto transitions as in LR(0)
    for (i, X), j in trans.items():
        if X in nts:
            GOTO[i][X] = j
        else:
            ACTION[i][X] = f"s {j}"
    # REDUCE only for lookaheads in FOLLOW(A)
    for i, I in enumerate(states):
        for (A, p, dot) in I:
            if dot == len(p):  # complete item
                if A == S_dash:
                    ACTION[i]["$"] = "acc"
                else:
                    prod_str = " ".join(p) if p else "ε"
                    new = f"r {A}->{prod_str}"
                    for a in follow[A]:
                        old = ACTION[i][a]
                        if old and old != "" and old != new:
                            conflicts.append((i, a, old, new))
                        ACTION[i][a] = new
    return ACTION, GOTO, terms, nts, conflicts, follow



if __name__ == "__main__":
    # Build canonical LR(0) artifacts
    Gaug, Glst, S_dash, S, states, trans = build_lr0("grammar.txt")

    # Ordering indices so states print as: S', S, A ... and productions in file order
    nt_index, prod_index = build_order_indices(Gaug)

    print("Augmented grammar:")
    for A, prods in Gaug.items():
        print(f"{A} -> {' | '.join(prods)}")

    print("\nCanonical LR(0) item sets:")
    for i, I in enumerate(states):
        print(state_to_str(i, I, nt_index, prod_index))

    print(transitions_to_str(trans))

    # ---- LR(0) parsing table ----
    ACTION, GOTO, terms, nts, lr0_conflicts = build_lr0_table(Glst, S_dash, states, trans)
    print("\nLR(0) Parsing Table")
    print(lr0_table_to_text(ACTION, GOTO, terms, nts))
    if lr0_conflicts:
        print("\nLR(0) Conflicts:")
        for i, sym, old, new in lr0_conflicts:
            print(f"  State I{i}, on '{sym}': {old} vs {new}")
    else:
        print("\nNo conflicts in LR(0) table.")

    # ---- SLR(1) parsing table ----
    SLR_ACTION, SLR_GOTO, slr_terms, slr_nts, slr_conflicts, follow = build_slr1_table(Glst, S_dash, states, trans)
    print("\nSLR(1) Parsing Table")
    print(lr0_table_to_text(SLR_ACTION, SLR_GOTO, slr_terms, slr_nts))
    if slr_conflicts:
        print("\nSLR(1) Conflicts:")
        for i, sym, old, new in slr_conflicts:
            print(f"  State I{i}, on '{sym}': {old} vs {new}")
    else:
        print("\nNo conflicts in SLR(1) table.")

    print("\nFOLLOW sets (for SLR(1)):")
    for A in follow:
        shown = ", ".join(sorted(follow[A]))
        print(f"Follow({A}) = {{ {shown} }}")


    # ---- Decide which traces to show ----
    lr0_ok = (len(lr0_conflicts) == 0)
    slr_ok = (len(slr_conflicts) == 0)

    if not lr0_ok and not slr_ok:
        print("\nBoth LR(0) and SLR(1) tables have conflicts. Parsing is disabled.")
    else:
        try:
            inp = input("\nEnter input string to parse (without $): ").strip()
        except EOFError:
            inp = ""
        if inp:
            if lr0_ok:
                print("\nUsing LR(0) table for parsing")
                trace0 = lr0_parse(inp, ACTION, GOTO, terms, nts, states, Glst, S_dash)
                print("\n[LR(0) Trace] {:<24} | {:<18} | {}".format("STATE STACK", "INPUT", "ACTION"))
                print("-"*78)
                for stack_str, input_str, act in trace0:
                    print("{:<24} | {:<18} | {}".format(stack_str, input_str, act))
            else:
                print("\nLR(0) table has conflicts; skipping LR(0) parse.")

            if slr_ok:
                print("\nUsing SLR(1) table for parsing")
                trace1 = lr0_parse(inp, SLR_ACTION, SLR_GOTO, slr_terms, slr_nts, states, Glst, S_dash)
                print("\n[SLR(1) Trace] {:<24} | {:<18} | {}".format("STATE STACK", "INPUT", "ACTION"))
                print("-"*80)
                for stack_str, input_str, act in trace1:
                    print("{:<24} | {:<18} | {}".format(stack_str, input_str, act))
            else:
                print("\nSLR(1) table has conflicts; skipping SLR(1) parse.")
