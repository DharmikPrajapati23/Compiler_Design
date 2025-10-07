# # # clr_lalr.py
# # # -*- coding: utf-8 -*-
# # from collections import defaultdict, deque

# # # ---------- IO and tokenization ----------

# # def read_strings(filepath):
# #     G = {}
# #     with open(filepath, "r", encoding="utf-8") as f:
# #         for line in f:
# #             line = line.strip()
# #             if not line or "->" not in line:
# #                 continue
# #             A, rhs = line.split("->", 1)
# #             A = A.strip()
# #             prods = [p.strip() for p in rhs.split("|")]
# #             G[A] = prods
# #     return G

# # def tokenize_production(prod, nonterminals):
# #     if prod == "ε":
# #         return ["ε"]
# #     toks = []
# #     i = 0
# #     nts = sorted(nonterminals, key=len, reverse=True)
# #     while i < len(prod):
# #         matched = False
# #         for nt in nts:
# #             L = len(nt)
# #             if prod[i:i+L] == nt:
# #                 toks.append(nt); i += L; matched = True; break
# #         if not matched:
# #             toks.append(prod[i]); i += 1
# #     return toks

# # def to_symbol_lists(Gstr):
# #     nts = set(Gstr.keys())
# #     Glst = {}
# #     for A, prods in Gstr.items():
# #         Glst[A] = [tokenize_production(p, nts) for p in prods]
# #     return Glst

# # def augment_grammar(Gstr):
# #     if not Gstr:
# #         raise ValueError("Empty grammar.")
# #     S = next(iter(Gstr))
# #     S_dash = S + "'"
# #     while S_dash in Gstr:
# #         S_dash += "'"
# #     Gaug = {S_dash: [S]}
# #     Gaug.update(Gstr)
# #     return Gaug, S_dash, S

# # # ---------- FIRST ----------

# # def compute_first(Glst):
# #     nts = list(Glst.keys())
# #     nts_set = set(nts)
# #     first = {A: set() for A in Glst}
# #     changed = True
# #     while changed:
# #         changed = False
# #         for A in Glst:
# #             for prod in Glst[A]:
# #                 k = 0
# #                 while k < len(prod):
# #                     X = prod[k]
# #                     if X == "ε":
# #                         if "ε" not in first[A]:
# #                             first[A].add("ε"); changed = True
# #                         break
# #                     if X not in nts_set:
# #                         if X not in first[A]:
# #                             first[A].add(X); changed = True
# #                         break
# #                     add = first[X] - {"ε"}
# #                     if not add.issubset(first[A]):
# #                         first[A].update(add); changed = True
# #                     if "ε" not in first[X]:
# #                         break
# #                     k += 1
# #                 else:
# #                     if "ε" not in first[A]:
# #                         first[A].add("ε"); changed = True
# #     return first

# # def first_of_seq(seq, first, Glst):
# #     nts_set = set(Glst.keys())
# #     out = set()
# #     if not seq:
# #         out.add("ε"); return out
# #     for X in seq:
# #         if X in nts_set:
# #             out |= (first[X] - {"ε"})
# #             if "ε" not in first[X]:
# #                 break
# #         else:
# #             out.add(X); break
# #     else:
# #         out.add("ε")
# #     return out

# # # ---------- CLR (LR(1)) items ----------
# # def item_core_str(A, p, dot):
# #     syms = list(p)
# #     syms.insert(dot, "•")
# #     return f"{A} -> {' '.join(syms) if syms else '•'}"

# # def state_lr1_str_merged_lookaheads(idx, I):
# #     """
# #     Render a state (CLR or LALR) grouping identical cores and unioning lookaheads:
# #     A -> • a A, a | b
# #     """
# #     from collections import defaultdict
# #     la_map = defaultdict(set)  # (A, p, dot) -> set(lookaheads)
# #     for (A, p, dot, la) in I:
# #         la_map[(A, p, dot)].add(la)

# #     cores_sorted = sorted(la_map.keys(), key=lambda x: (x[0], x[1], x[2]))

# #     lines = [f"I{idx}:"]
# #     for (A, p, dot) in cores_sorted:
# #         core_txt = item_core_str(A, p, dot)
# #         las = " | ".join(sorted(la_map[(A, p, dot)], key=str))
# #         lines.append(f"  {core_txt}, {las}")
# #     return "\n".join(lines)

# # # Optional: explicit alias for readability
# # def state_lalr_str_merged_lookaheads(idx, I):
# #     return state_lr1_str_merged_lookaheads(idx, I)

# # # Item: (A, tuple(rhs), dot, lookahead)
# # def lr1_closure(I, Glst, first):
# #     I = set(I)
# #     nts = set(Glst.keys())
# #     changed = True
# #     while changed:
# #         changed = False
# #         add_list = []
# #         for (A, beta, dot, la) in list(I):
# #             if dot < len(beta):
# #                 X = beta[dot]
# #                 if X in nts:
# #                     tail = list(beta[dot+1:])
# #                     la_set = first_of_seq(tail + [la], first, Glst)
# #                     for prod in Glst[X]:
# #                         for a in (la_set or {"$"}):
# #                             if a == "ε":
# #                                 continue
# #                             it = (X, tuple(prod), 0, a)
# #                             if it not in I and it not in add_list:
# #                                 add_list.append(it)
# #         if add_list:
# #             I.update(add_list); changed = True
# #     return I

# # def lr1_goto(I, X, Glst, first):
# #     J = set()
# #     for (A, beta, dot, la) in I:
# #         if dot < len(beta) and beta[dot] == X:
# #             J.add((A, beta, dot+1, la))
# #     if not J:
# #         return set()
# #     return lr1_closure(J, Glst, first)

# # def symbol_order(Glst):
# #     nts = list(Glst.keys())
# #     nts_set = set(nts)
# #     terms = set()
# #     for A, prods in Glst.items():
# #         for p in prods:
# #             for s in p:
# #                 if s != "ε" and s not in nts_set:
# #                     terms.add(s)
# #     terms = sorted(terms, key=str)
# #     return nts + terms

# # def canonical_lr1(Glst, S_dash, first):
# #     start_prod = Glst[S_dash][0]
# #     I0 = lr1_closure({(S_dash, tuple(start_prod), 0, "$")}, Glst, first)
# #     states = [I0]
# #     trans = {}
# #     work = deque([0])
# #     ordered_symbols = symbol_order(Glst)
# #     while work:
# #         i = work.popleft()
# #         I = states[i]
# #         for X in ordered_symbols:
# #             J = lr1_goto(I, X, Glst, first)
# #             if not J:
# #                 continue
# #             for idx, st in enumerate(states):
# #                 if st == J:
# #                     trans[(i, X)] = idx
# #                     break
# #             else:
# #                 states.append(J)
# #                 j = len(states) - 1
# #                 trans[(i, X)] = j
# #                 work.append(j)
# #     return states, trans

# # # ---------- Tables (CLR and LALR) ----------

# # def collect_terminals_nonterminals(Glst):
# #     nts = list(Glst.keys())
# #     nts_set = set(nts)
# #     terms = set()
# #     for A, prods in Glst.items():
# #         for p in prods:
# #             for s in p:
# #                 if s != "ε" and s not in nts_set:
# #                     terms.add(s)
# #     return nts, sorted(terms, key=str)

# # def build_lr1_table(Glst, S_dash, states, trans):
# #     nts, terms = collect_terminals_nonterminals(Glst)
# #     action_terms = terms + ["$"]
# #     ACTION = {i: {a: "" for a in action_terms} for i in range(len(states))}
# #     GOTO   = {i: {A: "" for A in nts} for i in range(len(states))}
# #     conflicts = []

# #     for (i, X), j in trans.items():
# #         if X in nts:
# #             GOTO[i][X] = j
# #         else:
# #             old = ACTION[i][X]
# #             new = f"s {j}"
# #             if old and old != new:
# #                 conflicts.append((i, X, old, new))
# #             ACTION[i][X] = new

# #     for i, I in enumerate(states):
# #         for (A, p, dot, la) in I:
# #             if dot == len(p):
# #                 if A == S_dash:
# #                     old = ACTION[i]["$"]; new = "acc"
# #                     if old and old != new:
# #                         conflicts.append((i, "$", old, new))
# #                     ACTION[i]["$"] = new
# #                 else:
# #                     prod_str = " ".join(p) if p else "ε"
# #                     new = f"r {A}->{prod_str}"
# #                     old = ACTION[i][la]
# #                     if old and old != new:
# #                         conflicts.append((i, la, old, new))
# #                     ACTION[i][la] = new
# #     return ACTION, GOTO, terms, nts, conflicts

# # # ---------- Merge CLR -> LALR ----------

# # def core_of(I):
# #     return frozenset((A, p, dot) for (A, p, dot, la) in I)

# # def merge_clr_states(states, trans):
# #     core_to_indices = defaultdict(list)
# #     for i, I in enumerate(states):
# #         core_to_indices[core_of(I)].append(i)

# #     merged_states = []
# #     core_to_merged = {}
# #     # Build merged states by unioning lookaheads per core item
# #     for core, idxs in core_to_indices.items():
# #         la_map = defaultdict(set)
# #         for i in idxs:
# #             for (A, p, dot, la) in states[i]:
# #                 la_map[(A, p, dot)].add(la)
# #         merged = set()
# #         for (A, p, dot), LAs in la_map.items():
# #             for a in sorted(LAs):
# #                 merged.add((A, p, dot, a))
# #         core_to_merged[core] = len(merged_states)
# #         merged_states.append(merged)

# #     # Redirect transitions via merged indices
# #     merged_trans = {}
# #     for (i, X), j in trans.items():
# #         mi = core_to_merged[core_of(states[i])]
# #         mj = core_to_merged[core_of(states[j])]
# #         merged_trans[(mi, X)] = mj

# #     return merged_states, merged_trans

# # def build_lalr_table(Glst, S_dash, lalr_states, lalr_trans):
# #     return build_lr1_table(Glst, S_dash, lalr_states, lalr_trans)

# # # ---------- Rendering ----------

# # def item_lr1_str(it):
# #     A, p, dot, la = it
# #     syms = list(p)
# #     syms.insert(dot, "•")
# #     return f"{A} -> {' '.join(syms) if syms else '•'}, {la}"

# # def state_lr1_str(idx, I):
# #     lines = [f"I{idx}:"]
# #     for it in sorted(I, key=lambda x: (x[0], x[1], x[2], x[3])):
# #         lines.append("  " + item_lr1_str(it))
# #     return "\n".join(lines)

# # def transitions_to_str(trans):
# #     by_src = defaultdict(list)
# #     for (i, X), j in trans.items():
# #         by_src[i].append((X, j))
# #     lines = ["\nGOTO transitions:"]
# #     for i in sorted(by_src.keys()):
# #         moves = ", ".join(f"on {X} -> I{j}" for X, j in sorted(by_src[i], key=lambda t: (t[0] != "$", str(t[0]))))
# #         lines.append(f"  I{i}: {moves}")
# #     return "\n".join(lines)

# # def table_to_text(ACTION, GOTO, terms, nts):
# #     action_cols = terms + ["$"]
# #     goto_cols = [A for A in nts if A != nts[0]]
# #     headers = ["State"] + action_cols + goto_cols
# #     rows = []
# #     for i in range(len(ACTION)):
# #         row = [f"I{i}"]
# #         row += [ACTION[i].get(a, "") for a in action_cols]
# #         row += [GOTO[i].get(A, "") for A in goto_cols]
# #         rows.append(row)
# #     col_w = [max(len(h), max(len(str(r[c])) for r in rows)) for c, h in enumerate(headers)]
# #     def fmt_row(vals):
# #         return " | ".join(str(v).ljust(col_w[k]) for k, v in enumerate(vals))
# #     sep = "-+-".join("-"*w for w in col_w)
# #     return "\n".join([fmt_row(headers), sep] + [fmt_row(r) for r in rows])

# # # ---------- Optional LALR parse ----------

# # def lalr_parse(input_string, ACTION, GOTO):
# #     stack = [0]
# #     w = list(input_string) + ["$"]
# #     ip = 0
# #     trace = []
# #     while True:
# #         s = stack[-1]
# #         a = w[ip]
# #         act = ACTION[s].get(a, "")
# #         trace.append((" ".join(map(str, stack)), "".join(w[ip:]), act))
# #         if act == "":
# #             trace.append((" ".join(map(str, stack)), "".join(w[ip:]), "ERROR"))
# #             break
# #         if act == "acc":
# #             break
# #         if act.startswith("s "):
# #             j = int(act[2:])
# #             stack.append(a); stack.append(j)
# #             ip += 1
# #         elif act.startswith("r "):
# #             prod = act[2:]
# #             A, rhs = prod.split("->")
# #             A = A.strip(); rhs_syms = rhs.strip().split()
# #             m = 0 if rhs_syms == ["ε"] else 2*len(rhs_syms)
# #             for _ in range(m):
# #                 stack.pop()
# #             t = stack[-1]
# #             stack.append(A)
# #             j = GOTO[t][A]
# #             stack.append(j)
# #         else:
# #             trace.append((" ".join(map(str, stack)), "".join(w[ip:]), "ERROR"))
# #             break
# #     return trace

# # # ---------- Main ----------

# # if __name__ == "__main__":
# #     # Load and augment
# #     Gstr = read_strings("grammar.txt")
# #     Gaug, S_dash, S = augment_grammar(Gstr)
# #     Glst = to_symbol_lists(Gaug)

# #     print("Augmented grammar:")
# #     for A, Ps in Gaug.items():
# #         print(f"{A} -> {' | '.join(Ps)}")

# #     # CLR (LR(1)) collection and table
# #     first = compute_first(Glst)
# #     clr_states, clr_trans = canonical_lr1(Glst, S_dash, first)

# #     print("\nCLR (LR(1)) item sets:")
# #     for i, I in enumerate(clr_states):
# #         print(state_lr1_str_merged_lookaheads(i, I))

# #     print(transitions_to_str(clr_trans))

# #     ACTION_CLR, GOTO_CLR, terms, nts, clr_conf = build_lr1_table(Glst, S_dash, clr_states, clr_trans)
# #     print("\nCLR Parsing Table")
# #     print(table_to_text(ACTION_CLR, GOTO_CLR, terms, nts))
# #     if clr_conf:
# #         print("\nCLR Conflicts:")
# #         for i, sym, old, new in clr_conf:
# #             print(f"  I{i}, on '{sym}': {old} vs {new}")
# #     else:
# #         print("\nNo conflicts in CLR table.")

# #     # Merge CLR -> LALR and build table
# #     lalr_states, lalr_trans = merge_clr_states(clr_states, clr_trans)

# #     print("\nLALR merged item sets (from CLR cores):")
# #     for i, I in enumerate(lalr_states):
# #         print(state_lalr_str_merged_lookaheads(i, I))  # same merged lookahead view

# #     print(transitions_to_str(lalr_trans))

# #     ACTION_LALR, GOTO_LALR, terms2, nts2, lalr_conf = build_lalr_table(Glst, S_dash, lalr_states, lalr_trans)
# #     print("\nLALR Parsing Table")
# #     print(table_to_text(ACTION_LALR, GOTO_LALR, terms2, nts2))
# #     if lalr_conf:
# #         print("\nLALR Conflicts:")
# #         for i, sym, old, new in lalr_conf:
# #             print(f"  I{i}, on '{sym}': {old} vs {new}")
# #     else:
# #         print("\nNo conflicts in LALR table.")

# #     # Optional parse if LALR is conflict-free
# #     if not lalr_conf:
# #         try:
# #             s = input("\nEnter input string to parse with LALR (without $): ").strip()
# #         except EOFError:
# #             s = ""
# #         if s:
# #             trace = lalr_parse(s, ACTION_LALR, GOTO_LALR)
# #             print("\n{:<24} | {:<18} | {}".format("STATE STACK", "INPUT", "ACTION"))
# #             print("-"*72)
# #             for stck, inp, act in trace:
# #                 print("{:<24} | {:<18} | {}".format(stck, inp, act))



# #------------------------------------------------------------------------------------








# # clr_lalr.py
# # -*- coding: utf-8 -*-
# from collections import defaultdict, deque

# # ---------- IO and tokenization ----------

# def read_strings(filepath):
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
#                 toks.append(nt); i += L; matched = True; break
#         if not matched:
#             toks.append(prod[i]); i += 1
#     return toks

# def to_symbol_lists(Gstr):
#     nts = set(Gstr.keys())
#     Glst = {}
#     for A, prods in Gstr.items():
#         Glst[A] = [tokenize_production(p, nts) for p in prods]
#     return Glst

# def augment_grammar(Gstr):
#     if not Gstr:
#         raise ValueError("Empty grammar.")
#     S = next(iter(Gstr))
#     S_dash = S + "'"
#     while S_dash in Gstr:
#         S_dash += "'"
#     Gaug = {S_dash: [S]}
#     Gaug.update(Gstr)
#     return Gaug, S_dash, S

# # ---------- FIRST ----------

# def compute_first(Glst):
#     nts = list(Glst.keys())
#     nts_set = set(nts)
#     first = {A: set() for A in Glst}
#     changed = True
#     while changed:
#         changed = False
#         for A in Glst:
#             for prod in Glst[A]:
#                 k = 0
#                 while k < len(prod):
#                     X = prod[k]
#                     if X == "ε":
#                         if "ε" not in first[A]:
#                             first[A].add("ε"); changed = True
#                         break
#                     if X not in nts_set:
#                         if X not in first[A]:
#                             first[A].add(X); changed = True
#                         break
#                     add = first[X] - {"ε"}
#                     if not add.issubset(first[A]):
#                         first[A].update(add); changed = True
#                     if "ε" not in first[X]:
#                         break
#                     k += 1
#                 else:
#                     if "ε" not in first[A]:
#                         first[A].add("ε"); changed = True
#     return first

# def first_of_seq(seq, first, Glst):
#     nts_set = set(Glst.keys())
#     out = set()
#     if not seq:
#         out.add("ε"); return out
#     for X in seq:
#         if X in nts_set:
#             out |= (first[X] - {"ε"})
#             if "ε" not in first[X]:
#                 break
#         else:
#             out.add(X); break
#     else:
#         out.add("ε")
#     return out

# # ---------- CLR (LR(1)) items ----------
# def group_clr_by_core(states):
#     """
#     Return:
#       core_to_indices: dict[frozenset(core item)]-> list[int] (CLR indices in encounter order)
#       groups: list[list[int]] groups of CLR indices with identical cores, in first-occurrence order
#     """
#     core_to_indices = defaultdict(list)
#     order = []
#     for i, I in enumerate(states):
#         core = frozenset((A, p, dot) for (A, p, dot, la) in I)
#         if core not in core_to_indices:
#             order.append(core)
#         core_to_indices[core].append(i)
#     groups = [core_to_indices[c] for c in order]
#     return core_to_indices, groups

# def label_for_group(g):
#     """
#     Build label text like '36' or '89' by concatenating CLR indices of the group in ascending order.
#     For singletons, use the single index, e.g., '2'.
#     """
#     return "".join(str(k) for k in sorted(g))

# def merge_clr_with_labels(states, trans):
#     """
#     Merge CLR states by core, union lookaheads, but:
#     - Compute merged_states (unique cores)
#     - Provide:
#       clr_to_merged_idx: map CLR index -> merged state index
#       merged_idx_to_label: map merged state index -> '36' style label
#       sequence_labels: list of labels in CLR encounter order (repeats allowed)
#       merged_trans: transitions between merged indices
#     """
#     _, groups = group_clr_by_core(states)
#     # Build merged states in the order of first occurrence of each core
#     merged_states = []
#     merged_idx_to_label = {}
#     core_to_merged_idx = {}
#     # Build a helper map from CLR index to its core
#     cores = [frozenset((A,p,dot) for (A,p,dot,la) in I) for I in states]

#     first_seen_core_order = []
#     for g in groups:
#         # union lookaheads for items sharing same (A,p,dot)
#         la_map = defaultdict(set)
#         for i in g:
#             for (A, p, dot, la) in states[i]:
#                 la_map[(A, p, dot)].add(la)
#         merged = set()
#         for (A, p, dot), LAs in la_map.items():
#             for a in sorted(LAs):
#                 merged.add((A, p, dot, a))
#         idx = len(merged_states)
#         merged_states.append(merged)
#         lab = label_for_group(g)
#         merged_idx_to_label[idx] = lab
#         # map all CLR indices of this group to this merged idx
#         c = cores[g[0]]
#         core_to_merged_idx[c] = idx
#         first_seen_core_order.append(c)

#     # Build CLR->merged index map
#     clr_to_merged_idx = {}
#     for i, I in enumerate(states):
#         c = cores[i]
#         clr_to_merged_idx[i] = core_to_merged_idx[c]

#     # Build merged transitions
#     merged_trans = {}
#     for (i, X), j in trans.items():
#         mi = clr_to_merged_idx[i]
#         mj = clr_to_merged_idx[j]
#         merged_trans[(mi, X)] = mj

#     # Sequence labels in CLR encounter order (repeats)
#     sequence_labels = []
#     for i in range(len(states)):
#         mi = clr_to_merged_idx[i]
#         sequence_labels.append(merged_idx_to_label[mi])

#     # Flag: any merge happened?
#     merged_flag = any(len(g) > 1 for g in groups)

#     return merged_states, merged_trans, clr_to_merged_idx, merged_idx_to_label, sequence_labels, merged_flag

# def item_core_str(A, p, dot):
#     syms = list(p)
#     syms.insert(dot, "•")
#     return f"{A} -> {' '.join(syms) if syms else '•'}"


# def state_str_with_label(label, I):
#     # Same merged-lookahead formatting used for CLR
#     la_map = defaultdict(set)
#     for (A, p, dot, la) in I:
#         la_map[(A, p, dot)].add(la)
#     cores_sorted = sorted(la_map.keys(), key=lambda x: (x[0], x[1], x[2]))
#     lines = [f"I{label}:"]
#     for (A, p, dot) in cores_sorted:
#         syms = list(p); syms.insert(dot, "•")
#         core_txt = f"{A} -> {' '.join(syms) if syms else '•'}"
#         las = " | ".join(sorted(la_map[(A, p, dot)], key=str))
#         lines.append(f"  {core_txt}, {las}")
#     return "\n".join(lines)

# def transitions_str_labeled(merged_trans, merged_idx_to_label):
#     by_src = defaultdict(list)
#     for (i, X), j in merged_trans.items():
#         by_src[i].append((X, j))
#     lines = ["\nGOTO transitions (LALR labels):"]
#     for i in sorted(by_src.keys()):
#         moves = ", ".join(
#             f"on {X} -> I{merged_idx_to_label[j]}"
#             for X, j in sorted(by_src[i], key=lambda t: (t[0] != "$", str(t[0])))
#         )
#         lines.append(f"  I{merged_idx_to_label[i]}: {moves}")
#     return "\n".join(lines)


# def state_lr1_str_merged_lookaheads(idx, I):
#     """
#     Render a state (CLR or LALR) grouping identical cores and unioning lookaheads:
#     A -> • a A, a | b
#     """
#     from collections import defaultdict
#     la_map = defaultdict(set)  # (A, p, dot) -> set(lookaheads)
#     for (A, p, dot, la) in I:
#         la_map[(A, p, dot)].add(la)

#     cores_sorted = sorted(la_map.keys(), key=lambda x: (x[0], x[1], x[2]))

#     lines = [f"I{idx}:"]
#     for (A, p, dot) in cores_sorted:
#         core_txt = item_core_str(A, p, dot)
#         las = " | ".join(sorted(la_map[(A, p, dot)], key=str))
#         lines.append(f"  {core_txt}, {las}")
#     return "\n".join(lines)

# # Optional: explicit alias for readability
# def state_lalr_str_merged_lookaheads(idx, I):
#     return state_lr1_str_merged_lookaheads(idx, I)

# # Item: (A, tuple(rhs), dot, lookahead)
# def lr1_closure(I, Glst, first):
#     I = set(I)
#     nts = set(Glst.keys())
#     changed = True
#     while changed:
#         changed = False
#         add_list = []
#         for (A, beta, dot, la) in list(I):
#             if dot < len(beta):
#                 X = beta[dot]
#                 if X in nts:
#                     tail = list(beta[dot+1:])
#                     la_set = first_of_seq(tail + [la], first, Glst)
#                     for prod in Glst[X]:
#                         for a in (la_set or {"$"}):
#                             if a == "ε":
#                                 continue
#                             it = (X, tuple(prod), 0, a)
#                             if it not in I and it not in add_list:
#                                 add_list.append(it)
#         if add_list:
#             I.update(add_list); changed = True
#     return I

# def lr1_goto(I, X, Glst, first):
#     J = set()
#     for (A, beta, dot, la) in I:
#         if dot < len(beta) and beta[dot] == X:
#             J.add((A, beta, dot+1, la))
#     if not J:
#         return set()
#     return lr1_closure(J, Glst, first)

# def build_lalr_table_labeled(Glst, S_dash, lalr_states, lalr_trans, merged_idx_to_label):
#     ACTION, GOTO, terms, nts, conflicts = build_lr1_table(Glst, S_dash, lalr_states, lalr_trans)
#     # Convert row indices to labels
#     row_labels = [merged_idx_to_label[i] for i in range(len(lalr_states))]
#     # Also build a display table keyed by label
#     action_cols = terms + ["$"]
#     goto_cols = [A for A in nts if A != nts[0]]
#     rows = []
#     for i, lab in enumerate(row_labels):
#         row = [lab] + [ACTION[i].get(a, "") for a in action_cols] + [GOTO[i].get(A, "") for A in goto_cols]
#         rows.append(row)
#     headers = ["State"] + action_cols + goto_cols
#     return ACTION, GOTO, terms, nts, conflicts, headers, rows


# def symbol_order(Glst):
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

# def canonical_lr1(Glst, S_dash, first):
#     start_prod = Glst[S_dash][0]
#     I0 = lr1_closure({(S_dash, tuple(start_prod), 0, "$")}, Glst, first)
#     states = [I0]
#     trans = {}
#     work = deque([0])
#     ordered_symbols = symbol_order(Glst)
#     while work:
#         i = work.popleft()
#         I = states[i]
#         for X in ordered_symbols:
#             J = lr1_goto(I, X, Glst, first)
#             if not J:
#                 continue
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

# # ---------- Tables (CLR and LALR) ----------

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




# def build_lr1_table(Glst, S_dash, states, trans, prod_num):
#     nts, terms = collect_terminals_nonterminals(Glst)
#     action_terms = terms + ["$"]
#     ACTION = {i: {a: "" for a in action_terms} for i in range(len(states))}
#     GOTO   = {i: {A: "" for A in nts} for i in range(len(states))}
#     conflicts = []

#     # Shifts and GOTOs
#     for (i, X), j in trans.items():
#         if X in nts:
#             GOTO[i][X] = j
#         else:
#             old = ACTION[i][X]; new = f"S{j}"
#             if old and old != new:
#                 conflicts.append((i, X, old, new))
#             ACTION[i][X] = new

#     # Reductions and Accept
#     for i, I in enumerate(states):
#         for (A, p, dot, la) in I:
#             if dot == len(p):
#                 if A == S_dash:
#                     old = ACTION[i]["$"]; new = "Accept"
#                     if old and old != new:
#                         conflicts.append((i, "$", old, new))
#                     ACTION[i]["$"] = new
#                 else:
#                     k = prod_num[(A, p)]
#                     new = f"R{k}"
#                     old = ACTION[i][la]
#                     if old and old != new:
#                         conflicts.append((i, la, old, new))
#                     ACTION[i][la] = new
#     return ACTION, GOTO, terms, nts, conflicts


# # def build_lr1_table(Glst, S_dash, states, trans):
# #     nts, terms = collect_terminals_nonterminals(Glst)
# #     action_terms = terms + ["$"]
# #     ACTION = {i: {a: "" for a in action_terms} for i in range(len(states))}
# #     GOTO   = {i: {A: "" for A in nts} for i in range(len(states))}
# #     conflicts = []

# #     for (i, X), j in trans.items():
# #         if X in nts:
# #             GOTO[i][X] = j
# #         else:
# #             old = ACTION[i][X]
# #             new = f"s {j}"
# #             if old and old != new:
# #                 conflicts.append((i, X, old, new))
# #             ACTION[i][X] = new

# #     for i, I in enumerate(states):
# #         for (A, p, dot, la) in I:
# #             if dot == len(p):
# #                 if A == S_dash:
# #                     old = ACTION[i]["$"]; new = "acc"
# #                     if old and old != new:
# #                         conflicts.append((i, "$", old, new))
# #                     ACTION[i]["$"] = new
# #                 else:
# #                     prod_str = " ".join(p) if p else "ε"
# #                     new = f"r {A}->{prod_str}"
# #                     old = ACTION[i][la]
# #                     if old and old != new:
# #                         conflicts.append((i, la, old, new))
# #                     ACTION[i][la] = new
# #     return ACTION, GOTO, terms, nts, conflicts

# # ---------- Merge CLR -> LALR ----------

# def core_of(I):
#     return frozenset((A, p, dot) for (A, p, dot, la) in I)

# def merge_clr_states(states, trans):
#     core_to_indices = defaultdict(list)
#     for i, I in enumerate(states):
#         core_to_indices[core_of(I)].append(i)

#     merged_states = []
#     core_to_merged = {}
#     # Build merged states by unioning lookaheads per core item
#     for core, idxs in core_to_indices.items():
#         la_map = defaultdict(set)
#         for i in idxs:
#             for (A, p, dot, la) in states[i]:
#                 la_map[(A, p, dot)].add(la)
#         merged = set()
#         for (A, p, dot), LAs in la_map.items():
#             for a in sorted(LAs):
#                 merged.add((A, p, dot, a))
#         core_to_merged[core] = len(merged_states)
#         merged_states.append(merged)

#     # Redirect transitions via merged indices
#     merged_trans = {}
#     for (i, X), j in trans.items():
#         mi = core_to_merged[core_of(states[i])]
#         mj = core_to_merged[core_of(states[j])]
#         merged_trans[(mi, X)] = mj

#     return merged_states, merged_trans

# def build_lalr_table(Glst, S_dash, lalr_states, lalr_trans):
#     return build_lr1_table(Glst, S_dash, lalr_states, lalr_trans)

# # ---------- Rendering ----------

# def item_lr1_str(it):
#     A, p, dot, la = it
#     syms = list(p)
#     syms.insert(dot, "•")
#     return f"{A} -> {' '.join(syms) if syms else '•'}, {la}"

# def state_lr1_str(idx, I):
#     lines = [f"I{idx}:"]
#     for it in sorted(I, key=lambda x: (x[0], x[1], x[2], x[3])):
#         lines.append("  " + item_lr1_str(it))
#     return "\n".join(lines)

# def transitions_to_str(trans):
#     by_src = defaultdict(list)
#     for (i, X), j in trans.items():
#         by_src[i].append((X, j))
#     lines = ["\nGOTO transitions:"]
#     for i in sorted(by_src.keys()):
#         moves = ", ".join(f"on {X} -> I{j}" for X, j in sorted(by_src[i], key=lambda t: (t[0] != "$", str(t[0]))))
#         lines.append(f"  I{i}: {moves}")
#     return "\n".join(lines)

# def table_to_text(ACTION, GOTO, terms, nts):
#     action_cols = terms + ["$"]
#     goto_cols = [A for A in nts if A != nts[0]]
#     headers = ["State"] + action_cols + goto_cols
#     rows = []
#     for i in range(len(ACTION)):
#         row = [f"I{i}"]
#         row += [ACTION[i].get(a, "") for a in action_cols]
#         row += [GOTO[i].get(A, "") for A in goto_cols]
#         rows.append(row)
#     col_w = [max(len(h), max(len(str(r[c])) for r in rows)) for c, h in enumerate(headers)]
#     def fmt_row(vals):
#         return " | ".join(str(v).ljust(col_w[k]) for k, v in enumerate(vals))
#     sep = "-+-".join("-"*w for w in col_w)
#     return "\n".join([fmt_row(headers), sep] + [fmt_row(r) for r in rows])

# # ---------- Optional LALR parse ----------

# def lalr_parse(input_string, ACTION, GOTO):
#     stack = [0]
#     w = list(input_string) + ["$"]
#     ip = 0
#     trace = []
#     while True:
#         s = stack[-1]
#         a = w[ip]
#         act = ACTION[s].get(a, "")
#         trace.append((" ".join(map(str, stack)), "".join(w[ip:]), act))
#         if act == "":
#             trace.append((" ".join(map(str, stack)), "".join(w[ip:]), "ERROR"))
#             break
#         if act == "acc":
#             break
#         if act.startswith("s "):
#             j = int(act[2:])
#             stack.append(a); stack.append(j)
#             ip += 1
#         elif act.startswith("r "):
#             prod = act[2:]
#             A, rhs = prod.split("->")
#             A = A.strip(); rhs_syms = rhs.strip().split()
#             m = 0 if rhs_syms == ["ε"] else 2*len(rhs_syms)
#             for _ in range(m):
#                 stack.pop()
#             t = stack[-1]
#             stack.append(A)
#             j = GOTO[t][A]
#             stack.append(j)
#         else:
#             trace.append((" ".join(map(str, stack)), "".join(w[ip:]), "ERROR"))
#             break
#     return trace

# # Render table (console)
# def render_table(headers, rows):
#     col_w = [max(len(h), max(len(str(r[c])) for r in rows)) for c, h in enumerate(headers)]
#     def fmt(vals): return " | ".join(str(v).ljust(col_w[i]) for i, v in enumerate(vals))
#     sep = "-+-".join("-"*w for w in col_w)
#     return "\n".join([fmt(headers), sep] + [fmt(r) for r in rows])










# def enumerate_productions(Glst):
#     """
#     Return dict mapping (A, tuple(rhs)) -> production_number starting at 1 (or 0 if preferred).
#     Order is NT insertion order then their productions order.
#     """
#     pid = {}
#     k = 1
#     for A, prods in Glst.items():
#         for p in prods:
#             pid[(A, tuple(p))] = k
#             k += 1
#     return pid

# def format_action_cell(val, prod_ids):
#     if not val:
#         return ""
#     if val == "acc":
#         return "Accept"
#     if val.startswith("s "):
#         return "S" + val.split()[1]
#     if val.startswith("r "):
#         # val like 'r A->α'
#         prod = val[2:]
#         A, rhs = prod.split("->", 1)
#         A = A.strip()
#         rhs_syms = rhs.strip().split()
#         if rhs_syms == []:
#             # shouldn't happen
#             key = (A, tuple(["ε"]))
#         elif rhs_syms == ["ε"]:
#             key = (A, tuple(["ε"]))
#         else:
#             key = (A, tuple(rhs_syms))
#         k = prod_ids.get(key, None)
#         return f"R{k}" if k is not None else f"R({A}->{rhs.strip()})"
#     return val

# def number_productions(Gaug, Glst):
#     """
#     Returns prod_num[(A, tuple(rhs))] = k and prod_list[k] = (A, tuple(rhs))
#     Numbering:
#       0: S' -> S
#       1.. : original productions in file/insertion order
#     """
#     prod_num = {}
#     prod_list = []
#     k = 0
#     # Augmented start
#     start_rhs = tuple(Glst[next(iter(Gaug))][0])  # S' first key in Gaug
#     S_dash = next(iter(Gaug))
#     prod_num[(S_dash, start_rhs)] = k
#     prod_list.append((S_dash, start_rhs)); k += 1
#     # Rest in insertion order, skipping S'
#     for A in list(Gaug.keys())[1:]:
#         for rhs in Glst[A]:
#             t = (A, tuple(rhs))
#             prod_num[t] = k
#             prod_list.append(t); k += 1
#     return prod_num, prod_list


# # ---------- Main ----------

# # if __name__ == "__main__":
# #     # Load and augment
# #     Gstr = read_strings("grammar.txt")
# #     Gaug, S_dash, S = augment_grammar(Gstr)
# #     Glst = to_symbol_lists(Gaug)

# #     print("Augmented grammar:")
# #     for A, Ps in Gaug.items():
# #         print(f"{A} -> {' | '.join(Ps)}")

# #     # CLR (LR(1)) collection and table
# #     first = compute_first(Glst)
# #     clr_states, clr_trans = canonical_lr1(Glst, S_dash, first)

# #     print("\nCLR (LR(1)) item sets:")
# #     for i, I in enumerate(clr_states):
# #         print(state_lr1_str_merged_lookaheads(i, I))

# #     print(transitions_to_str(clr_trans))

# #     ACTION_CLR, GOTO_CLR, terms, nts, clr_conf = build_lr1_table(Glst, S_dash, clr_states, clr_trans)
# #     print("\nCLR Parsing Table")
# #     print(table_to_text(ACTION_CLR, GOTO_CLR, terms, nts))
# #     if clr_conf:
# #         print("\nCLR Conflicts:")
# #         for i, sym, old, new in clr_conf:
# #             print(f"  I{i}, on '{sym}': {old} vs {new}")
# #     else:
# #         print("\nNo conflicts in CLR table.")

# #     # Merge CLR -> LALR and build table
# #     lalr_states, lalr_trans = merge_clr_states(clr_states, clr_trans)

# #     print("\nLALR merged item sets (from CLR cores):")
# #     for i, I in enumerate(lalr_states):
# #         print(state_lalr_str_merged_lookaheads(i, I))  # same merged lookahead view

# #     print(transitions_to_str(lalr_trans))

# #     ACTION_LALR, GOTO_LALR, terms2, nts2, lalr_conf = build_lalr_table(Glst, S_dash, lalr_states, lalr_trans)
# #     print("\nLALR Parsing Table")
# #     print(table_to_text(ACTION_LALR, GOTO_LALR, terms2, nts2))
# #     if lalr_conf:
# #         print("\nLALR Conflicts:")
# #         for i, sym, old, new in lalr_conf:
# #             print(f"  I{i}, on '{sym}': {old} vs {new}")
# #     else:
# #         print("\nNo conflicts in LALR table.")

# #     # Optional parse if LALR is conflict-free
# #     if not lalr_conf:
# #         try:
# #             s = input("\nEnter input string to parse with LALR (without $): ").strip()
# #         except EOFError:
# #             s = ""
# #         if s:
# #             trace = lalr_parse(s, ACTION_LALR, GOTO_LALR)
# #             print("\n{:<24} | {:<18} | {}".format("STATE STACK", "INPUT", "ACTION"))
# #             print("-"*72)
# #             for stck, inp, act in trace:
# #                 print("{:<24} | {:<18} | {}".format(stck, inp, act))







# if __name__ == "__main__":
#     # Load and augment
#     Gstr = read_strings("grammar.txt")
#     Gaug, S_dash, S = augment_grammar(Gstr)
#     Glst = to_symbol_lists(Gaug)

#     print("Augmented grammar:")
#     for A, Ps in Gaug.items():
#         print(f"{A} -> {' | '.join(Ps)}")

#     # CLR (LR(1)) collection
#     first = compute_first(Glst)
#     clr_states, clr_trans = canonical_lr1(Glst, S_dash, first)

#     print("\nCLR (LR(1)) item sets (merged lookaheads):")
#     for i, I in enumerate(clr_states):
#         print(state_lr1_str_merged_lookaheads(i, I))

#     print(transitions_to_str(clr_trans))

#     # CLR parsing table
#     prod_num, prod_list = number_productions(Gaug, Glst)
#     ACTION_CLR, GOTO_CLR, terms, nts, clr_conf = build_lr1_table(Glst, S_dash, clr_states, clr_trans, prod_num)
#     print("\nCLR Parsing Table")
#     print(table_to_text(ACTION_CLR, GOTO_CLR, terms, nts))  # will show Rk/Sj/Accept

#     # ACTION_CLR, GOTO_CLR, terms, nts, clr_conf = build_lr1_table(Glst, S_dash, clr_states, clr_trans)
#     # print("\nCLR Parsing Table")
#     # print(table_to_text(ACTION_CLR, GOTO_CLR, terms, nts))
#     if clr_conf:
#         print("\nCLR Conflicts:")
#         for i, sym, old, new in clr_conf:
#             print(f"  I{i}, on '{sym}': {old} vs {new}")
#     else:
#         print("\nNo conflicts in CLR table.")

#     # Merge CLR -> LALR with labels and sequence
#     (lalr_states, lalr_trans,
#      clr_to_merged_idx, merged_idx_to_label,
#      sequence_labels, merged_flag) = merge_clr_with_labels(clr_states, clr_trans)

#     # Show CLR indices mapped to LALR labels in encounter order (repeats allowed)
#     print("\nCLR indices mapped to LALR labels in encounter order:")
#     print(", ".join(f"I{lab}" for lab in sequence_labels))

#     if not merged_flag:
#         print("\nNo sets to merge; LALR equals CLR.")
#     else:
#         print("\nLALR merged item sets (from CLR cores; merged lookaheads):")
#         # Print each unique merged state once with its label
#         for mi in range(len(lalr_states)):
#             lab = merged_idx_to_label[mi]
#             print(state_str_with_label(lab, lalr_states[mi]))
#         print(transitions_str_labeled(lalr_trans, merged_idx_to_label))

#     # LALR parsing table with labeled rows
#     ACTION_LALR, GOTO_LALR, terms2, nts2, lalr_conf, headers, rows = build_lalr_table_labeled(
#         Glst, S_dash, lalr_states, lalr_trans, merged_idx_to_label
#     )

#     print("\nLALR Parsing Table (labeled rows)")
#     print(render_table(headers, rows))
#     if lalr_conf:
#         print("\nLALR Conflicts:")
#         for i, sym, old, new in lalr_conf:
#             print(f"  I{merged_idx_to_label[i]}, on '{sym}': {old} vs {new}")
#     else:
#         print("\nNo conflicts in LALR table.")

#     # Optional parse if LALR is conflict-free
#     if not lalr_conf:
#         try:
#             s = input("\nEnter input string to parse with LALR (without $): ").strip()
#         except EOFError:
#             s = ""
#         if s:
#             trace = lalr_parse(s, ACTION_LALR, GOTO_LALR)
#             print("\n{:<24} | {:<18} | {}".format("STATE STACK", "INPUT", "ACTION"))
#             print("-"*72)
#             for stck, inp, act in trace:
#                 print("{:<24} | {:<18} | {}".format(stck, inp, act))



























#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------












# # clr_lalr.py
# # -*- coding: utf-8 -*-
# from collections import defaultdict, deque

# # ---------- IO and tokenization ----------

# def read_strings(filepath):
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

# def augment_grammar(Gstr):
#     if not Gstr:
#         raise ValueError("Empty grammar.")
#     S = next(iter(Gstr))
#     S_dash = S + "'"
#     while S_dash in Gstr:
#         S_dash += "'"
#     Gaug = {S_dash: [S]}
#     Gaug.update(Gstr)
#     return Gaug, S_dash, S

# # ---------- FIRST sets ----------

# def compute_first(Glst):
#     nts = list(Glst.keys())
#     nts_set = set(nts)
#     first = {A: set() for A in Glst}
#     changed = True
#     while changed:
#         changed = False
#         for A in Glst:
#             for prod in Glst[A]:
#                 k = 0
#                 while k < len(prod):
#                     X = prod[k]
#                     if X == "ε":
#                         if "ε" not in first[A]:
#                             first[A].add("ε")
#                             changed = True
#                         break
#                     if X not in nts_set:
#                         if X not in first[A]:
#                             first[A].add(X)
#                             changed = True
#                         break
#                     add = first[X] - {"ε"}
#                     if not add.issubset(first[A]):
#                         first[A].update(add)
#                         changed = True
#                     if "ε" not in first[X]:
#                         break
#                     k += 1
#                 else:
#                     if "ε" not in first[A]:
#                         first[A].add("ε")
#                         changed = True
#     return first

# def first_of_seq(seq, first, Glst):
#     nts_set = set(Glst.keys())
#     out = set()
#     if not seq:
#         out.add("ε")
#         return out
#     for X in seq:
#         if X in nts_set:
#             out |= (first[X] - {"ε"})
#             if "ε" not in first[X]:
#                 break
#         else:
#             out.add(X)
#             break
#     else:
#         out.add("ε")
#     return out

# # ---------- CLR (LR(1)) items and automaton ----------

# # LR(1) item: (A, tuple(rhs), dot_pos, lookahead)

# def lr1_closure(I, Glst, first):
#     I = set(I)
#     nts = set(Glst.keys())
#     changed = True
#     while changed:
#         changed = False
#         add_list = []
#         for (A, beta, dot, la) in list(I):
#             if dot < len(beta):
#                 X = beta[dot]
#                 if X in nts:
#                     tail = list(beta[dot+1:])
#                     la_set = first_of_seq(tail + [la], first, Glst)
#                     for prod in Glst[X]:
#                         for a in (la_set or {"$"}):
#                             if a == "ε":
#                                 continue
#                             it = (X, tuple(prod), 0, a)
#                             if it not in I and it not in add_list:
#                                 add_list.append(it)
#         if add_list:
#             I.update(add_list)
#             changed = True
#     return I

# def lr1_goto(I, X, Glst, first):
#     J = set()
#     for (A, beta, dot, la) in I:
#         if dot < len(beta) and beta[dot] == X:
#             J.add((A, beta, dot+1, la))
#     if not J:
#         return set()
#     return lr1_closure(J, Glst, first)

# def symbol_order(Glst):
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

# def canonical_lr1(Glst, S_dash, first):
#     start_prod = Glst[S_dash][0]
#     I0 = lr1_closure({(S_dash, tuple(start_prod), 0, "$")}, Glst, first)
#     states = [I0]
#     trans = {}
#     work = deque([0])
#     ordered_symbols = symbol_order(Glst)
#     while work:
#         i = work.popleft()
#         I = states[i]
#         for X in ordered_symbols:
#             J = lr1_goto(I, X, Glst, first)
#             if not J:
#                 continue
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

# # ---------- Production numbering ----------

# def number_productions(Gaug, Glst):
#     """
#     Number productions to emit Rk in ACTION:
#       0: S' -> S
#       1..: rest in insertion order
#     """
#     prod_num = {}
#     prod_list = []
#     k = 0
#     S_dash = next(iter(Gaug))
#     start_rhs = tuple(Glst[S_dash][0])
#     prod_num[(S_dash, start_rhs)] = k
#     prod_list.append((S_dash, start_rhs))
#     k += 1
#     for A in list(Gaug.keys())[1:]:
#         for rhs in Glst[A]:
#             t = (A, tuple(rhs))
#             prod_num[t] = k
#             prod_list.append(t)
#             k += 1
#     return prod_num, prod_list

# # ---------- Tables (CLR and LALR) ----------

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

# def build_lr1_table(Glst, S_dash, states, trans, prod_num):
#     nts, terms = collect_terminals_nonterminals(Glst)
#     action_terms = terms + ["$"]
#     ACTION = {i: {a: "" for a in action_terms} for i in range(len(states))}
#     GOTO   = {i: {A: "" for A in nts} for i in range(len(states))}
#     conflicts = []

#     # Shifts and GOTOs
#     for (i, X), j in trans.items():
#         if X in nts:
#             GOTO[i][X] = j
#         else:
#             old = ACTION[i][X]; new = f"S{j}"
#             if old and old != new:
#                 conflicts.append((i, X, old, new))
#             ACTION[i][X] = new

#     # Reductions and Accept
#     # Reductions and Accept (ensure ε-productions write cells)
#     for i, I in enumerate(states):
#         for (A, p, dot, la) in I:
#             if dot == len(p):
#                 if A == S_dash:
#                     old = ACTION[i]["$"]; new = "Accept"
#                     if old and old != new:
#                         conflicts.append((i, "$", old, new))
#                     ACTION[i]["$"] = new
#                 else:
#                     # Try numbered reduce; fallback to textual
#                     k = None
#                     try:
#                         k = prod_num[(A, p)]
#                     except KeyError:
#                         pass
#                     new = f"R{k}" if k is not None else f"r {A}->{('ε' if (len(p)==1 and p[0]=='ε') else ' '.join(p))}"
#                     old = ACTION[i][la]
#                     if old and old != new:
#                         conflicts.append((i, la, old, new))
#                     ACTION[i][la] = new

    
#     # for i, I in enumerate(states):
#     #     for (A, p, dot, la) in I:
#     #         if dot == len(p):
#     #             if A == S_dash:
#     #                 old = ACTION[i]["$"]; new = "Accept"
#     #                 if old and old != new:
#     #                     conflicts.append((i, "$", old, new))
#     #                 ACTION[i]["$"] = new
#     #             else:
#     #                 k = prod_num[(A, p)]
#     #                 new = f"R{k}"
#     #                 old = ACTION[i][la]
#     #                 if old and old != new:
#     #                     conflicts.append((i, la, old, new))
#     #                 ACTION[i][la] = new

#     return ACTION, GOTO, terms, nts, conflicts

# # ---------- Merge CLR -> LALR with labels ----------

# def group_clr_by_core(states):
#     core_to_indices = defaultdict(list)
#     order = []
#     for i, I in enumerate(states):
#         core = frozenset((A, p, dot) for (A, p, dot, la) in I)
#         if core not in core_to_indices:
#             order.append(core)
#         core_to_indices[core].append(i)
#     groups = [core_to_indices[c] for c in order]
#     return core_to_indices, groups

# def label_for_group(g):
#     return "".join(str(k) for k in sorted(g))

# def merge_clr_with_labels(states, trans):
#     _, groups = group_clr_by_core(states)
#     merged_states = []
#     merged_idx_to_label = {}
#     core_to_merged_idx = {}
#     cores = [frozenset((A, p, dot) for (A, p, dot, la) in I) for I in states]

#     for g in groups:
#         la_map = defaultdict(set)
#         for i in g:
#             for (A, p, dot, la) in states[i]:
#                 la_map[(A, p, dot)].add(la)
#         merged = set()
#         for (A, p, dot), LAs in la_map.items():
#             for a in sorted(LAs):
#                 merged.add((A, p, dot, a))
#         idx = len(merged_states)
#         merged_states.append(merged)
#         lab = label_for_group(g)
#         merged_idx_to_label[idx] = lab
#         core_to_merged_idx[cores[g[0]]] = idx

#     clr_to_merged_idx = {}
#     for i, I in enumerate(states):
#         clr_to_merged_idx[i] = core_to_merged_idx[cores[i]]

#     merged_trans = {}
#     for (i, X), j in trans.items():
#         mi = clr_to_merged_idx[i]
#         mj = clr_to_merged_idx[j]
#         merged_trans[(mi, X)] = mj

#     sequence_labels = []
#     for i in range(len(states)):
#         mi = clr_to_merged_idx[i]
#         sequence_labels.append(merged_idx_to_label[mi])

#     merged_flag = any(len(g) > 1 for g in groups)
#     return merged_states, merged_trans, clr_to_merged_idx, merged_idx_to_label, sequence_labels, merged_flag

# # ---------- Rendering (state prints with ε hidden) ----------

# def item_core_str_hide_epsilon(A, p, dot):
#     # Show empty RHS for ε-production
#     if len(p) == 1 and p[0] == "ε":
#         return f"{A} -> •"
#     syms = list(p)
#     syms.insert(dot, "•")
#     return f"{A} -> {' '.join(syms) if syms else '•'}"

# def state_lr1_str_merged_lookaheads(idx, I):
#     la_map = defaultdict(set)
#     for (A, p, dot, la) in I:
#         la_map[(A, p, dot)].add(la)
#     cores_sorted = sorted(la_map.keys(), key=lambda x: (x[0], x[1], x[2]))
#     lines = [f"I{idx}:"]
#     for (A, p, dot) in cores_sorted:
#         core_txt = item_core_str_hide_epsilon(A, p, dot)
#         las = " | ".join(sorted(la_map[(A, p, dot)], key=str))
#         lines.append(f"  {core_txt}, {las}")
#     return "\n".join(lines)

# def state_str_with_label(label, I):
#     la_map = defaultdict(set)
#     for (A, p, dot, la) in I:
#         la_map[(A, p, dot)].add(la)
#     cores_sorted = sorted(la_map.keys(), key=lambda x: (x[0], x[1], x[2]))
#     lines = [f"I{label}:"]
#     for (A, p, dot) in cores_sorted:
#         core_txt = item_core_str_hide_epsilon(A, p, dot)
#         las = " | ".join(sorted(la_map[(A, p, dot)], key=str))
#         lines.append(f"  {core_txt}, {las}")
#     return "\n".join(lines)

# def transitions_to_str(trans):
#     by_src = defaultdict(list)
#     for (i, X), j in trans.items():
#         by_src[i].append((X, j))
#     lines = ["\nGOTO transitions:"]
#     for i in sorted(by_src.keys()):
#         moves = ", ".join(f"on {X} -> I{j}" for X, j in sorted(by_src[i], key=lambda t: (t[0] != "$", str(t[0]))))
#         lines.append(f"  I{i}: {moves}")
#     return "\n".join(lines)

# def transitions_str_labeled(merged_trans, merged_idx_to_label):
#     by_src = defaultdict(list)
#     for (i, X), j in merged_trans.items():
#         by_src[i].append((X, j))
#     lines = ["\nGOTO transitions (LALR labels):"]
#     for i in sorted(by_src.keys()):
#         moves = ", ".join(
#             f"on {X} -> I{merged_idx_to_label[j]}"
#             for X, j in sorted(by_src[i], key=lambda t: (t[0] != "$", str(t[0])))
#         )
#         lines.append(f"  I{merged_idx_to_label[i]}: {moves}")
#     return "\n".join(lines)

# def table_to_text(ACTION, GOTO, terms, nts):
#     action_cols = terms + ["$"]
#     goto_cols = [A for A in nts if A != nts[0]]
#     headers = ["State"] + action_cols + goto_cols
#     rows = []
#     for i in range(len(ACTION)):
#         row = [f"I{i}"]
#         row += [ACTION[i].get(a, "") for a in action_cols]
#         row += [GOTO[i].get(A, "") for A in goto_cols]
#         rows.append(row)
#     col_w = [max(len(h), max(len(str(r[c])) for r in rows)) for c, h in enumerate(headers)]
#     def fmt_row(vals):
#         return " | ".join(str(v).ljust(col_w[k]) for k, v in enumerate(vals))
#     sep = "-+-".join("-"*w for w in col_w)
#     return "\n".join([fmt_row(headers), sep] + [fmt_row(r) for r in rows])

# # ---------- LALR table (labeled rows) ----------

# def build_lalr_table_labeled(Glst, S_dash, lalr_states, lalr_trans, merged_idx_to_label, prod_num):
#     ACTION, GOTO, terms, nts, conflicts = build_lr1_table(Glst, S_dash, lalr_states, lalr_trans, prod_num)
#     row_labels = [merged_idx_to_label[i] for i in range(len(lalr_states))]
#     action_cols = terms + ["$"]
#     goto_cols = [A for A in nts if A != nts[0]]
#     rows = []
#     for i, lab in enumerate(row_labels):
#         row = [lab] + [ACTION[i].get(a, "") for a in action_cols] + [GOTO[i].get(A, "") for A in goto_cols]
#         rows.append(row)
#     headers = ["State"] + action_cols + goto_cols
#     return ACTION, GOTO, terms, nts, conflicts, headers, rows

# # ---------- Optional LALR parse ----------

# def lalr_parse(input_string, ACTION, GOTO):
#     stack = [0]
#     w = list(input_string) + ["$"]
#     ip = 0
#     trace = []
#     while True:
#         s = stack[-1]
#         a = w[ip]
#         act = ACTION[s].get(a, "")
#         trace.append((" ".join(map(str, stack)), "".join(w[ip:]), act))
#         if act == "":
#             trace.append((" ".join(map(str, stack)), "".join(w[ip:]), "ERROR"))
#             break
#         if act == "Accept":
#             break
#         if act.startswith("S"):
#             j = int(act[1:])
#             stack.append(a); stack.append(j)
#             ip += 1
#         elif act.startswith("R"):
#             # This parser uses only table entries; no need to map Rk back to text here
#             # Pop count cannot be recovered from Rk alone; normally we would carry prod_list.
#             # For demo, treat R as single-symbol pop is not correct; keep table-only trace or store prod_list for full parsing.
#             # If full parsing is required, pass prod_list and map Rk -> (A, rhs) to pop 2*len(rhs).
#             trace.append((" ".join(map(str, stack)), "".join(w[ip:]), "ERROR (R needs prod mapping)"))
#             break
#         else:
#             trace.append((" ".join(map(str, stack)), "".join(w[ip:]), "ERROR"))
#             break
#     return trace

# # ---------- Render helper (for labeled tables) ----------

# def render_table(headers, rows):
#     col_w = [max(len(h), max(len(str(r[c])) for r in rows)) for c, h in enumerate(headers)]
#     def fmt(vals): return " | ".join(str(v).ljust(col_w[i]) for i, v in enumerate(vals))
#     sep = "-+-".join("-"*w for w in col_w)
#     return "\n".join([fmt(headers), sep] + [fmt(r) for r in rows])

# # ---------- Main ----------

# if __name__ == "__main__":
#     # Load and augment
#     Gstr = read_strings("grammar.txt")
#     Gaug, S_dash, S = augment_grammar(Gstr)
#     Glst = to_symbol_lists(Gaug)

#     print("Augmented grammar:")
#     for A, Ps in Gaug.items():
#         print(f"{A} -> {' | '.join(Ps)}")

#     # CLR (LR(1)) collection
#     first = compute_first(Glst)
#     clr_states, clr_trans = canonical_lr1(Glst, S_dash, first)

#     print("\nCLR (LR(1)) item sets (merged lookaheads):")
#     for i, I in enumerate(clr_states):
#         print(state_lr1_str_merged_lookaheads(i, I))

#     print(transitions_to_str(clr_trans))

#     # Production numbering for Rk in tables
#     prod_num, prod_list = number_productions(Gaug, Glst)

#     # CLR parsing table (Sx / Ry / Accept)
#     ACTION_CLR, GOTO_CLR, terms, nts, clr_conf = build_lr1_table(Glst, S_dash, clr_states, clr_trans, prod_num)
#     print("\nCLR Parsing Table")
#     print(table_to_text(ACTION_CLR, GOTO_CLR, terms, nts))
#     if clr_conf:
#         print("\nCLR Conflicts:")
#         for i, sym, old, new in clr_conf:
#             print(f"  I{i}, on '{sym}': {old} vs {new}")
#     else:
#         print("\nNo conflicts in CLR table.")

#     # Merge CLR -> LALR with labels
#     (lalr_states, lalr_trans,
#      clr_to_merged_idx, merged_idx_to_label,
#      sequence_labels, merged_flag) = merge_clr_with_labels(clr_states, clr_trans)

#     print("\nCLR indices mapped to LALR labels in encounter order:")
#     print(", ".join(f"I{lab}" for lab in sequence_labels))

#     if not merged_flag:
#         print("\nNo sets to merge; LALR equals CLR.")
#     else:
#         print("\nLALR merged item sets (from CLR cores; merged lookaheads):")
#         for mi in range(len(lalr_states)):
#             lab = merged_idx_to_label[mi]
#             print(state_str_with_label(lab, lalr_states[mi]))
#         print(transitions_str_labeled(lalr_trans, merged_idx_to_label))

#     # LALR parsing table with labeled rows
#     ACTION_LALR, GOTO_LALR, terms2, nts2, lalr_conf, headers, rows = build_lalr_table_labeled(
#         Glst, S_dash, lalr_states, lalr_trans, merged_idx_to_label, prod_num
#     )
#     print("\nLALR Parsing Table (labeled rows)")
#     print(render_table(headers, rows))
#     if lalr_conf:
#         print("\nLALR Conflicts:")
#         for i, sym, old, new in lalr_conf:
#             print(f"  I{merged_idx_to_label[i]}, on '{sym}': {old} vs {new}")
#     else:
#         print("\nNo conflicts in LALR table.")

#     # Optional: parsing trace using LALR table would require mapping Rk -> (A, rhs)
#     # You can extend lalr_parse to accept prod_list to pop correct counts.





















































# clr_lalr.py
# -*- coding: utf-8 -*-
from collections import defaultdict, deque
import graphviz

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
    # ε means empty production
    if prod == "ε" or prod == "":
        return []
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

def augment_grammar(Gstr):
    if not Gstr:
        raise ValueError("Empty grammar.")
    S = next(iter(Gstr))
    S_dash = S + "'"
    while S_dash in Gstr:
        S_dash += "'"
    Gaug = {S_dash: [S]}
    Gaug.update(Gstr)
    return Gaug, S_dash, S

# ---------- FIRST sets ----------

def compute_first(Glst):
    nts = list(Glst.keys())
    nts_set = set(nts)
    first = {A: set() for A in Glst}
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
                    X = prod[k]
                    if X not in nts_set:
                        if X not in first[A]:
                            first[A].add(X)
                            changed = True
                        break
                    add = first[X] - {"ε"}
                    if not add.issubset(first[A]):
                        first[A].update(add)
                        changed = True
                    if "ε" not in first[X]:
                        break
                    k += 1
                else:
                    if "ε" not in first[A]:
                        first[A].add("ε")
                        changed = True
    return first


def first_of_seq(seq, first, Glst):
    nts_set = set(Glst.keys())
    out = set()
    if not seq:
        out.add("ε")
        return out
    for X in seq:
        if X in nts_set:
            out |= (first[X] - {"ε"})
            if "ε" not in first[X]:
                break
        else:
            out.add(X)
            break
    else:
        out.add("ε")
    return out


# ---------- CLR (LR(1)) items and automaton ----------

# LR(1) item: (A, tuple(rhs), dot_pos, lookahead)

def lr1_closure(I, Glst, first):
    I = set(I)
    nts = set(Glst.keys())
    changed = True
    while changed:
        changed = False
        add_list = []
        for (A, beta, dot, la) in list(I):
            if dot < len(beta):
                X = beta[dot]
                if X in nts:
                    tail = list(beta[dot+1:])
                    la_set = first_of_seq(tail + [la], first, Glst)
                    for prod in Glst[X]:
                        for a in la_set:
                            if a == "ε":
                                continue
                            it = (X, tuple(prod), 0, a)
                            if it not in I and it not in add_list:
                                add_list.append(it)
        if add_list:
            I.update(add_list)
            changed = True
    return I


def lr1_goto(I, X, Glst, first):
    J = set()
    for (A, beta, dot, la) in I:
        if dot < len(beta) and beta[dot] == X:
            J.add((A, beta, dot+1, la))
    if not J:
        return set()
    return lr1_closure(J, Glst, first)

def symbol_order(Glst):
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

def canonical_lr1(Glst, S_dash, first):
    start_prod = Glst[S_dash][0]
    I0 = lr1_closure({(S_dash, tuple(start_prod), 0, "$")}, Glst, first)
    states = [I0]
    trans = {}
    work = deque([0])
    ordered_symbols = symbol_order(Glst)
    while work:
        i = work.popleft()
        I = states[i]
        for X in ordered_symbols:
            J = lr1_goto(I, X, Glst, first)
            if not J:
                continue
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

# ---------- Production numbering ----------

def number_productions(Gaug, Glst):
    """
    Number productions to emit Rk in ACTION:
      0: S' -> S
      1..: rest in insertion order
    """
    prod_num = {}
    prod_list = []
    k = 0
    S_dash = next(iter(Gaug))
    start_rhs = tuple(Glst[S_dash][0])
    prod_num[(S_dash, start_rhs)] = k
    prod_list.append((S_dash, start_rhs))
    k += 1
    for A in list(Gaug.keys())[1:]:
        for rhs in Glst[A]:
            t = (A, tuple(rhs))
            prod_num[t] = k
            prod_list.append(t)
            k += 1
    return prod_num, prod_list

# ---------- Tables (CLR and LALR) ----------
def collect_terminals_nonterminals(Glst):
    nts = list(Glst.keys())
    nts_set = set(nts)
    terms = set()
    for A, prods in Glst.items():
        for p in prods:
            for s in p:
                if s not in nts_set:
                    terms.add(s)
    return nts, sorted(terms, key=str)

def build_lr1_table(Glst, S_dash, states, trans, prod_num):
    nts, terms = collect_terminals_nonterminals(Glst)
    action_terms = terms + ["$"]
    ACTION = {i: {a: "" for a in action_terms} for i in range(len(states))}
    GOTO   = {i: {A: "" for A in nts} for i in range(len(states))}
    conflicts = []

    for (i, X), j in trans.items():
        if X in nts:
            GOTO[i][X] = j
        else:
            old = ACTION[i][X]; new = f"S{j}"
            if old and old != new:
                conflicts.append((i, X, old, new))
            ACTION[i][X] = new

    for i, I in enumerate(states):
        for (A, p, dot, la) in I:
            if dot == len(p):
                if A == S_dash:
                    old = ACTION[i]["$"]; new = "Accept"
                    if old and old != new:
                        conflicts.append((i, "$", old, new))
                    ACTION[i]["$"] = new
                else:
                    # prefer numbered production
                    k = prod_num.get((A, p))
                    if k is not None:
                        new = f"R{k}"
                    else:
                        rhs_txt = "ε" if len(p) == 0 else " ".join(p)
                        new = f"r {A}->{rhs_txt}"
                    old = ACTION[i][la]
                    if old and old != new:
                        conflicts.append((i, la, old, new))
                    ACTION[i][la] = new
    return ACTION, GOTO, terms, nts, conflicts

# ---------- Merge CLR -> LALR with labels ----------

def group_clr_by_core(states):
    core_to_indices = defaultdict(list)
    order = []
    for i, I in enumerate(states):
        core = frozenset((A, p, dot) for (A, p, dot, la) in I)
        if core not in core_to_indices:
            order.append(core)
        core_to_indices[core].append(i)
    groups = [core_to_indices[c] for c in order]
    return core_to_indices, groups

def label_for_group(g):
    return "".join(str(k) for k in sorted(g))

def merge_clr_with_labels(states, trans):
    _, groups = group_clr_by_core(states)
    merged_states = []
    merged_idx_to_label = {}
    core_to_merged_idx = {}
    cores = [frozenset((A, p, dot) for (A, p, dot, la) in I) for I in states]

    for g in groups:
        la_map = defaultdict(set)
        for i in g:
            for (A, p, dot, la) in states[i]:
                la_map[(A, p, dot)].add(la)
        merged = set()
        for (A, p, dot), LAs in la_map.items():
            for a in sorted(LAs):
                merged.add((A, p, dot, a))
        idx = len(merged_states)
        merged_states.append(merged)
        lab = label_for_group(g)
        merged_idx_to_label[idx] = lab
        core_to_merged_idx[cores[g[0]]] = idx

    clr_to_merged_idx = {}
    for i, I in enumerate(states):
        clr_to_merged_idx[i] = core_to_merged_idx[cores[i]]

    merged_trans = {}
    for (i, X), j in trans.items():
        mi = clr_to_merged_idx[i]
        mj = clr_to_merged_idx[j]
        merged_trans[(mi, X)] = mj

    sequence_labels = []
    for i in range(len(states)):
        mi = clr_to_merged_idx[i]
        sequence_labels.append(merged_idx_to_label[mi])

    merged_flag = any(len(g) > 1 for g in groups)
    return merged_states, merged_trans, clr_to_merged_idx, merged_idx_to_label, sequence_labels, merged_flag

# ---------- Rendering (state prints with ε hidden) ----------

def item_core_str_hide_epsilon(A, p, dot):
    # p is a tuple/list; empty means ε-production
    if len(p) == 0:
        # dot can only be 0 or len(p)=0, completion equals dot==0
        return f"{A} -> •"
    syms = list(p)
    syms.insert(dot, "•")
    return f"{A} -> {' '.join(syms)}"



def state_lr1_str_merged_lookaheads(idx, I):
    la_map = defaultdict(set)
    for (A, p, dot, la) in I:
        la_map[(A, p, dot)].add(la)
    cores_sorted = sorted(la_map.keys(), key=lambda x: (x[0], x[1], x[2]))
    lines = [f"I{idx}:"]
    for (A, p, dot) in cores_sorted:
        core_txt = item_core_str_hide_epsilon(A, p, dot)
        las = " | ".join(sorted(la_map[(A, p, dot)], key=str))
        lines.append(f"  {core_txt}, {las}")
    return "\n".join(lines)

def state_str_with_label(label, I):
    la_map = defaultdict(set)
    for (A, p, dot, la) in I:
        la_map[(A, p, dot)].add(la)
    cores_sorted = sorted(la_map.keys(), key=lambda x: (x[0], x[1], x[2]))
    lines = [f"I{label}:"]
    for (A, p, dot) in cores_sorted:
        core_txt = item_core_str_hide_epsilon(A, p, dot)
        las = " | ".join(sorted(la_map[(A, p, dot)], key=str))
        lines.append(f"  {core_txt}, {las}")
    return "\n".join(lines)

def transitions_to_str(trans):
    by_src = defaultdict(list)
    for (i, X), j in trans.items():
        by_src[i].append((X, j))
    lines = ["\nGOTO transitions:"]
    for i in sorted(by_src.keys()):
        moves = ", ".join(f"on {X} -> I{j}" for X, j in sorted(by_src[i], key=lambda t: (t[0] != "$", str(t[0]))))
        lines.append(f"  I{i}: {moves}")
    return "\n".join(lines)

def transitions_str_labeled(merged_trans, merged_idx_to_label):
    by_src = defaultdict(list)
    for (i, X), j in merged_trans.items():
        by_src[i].append((X, j))
    lines = ["\nGOTO transitions (LALR labels):"]
    for i in sorted(by_src.keys()):
        moves = ", ".join(
            f"on {X} -> I{merged_idx_to_label[j]}"
            for X, j in sorted(by_src[i], key=lambda t: (t[0] != "$", str(t[0])))
        )
        lines.append(f"  I{merged_idx_to_label[i]}: {moves}")
    return "\n".join(lines)

def table_to_text(ACTION, GOTO, terms, nts):
    action_cols = terms + ["$"]
    goto_cols = [A for A in nts if A != nts[0]]
    headers = ["State"] + action_cols + goto_cols
    rows = []
    for i in range(len(ACTION)):
        row = [f"I{i}"]
        row += [ACTION[i].get(a, "") for a in action_cols]
        row += [GOTO[i].get(A, "") for A in goto_cols]
        rows.append(row)
    col_w = [max(len(h), max(len(str(r[c])) for r in rows)) for c, h in enumerate(headers)]
    def fmt_row(vals):
        return " | ".join(str(v).ljust(col_w[k]) for k, v in enumerate(vals))
    sep = "-+-".join("-"*w for w in col_w)
    return "\n".join([fmt_row(headers), sep] + [fmt_row(r) for r in rows])

# ---------- LALR table (labeled rows) ----------

def build_lalr_table_labeled(Glst, S_dash, lalr_states, lalr_trans, merged_idx_to_label, prod_num):
    ACTION, GOTO, terms, nts, conflicts = build_lr1_table(Glst, S_dash, lalr_states, lalr_trans, prod_num)
    row_labels = [merged_idx_to_label[i] for i in range(len(lalr_states))]
    action_cols = terms + ["$"]
    goto_cols = [A for A in nts if A != nts[0]]
    rows = []
    for i, lab in enumerate(row_labels):
        row = [lab] + [ACTION[i].get(a, "") for a in action_cols] + [GOTO[i].get(A, "") for A in goto_cols]
        rows.append(row)
    headers = ["State"] + action_cols + goto_cols
    return ACTION, GOTO, terms, nts, conflicts, headers, rows

# ---------- Optional LALR parse ----------
def lalr_parse(input_string, ACTION, GOTO, prod_list):
    stack = [0]
    w = list(input_string) + ["$"]
    ip = 0
    trace = []
    while True:
        s = stack[-1]
        a = w[ip]
        act = ACTION[s].get(a, "")
        trace.append((" ".join(map(str, stack)), "".join(w[ip:]), act))
        if act == "":
            trace.append((" ".join(map(str, stack)), "".join(w[ip:]), "ERROR"))
            break
        if act == "Accept":
            break
        if act.startswith("S"):
            j = int(act[1:])
            stack.append(a); stack.append(j)
            ip += 1
        elif act.startswith("R"):
            k = int(act[1:])
            A, rhs = prod_list[k]
            m = 2 * len(rhs)  # 0 if empty
            for _ in range(m):
                stack.pop()
            t = stack[-1]
            stack.append(A)
            stack.append(GOTO[t][A])
        else:
            trace.append((" ".join(map(str, stack)), "".join(w[ip:]), "ERROR"))
            break
    return trace

# ---------- Render helper (for labeled tables) ----------

def render_table(headers, rows):
    col_w = [max(len(h), max(len(str(r[c])) for r in rows)) for c, h in enumerate(headers)]
    def fmt(vals): return " | ".join(str(v).ljust(col_w[i]) for i, v in enumerate(vals))
    sep = "-+-".join("-"*w for w in col_w)
    return "\n".join([fmt(headers), sep] + [fmt(r) for r in rows])





def parse_with_rnums(input_string, ACTION, GOTO, prod_list):
    """
    Generic LR parser using ACTION (Sx/Rk/Accept) and GOTO, with prod_list[k]=(A, rhs_tuple).
    Returns a trace of (state_stack, input_suffix, action_taken).
    """
    stack = [0]
    w = list(input_string) + ["$"]
    ip = 0
    trace = []
    while True:
        s = stack[-1]
        a = w[ip]
        act = ACTION[s].get(a, "")
        trace.append((" ".join(map(str, stack)), "".join(w[ip:]), act))
        if act == "":
            trace.append((" ".join(map(str, stack)), "".join(w[ip:]), "ERROR"))
            break
        if act == "Accept":
            break
        if act.startswith("S"):
            j = int(act[1:])
            stack.append(a); stack.append(j)
            ip += 1
        elif act.startswith("R"):
            k = int(act[1:])
            A, rhs = prod_list[k]
            m = 2 * len(rhs)  # 0 if ε (empty tuple)
            for _ in range(m):
                stack.pop()
            t = stack[-1]
            stack.append(A)
            goto_next = GOTO[t][A]
            if goto_next == "":
                trace.append((" ".join(map(str, stack)), "".join(w[ip:]), "ERROR (missing GOTO)"))
                break
            stack.append(goto_next)
        else:
            trace.append((" ".join(map(str, stack)), "".join(w[ip:]), "ERROR"))
            break
    return trace

# def print_trace(title, trace):
#     print(f"\n[{title}] {:<24} | {:<18} | {}".format("STATE STACK", "INPUT", "ACTION"))
#     print("-" * 80)
#     for stack_str, input_str, act in trace:
#         print("{:<24} | {:<18} | {}".format(stack_str, input_str, act))





#---------Diagram---------
def render_lr_automaton(states, trans, state_label_fn):
    """
    Build and return a Graphviz Digraph for LR automaton.
    states: list of canonical item sets
    trans: dict (src, symbol) -> tgt
    state_label_fn: function to stringify a state (must accept (idx, state))
    """
    import graphviz
    g = graphviz.Digraph(format="png")
    g.attr(rankdir="LR")  # Left-to-right

    for idx, state in enumerate(states):
        label = state_label_fn(idx, state)
        label = label.replace("\n", "\\n")  # Important for graphviz multiline labels
        g.node(f"I{idx}", label=label, shape="ellipse")

    for (src, sym), tgt in trans.items():
        g.edge(f"I{src}", f"I{tgt}", label=str(sym))

    return g


# def render_lr_automaton(states, trans, state_label_fn):
#     """
#     Build and return a Graphviz Digraph for LR automaton.
#     states: list of canonical item sets
#     trans: dict (src, symbol) -> tgt
#     state_label_fn: function to stringify a state (must accept (idx, state))
#     """
#     g = graphviz.Digraph(format="png")
#     g.attr(rankdir="LR")  # LR: left-to-right

#     # Add nodes with labels
#     for idx, state in enumerate(states):
#         label = state_label_fn(idx, state)
#         g.node(f"I{idx}", label=label, shape="ellipse")

#     # Add transitions (edges)
#     for (src, sym), tgt in trans.items():
#         g.edge(f"I{src}", f"I{tgt}", label=str(sym))

#     return g

# ---------- Main ----------

if __name__ == "__main__":
    # ---- Load and augment ----
    Gstr = read_strings("grammar.txt")
    Gaug, S_dash, S = augment_grammar(Gstr)
    Glst = to_symbol_lists(Gaug)

    print("Augmented grammar:")
    for A, Ps in Gaug.items():
        print(f"{A} -> {' | '.join(Ps)}")

    # ---- CLR (LR(1)) canonical collection ----
    first = compute_first(Glst)
    clr_states, clr_trans = canonical_lr1(Glst, S_dash, first)

    print("\nCLR (LR(1)) item sets (merged lookaheads):")
    for i, I in enumerate(clr_states):
        print(state_lr1_str_merged_lookaheads(i, I))

    print(transitions_to_str(clr_trans))

    # ---- Production numbering for Rk ----
    prod_num, prod_list = number_productions(Gaug, Glst)

    # ---- CLR parsing table ----
    ACTION_CLR, GOTO_CLR, terms, nts, clr_conf = build_lr1_table(Glst, S_dash, clr_states, clr_trans, prod_num)
    print("\nCLR Parsing Table")
    print(table_to_text(ACTION_CLR, GOTO_CLR, terms, nts))
    if clr_conf:
        print("\nCLR Conflicts:")
        for i, sym, old, new in clr_conf:
            print(f"  I{i}, on '{sym}': {old} vs {new}")
    else:
        print("\nNo conflicts in CLR table.")

    # ---- Merge CLR -> LALR with labels ----
    (lalr_states, lalr_trans,
     clr_to_merged_idx, merged_idx_to_label,
     sequence_labels, merged_flag) = merge_clr_with_labels(clr_states, clr_trans)

    print("\nCLR indices mapped to LALR labels in encounter order:")
    print(", ".join(f"I{lab}" for lab in sequence_labels))

    if not merged_flag:
        print("\nNo sets to merge; LALR equals CLR.")
    else:
        print("\nLALR merged item sets (from CLR cores; merged lookaheads):")
        for mi in range(len(lalr_states)):
            lab = merged_idx_to_label[mi]
            print(state_str_with_label(lab, lalr_states[mi]))
        print(transitions_str_labeled(lalr_trans, merged_idx_to_label))

    # ---- LALR parsing table with labeled rows ----
    ACTION_LALR, GOTO_LALR, terms2, nts2, lalr_conf, headers, rows = build_lalr_table_labeled(
        Glst, S_dash, lalr_states, lalr_trans, merged_idx_to_label, prod_num
    )
    print("\nLALR Parsing Table (labeled rows)")
    print(render_table(headers, rows))
    if lalr_conf:
        print("\nLALR Conflicts:")
        for i, sym, old, new in lalr_conf:
            print(f"  I{merged_idx_to_label[i]}, on '{sym}': {old} vs {new}")
    else:
        print("\nNo conflicts in LALR table.")

    # ---- Decide which traces to show ----
    clr_ok = (len(clr_conf) == 0)
    lalr_ok = (len(lalr_conf) == 0)

    if not clr_ok and not lalr_ok:
        print("\nBoth CLR and LALR tables have conflicts. Parsing is disabled.")
    else:
        try:
            inp = input("\nEnter input string to parse (without $): ").strip()
        except EOFError:
            inp = ""
        if inp:
            if clr_ok:
                trace_clr = parse_with_rnums(inp, ACTION_CLR, GOTO_CLR, prod_list)
                print("\n[CLR Trace] {:<24} | {:<18} | {}".format("STACK", "INPUT", "ACTION"))
                print("-" * 80)
                for stack_str, input_str, act in trace_clr:
                    print("{:<24} | {:<18} | {}".format(stack_str, input_str, act))
            else:
                print("\nCLR table has conflicts; skipping CLR parse.")

            if lalr_ok:
                trace_lalr = parse_with_rnums(inp, ACTION_LALR, GOTO_LALR, prod_list)
                print("\n[LALR Trace] {:<24} | {:<18} | {}".format("STACK", "INPUT", "ACTION"))
                print("-" * 80)
                for stack_str, input_str, act in trace_lalr:
                    print("{:<24} | {:<18} | {}".format(stack_str, input_str, act))
            else:
                print("\nLALR table has conflicts; skipping LALR parse.")




# if __name__ == "__main__":
#     # Load and augment
#     Gstr = read_strings("grammar.txt")
#     Gaug, S_dash, S = augment_grammar(Gstr)
#     Glst = to_symbol_lists(Gaug)

#     print("Augmented grammar:")
#     for A, Ps in Gaug.items():
#         print(f"{A} -> {' | '.join(Ps)}")

#     # CLR (LR(1)) collection
#     first = compute_first(Glst)
#     clr_states, clr_trans = canonical_lr1(Glst, S_dash, first)

#     print("\nCLR (LR(1)) item sets (merged lookaheads):")
#     for i, I in enumerate(clr_states):
#         print(state_lr1_str_merged_lookaheads(i, I))

#     print(transitions_to_str(clr_trans))

#     # Production numbering for Rk in tables
#     prod_num, prod_list = number_productions(Gaug, Glst)

#     # CLR parsing table (Sx / Ry / Accept)
#     ACTION_CLR, GOTO_CLR, terms, nts, clr_conf = build_lr1_table(Glst, S_dash, clr_states, clr_trans, prod_num)
#     print("\nCLR Parsing Table")
#     print(table_to_text(ACTION_CLR, GOTO_CLR, terms, nts))
#     if clr_conf:
#         print("\nCLR Conflicts:")
#         for i, sym, old, new in clr_conf:
#             print(f"  I{i}, on '{sym}': {old} vs {new}")
#     else:
#         print("\nNo conflicts in CLR table.")

#     # Merge CLR -> LALR with labels
#     (lalr_states, lalr_trans,
#      clr_to_merged_idx, merged_idx_to_label,
#      sequence_labels, merged_flag) = merge_clr_with_labels(clr_states, clr_trans)

#     print("\nCLR indices mapped to LALR labels in encounter order:")
#     print(", ".join(f"I{lab}" for lab in sequence_labels))

#     if not merged_flag:
#         print("\nNo sets to merge; LALR equals CLR.")
#     else:
#         print("\nLALR merged item sets (from CLR cores; merged lookaheads):")
#         for mi in range(len(lalr_states)):
#             lab = merged_idx_to_label[mi]
#             print(state_str_with_label(lab, lalr_states[mi]))
#         print(transitions_str_labeled(lalr_trans, merged_idx_to_label))

#     # LALR parsing table with labeled rows
#     ACTION_LALR, GOTO_LALR, terms2, nts2, lalr_conf, headers, rows = build_lalr_table_labeled(
#         Glst, S_dash, lalr_states, lalr_trans, merged_idx_to_label, prod_num
#     )
#     print("\nLALR Parsing Table (labeled rows)")
#     print(render_table(headers, rows))
#     if lalr_conf:
#         print("\nLALR Conflicts:")
#         for i, sym, old, new in lalr_conf:
#             print(f"  I{merged_idx_to_label[i]}, on '{sym}': {old} vs {new}")
#     else:
#         print("\nNo conflicts in LALR table.")





# if __name__ == "__main__":
#     # Load and augment
#     Gstr = read_strings("grammar.txt")
#     Gaug, S_dash, S = augment_grammar(Gstr)
#     Glst = to_symbol_lists(Gaug)

#     print("Augmented grammar:")
#     for A, Ps in Gaug.items():
#         print(f"{A} -> {' | '.join(Ps)}")

#     # CLR (LR(1)) collection
#     first = compute_first(Glst)
#     clr_states, clr_trans = canonical_lr1(Glst, S_dash, first)

#     print("\nCLR (LR(1)) item sets (merged lookaheads):")
#     for i, I in enumerate(clr_states):
#         print(state_lr1_str_merged_lookaheads(i, I))

#     print(transitions_to_str(clr_trans))

#     # Production numbering for Rk in tables
#     prod_num, prod_list = number_productions(Gaug, Glst)

#     # CLR parsing table (Sx / Ry / Accept)
#     ACTION_CLR, GOTO_CLR, terms, nts, clr_conf = build_lr1_table(Glst, S_dash, clr_states, clr_trans, prod_num)
#     print("\nCLR Parsing Table")
#     print(table_to_text(ACTION_CLR, GOTO_CLR, terms, nts))
#     if clr_conf:
#         print("\nCLR Conflicts:")
#         for i, sym, old, new in clr_conf:
#             print(f"  I{i}, on '{sym}': {old} vs {new}")
#     else:
#         print("\nNo conflicts in CLR table.")

#     # Merge CLR -> LALR with labels
#     (lalr_states, lalr_trans,
#      clr_to_merged_idx, merged_idx_to_label,
#      sequence_labels, merged_flag) = merge_clr_with_labels(clr_states, clr_trans)

#     print("\nCLR indices mapped to LALR labels in encounter order:")
#     print(", ".join(f"I{lab}" for lab in sequence_labels))

#     if not merged_flag:
#         print("\nNo sets to merge; LALR equals CLR.")
#     else:
#         print("\nLALR merged item sets (from CLR cores; merged lookaheads):")
#         for mi in range(len(lalr_states)):
#             lab = merged_idx_to_label[mi]
#             print(state_str_with_label(lab, lalr_states[mi]))
#         print(transitions_str_labeled(lalr_trans, merged_idx_to_label))

#     # LALR parsing table with labeled rows
#     ACTION_LALR, GOTO_LALR, terms2, nts2, lalr_conf, headers, rows = build_lalr_table_labeled(
#         Glst, S_dash, lalr_states, lalr_trans, merged_idx_to_label, prod_num
#     )
#     print("\nLALR Parsing Table (labeled rows)")
#     print(render_table(headers, rows))
#     if lalr_conf:
#         print("\nLALR Conflicts:")
#         for i, sym, old, new in lalr_conf:
#             print(f"  I{merged_idx_to_label[i]}, on '{sym}': {old} vs {new}")
#     else:
#         print("\nNo conflicts in LALR table.")

#     # Optional: parsing trace using LALR table would require mapping Rk -> (A, rhs)
#     # You can extend lalr_parse to accept prod_list to pop correct counts.






