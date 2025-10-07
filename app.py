# import streamlit as st

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

# def read_grammar_from_input(text):
#     grammar = {}
#     lines = text.strip().split('\n')
#     for line in lines:
#         if '->' in line:
#             nt, rhs = line.split("->")
#             grammar[nt.strip()] = [prod.strip() for prod in rhs.split('|')]
#     return grammar

# st.title("Left Recursion Removal Tool")

# st.write("Enter grammar rules (one per line), e.g.:")
# st.code("""E -> E+T | T
# T -> T*F | F
# F -> (E) | id""", language='text')

# grammar_input = st.text_area("Enter your grammar here", height=200)

# if st.button("Remove Left Recursion"):
#     if not grammar_input.strip():
#         st.warning("Please enter your grammar first.")
#     else:
#         # Save to grammar.txt
#         with open("grammar.txt", "w") as f:
#             f.write(grammar_input)

#         grammar = read_grammar_from_input(grammar_input)
#         transformed_grammar = remove_left_recursion(grammar)

#         st.success("Left recursion removed. Transformed grammar:")
#         for nt, prods in transformed_grammar.items():
#             st.write(f"{nt} -> {' | '.join(prods)}")




# import streamlit as st
# import first_follow
# import left_recursion
# import left_factoring

# st.title("Grammar Analysis Tool")

# st.write("Enter grammar rules (one per line), e.g.:")
# st.code("""S -> aBDh
# B -> cC
# C -> bC | ε
# D -> EF
# E -> g | ε
# F -> f | ε
# """, language='text')

# grammar_input = st.text_area("Enter your grammar here", height=250)

# operation = st.selectbox(
#     "Choose operation",
#     ["First & Follow", "Left Recursion Removal", "Left Factoring"]
# )

# if st.button("Process"):
#     if not grammar_input.strip():
#         st.warning("Please enter your grammar first.")
#     else:
#         # Save input to grammar.txt
#         with open("grammar.txt", "w", encoding="utf-8") as f:
#             f.write(grammar_input)


#         if operation == "First & Follow":
#             grammar = first_follow.read_grammar_from_file("grammar.txt")
#             first = first_follow.compute_first(grammar)
#             follow = first_follow.compute_follow(grammar, first)

#             st.success("FIRST sets:")
#             for nt in first:
#                 st.write(f"First({nt}) = {{ {', '.join(('∈' if s == 'ε' else s) for s in sorted(first[nt]))} }}")

#             st.success("FOLLOW sets:")
#             for nt in follow:
#                 st.write(f"Follow({nt}) = {{ {', '.join(('∈' if s == 'ε' else s) for s in sorted(follow[nt]))} }}")

#         elif operation == "Left Recursion Removal":
#             grammar = left_recursion.read_grammar_from_file("grammar.txt")
#             transformed = left_recursion.remove_left_recursion(grammar)

#             st.success("Left Recursion Removed Grammar:")
#             for nt, prods in transformed.items():
#                 st.write(f"{nt} -> {' | '.join(prods)}")

#         elif operation == "Left Factoring":
#             grammar = left_factoring.read_grammar_from_file("grammar.txt")
#             factored = left_factoring.left_factoring(grammar)

#             st.success("Left Factored Grammar:")
#             for nt, prods in factored.items():
#                 st.write(f"{nt} -> {' | '.join(prods)}")




















# import streamlit as st
# import first_follow
# import left_recursion

# st.title("Grammar Analysis with Left Recursion Removal")

# st.write("Enter grammar rules (one per line), e.g.:")
# st.code("""S -> aBDh
# B -> cC
# C -> bC | ε
# D -> EF
# E -> g | ε
# F -> f | ε
# """, language='text')

# grammar_input = st.text_area("Enter your grammar here", height=250)

# if st.button("Process Grammar"):
#     if not grammar_input.strip():
#         st.warning("Please enter your grammar first.")
#     else:
#         # Save input grammar to file with UTF-8 encoding
#         with open("grammar.txt", "w", encoding="utf-8") as f:
#             f.write(grammar_input)

#         # Read and convert for left recursion removal
#         grammar = first_follow.read_grammar_from_file("grammar.txt")
#         grammar_str = {nt: [''.join(prod) for prod in prods] for nt, prods in grammar.items()}

#         # Remove left recursion
#         grammar_no_lr = left_recursion.remove_left_recursion(grammar_str)

#         # Display grammar after removing left recursion
#         st.subheader("Grammar After Removing Left Recursion:")
#         for nt, prods in grammar_no_lr.items():
#             st.write(f"{nt} -> {' | '.join(prods)}")

#         # Convert back for first/follow calculation
#         grammar_processed = {}
#         for nt, prods in grammar_no_lr.items():
#             grammar_processed[nt] = [list(prod) if prod != 'ε' else ['ε'] for prod in prods]

#         # Compute first and follow
#         first = first_follow.compute_first(grammar_processed)
#         follow = first_follow.compute_follow(grammar_processed, first)

#         # Display First sets
#         st.subheader("FIRST sets:")
#         for nt in first:
#             first_set = ', '.join('∈' if s == 'ε' else s for s in sorted(first[nt]))
#             st.write(f"First({nt}) = {{ {first_set} }}")

#         # Display Follow sets
#         st.subheader("FOLLOW sets:")
#         for nt in follow:
#             follow_set = ', '.join('∈' if s == 'ε' else s for s in sorted(follow[nt]))
#             st.write(f"Follow({nt}) = {{ {follow_set} }}")











# # app.py
# # -*- coding: utf-8 -*-

# import streamlit as st
# import left_recursion
# import left_factoring
# import first_follow

# st.title("Grammar Toolkit")

# st.write("Enter grammar rules (one per line):")
# st.code("""Example:
# S -> aBDh
# B -> cC
# C -> bC | ε
# D -> EF
# E -> g | ε
# F -> f | ε
# """, language="text")

# grammar_input = st.text_area("Enter your grammar here", height=220, placeholder="A -> aA | b\nB -> c | ε")

# action = st.selectbox(
#     "Select an operation",
#     ["Remove left recursion", "Remove left factoring", "Find First and Follow"],
#     index=0,
# )

# if st.button("Run"):
#     if not grammar_input.strip():
#         st.warning("Please enter your grammar first.")
#         st.stop()

#     # Persist the grammar to file for the modules to use
#     with open("grammar.txt", "w", encoding="utf-8") as f:
#         f.write(grammar_input)

#     if action == "Remove left recursion":
#         # Uses the high-level function that detects LR and removes if present
#         changed, outG, report = left_recursion.remove_left_recursion_if_any("grammar.txt")

#         st.subheader("Left Recursion Check")
#         # Human-readable detector summary
#         lines = []
#         if report.get("has_direct"):
#             lines.append("Direct left recursion detected.")
#         else:
#             lines.append("No direct left recursion.")
#         if report.get("has_indirect"):
#             lines.append("Indirect left recursion suspected (cycles present).")
#         else:
#             lines.append("No indirect left recursion.")
#         st.write("\n".join(lines))

#         if changed:
#             st.subheader("Grammar after removing left recursion")
#             for nt, prods in outG.items():
#                 st.write(f"{nt} -> {' | '.join(prods)}")
#         else:
#             st.info("No left recursion in the given grammar. Nothing to remove.")

#     elif action == "Remove left factoring":
#         # Read strings and factor using left_factoring module interface
#         grammar = left_factoring.read_grammar_from_file("grammar.txt")
#         factored = left_factoring.left_factoring(grammar)
#         st.subheader("Grammar after left factoring")
#         for nt, prods in factored.items():
#             st.write(f"{nt} -> {' | '.join(prods)}")

#     elif action == "Find First and Follow":
#         # Let first_follow handle LR internally if detected
#         grammar_list, changed, shown_text = first_follow.load_prepare_remove_lr_if_needed("grammar.txt")

#         st.subheader("Grammar used for FIRST/FOLLOW")
#         st.text(shown_text)

#         first = first_follow.compute_first(grammar_list)
#         follow = first_follow.compute_follow(grammar_list, first)

#         st.subheader("FIRST sets")
#         for nt in first:
#             shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(first[nt], key=lambda v: (v == "ε", v)))
#             st.write(f"First({nt}) = {{ {shown} }}")

#         st.subheader("FOLLOW sets")
#         for nt in follow:
#             shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(follow[nt], key=lambda v: (v == "ε", v)))
#             st.write(f"Follow({nt}) = {{ {shown} }}")




















# # -*- coding: utf-8 -*-
# import streamlit as st
# import left_recursion
# import left_factoring
# import first_follow

# st.title("Grammar Toolkit")

# st.write("Enter grammar rules (one per line). Use ε for epsilon and -> for productions.")
# st.code("""Example:
# S -> iEtS | iEtSeS | a
# E -> b | ε
# """, language="text")

# # Session state for grammar input
# if "grammar_text" not in st.session_state:
#     st.session_state.grammar_text = ""

# # # Optional selection helpers (workaround for cursor position)
# # with st.expander("Insertion helpers (optional)"):
# #     colA, colB, colC = st.columns([1, 1, 2])
# #     with colA:
# #         sel_start = st.number_input("Selection start", min_value=0, value=0, step=1)
# #     with colB:
# #         sel_end = st.number_input("Selection end", min_value=0, value=0, step=1)
# #     with colC:
# #         st.caption("Leave both as 0 to insert at the end. Provide start=end to insert at that index. If start<end, selected range is replaced.")

# def insert_text(base: str, to_insert: str, start: int, end: int) -> str:
#     n = len(base)
#     start = max(0, min(start, n))
#     end = max(0, min(end, n))
#     if start > end:
#         start, end = end, start
#     if start == 0 and end == 0:
#         # Append at end by default
#         return base + to_insert
#     # Replace the slice [start:end] with to_insert
#     return base[:start] + to_insert + base[end:]

# col1, col2 = st.columns([1, 1])
# with col1:
#     if st.button("Add ε"):
#         st.session_state.grammar_text = insert_text(
#             st.session_state.grammar_text, "ε", sel_start, sel_end
#         )
# with col2:
#     if st.button("Add ->"):
#         st.session_state.grammar_text = insert_text(
#             st.session_state.grammar_text, " -> ", sel_start, sel_end
#         )

# st.session_state.grammar_text = st.text_area(
#     "Grammar", value=st.session_state.grammar_text, height=220
# )

# action = st.selectbox(
#     "Select an operation",
#     ["Remove left recursion", "Remove left factoring", "Find First and Follow"],
#     index=0,
# )

# if st.button("Run"):
#     text = st.session_state.grammar_text
#     if not text.strip():
#         st.warning("Please enter your grammar first.")
#         st.stop()

#     # Persist grammar to file (UTF-8 to preserve ε)
#     with open("grammar.txt", "w", encoding="utf-8") as f:
#         f.write(text)

#     if action == "Remove left recursion":
#         changed, outG, report = left_recursion.remove_left_recursion_if_any("grammar.txt")

#         st.subheader("Left Recursion Check")
#         lines = []
#         if report.get("has_direct"):
#             lines.append("Direct left recursion detected.")
#         else:
#             lines.append("No direct left recursion.")
#         if report.get("has_indirect"):
#             lines.append("Indirect left recursion suspected (cycles present).")
#         else:
#             lines.append("No indirect left recursion.")
#         st.write("\n".join(lines))

#         if changed:
#             st.subheader("Grammar after removing left recursion")
#             for nt, prods in outG.items():
#                 st.write(f"{nt} -> {' | '.join(prods)}")
#         else:
#             st.info("No left recursion in the given grammar. Nothing to remove.")

#     elif action == "Remove left factoring":
#         grammar = left_factoring.read_grammar_from_file("grammar.txt")
#         factored = left_factoring.left_factoring(grammar)
#         st.subheader("Grammar after left factoring")
#         for nt, prods in factored.items():
#             st.write(f"{nt} -> {' | '.join(prods)}")

#     elif action == "Find First and Follow":
#         # Use first_follow orchestration (which removes LR if present)
#         grammar_list, changed_lr, shown_text = first_follow.load_prepare_remove_lr_if_needed("grammar.txt")

#         st.subheader("Grammar used for FIRST/FOLLOW")
#         st.text(shown_text)

#         first = first_follow.compute_first(grammar_list)
#         follow = first_follow.compute_follow(grammar_list, first)

#         st.subheader("FIRST sets")
#         for nt in first:
#             shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(first[nt], key=lambda v: (v == "ε", v)))
#             st.write(f"First({nt}) = {{ {shown} }}")

#         st.subheader("FOLLOW sets")
#         for nt in follow:
#             shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(follow[nt], key=lambda v: (v == "ε", v)))
#             st.write(f"Follow({nt}) = {{ {shown} }}")









# # -*- coding: utf-8 -*-
# import streamlit as st
# import left_recursion
# import left_factoring
# import first_follow

# st.title("Grammar Toolkit")

# st.write("Enter grammar rules (one per line). Use ε for epsilon and -> for productions.")
# st.code("""Example:
# S -> iEtS | iEtSeS | a
# E -> b | ε
# """, language="text")

# if "grammar_text" not in st.session_state:
#     st.session_state.grammar_text = ""

# # Insert buttons: backend-only append to end
# c1, c2 = st.columns([1, 1])
# with c1:
#     if st.button("Add ε"):
#         st.session_state.grammar_text = st.session_state.grammar_text + "ε"
# with c2:
#     if st.button("Add ->"):
#         st.session_state.grammar_text = st.session_state.grammar_text + " -> "

# # Main text area
# st.session_state.grammar_text = st.text_area(
#     "Grammar", value=st.session_state.grammar_text, height=220
# )

# action = st.selectbox(
#     "Select an operation",
#     ["Remove left recursion", "Remove left factoring", "Find First and Follow"],
#     index=0,
# )

# if st.button("Run"):
#     text = st.session_state.grammar_text
#     if not text.strip():
#         st.warning("Please enter your grammar first.")
#         st.stop()

#     # Persist grammar to file (UTF-8 to preserve ε)
#     with open("grammar.txt", "w", encoding="utf-8") as f:
#         f.write(text)

#     if action == "Remove left recursion":
#         changed, outG, report = left_recursion.remove_left_recursion_if_any("grammar.txt")

#         st.subheader("Left Recursion Check")
#         lines = []
#         lines.append("Direct left recursion detected." if report.get("has_direct") else "No direct left recursion.")
#         lines.append("Indirect left recursion suspected (cycles present)." if report.get("has_indirect") else "No indirect left recursion.")
#         st.write("\n".join(lines))

#         if changed:
#             st.subheader("Grammar after removing left recursion")
#             for nt, prods in outG.items():
#                 st.write(f"{nt} -> {' | '.join(prods)}")
#         else:
#             st.info("No left recursion in the given grammar. Nothing to remove.")

#     elif action == "Remove left factoring":
#         grammar = left_factoring.read_grammar_from_file("grammar.txt")
#         factored = left_factoring.left_factoring(grammar)
#         st.subheader("Grammar after left factoring")
#         for nt, prods in factored.items():
#             st.write(f"{nt} -> {' | '.join(prods)}")

#     elif action == "Find First and Follow":
#         grammar_list, changed_lr, shown_text = first_follow.load_prepare_remove_lr_if_needed("grammar.txt")

#         st.subheader("Grammar used for FIRST/FOLLOW")
#         st.text(shown_text)

#         first = first_follow.compute_first(grammar_list)
#         follow = first_follow.compute_follow(grammar_list, first)

#         st.subheader("FIRST sets")
#         for nt in first:
#             shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(first[nt], key=lambda v: (v == "ε", v)))
#             st.write(f"First({nt}) = {{ {shown} }}")

#         st.subheader("FOLLOW sets")
#         for nt in follow:
#             shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(follow[nt], key=lambda v: (v == "ε", v)))
#             st.write(f"Follow({nt}) = {{ {shown} }}")

#-------------------------------------------------------------------















# # -*- coding: utf-8 -*-
# import streamlit as st
# import left_recursion
# import left_factoring
# import first_follow





# def validate_grammar_text(text: str):
#     """
#     Returns (ok: bool, error_msg: str). Checks minimal CFG line format:
#     <NT> -> prod1 | prod2 | ...
#     - requires '->' exactly once per non-empty line
#     - LHS non-empty, no spaces
#     - each RHS production non-empty after strip, or equals 'ε'
#     """
#     lines = [ln.rstrip() for ln in text.splitlines()]
#     for idx, line in enumerate(lines, start=1):
#         if not line.strip():
#             # allow blank lines; skip
#             continue
#         if line.count("->") != 1:
#             return False, f"Line {idx}: each rule must contain exactly one '->'."
#         lhs, rhs = line.split("->", 1)
#         lhs = lhs.strip()
#         rhs = rhs.strip()
#         if not lhs:
#             return False, f"Line {idx}: left-hand side (nonterminal) is empty."
#         if " " in lhs:
#             return False, f"Line {idx}: nonterminal '{lhs}' must not contain spaces."
#         if not rhs:
#             return False, f"Line {idx}: right-hand side is empty."
#         parts = [p.strip() for p in rhs.split("|")]
#         if any(p == "" for p in parts):
#             return False, f"Line {idx}: empty production found; use 'ε' for empty."
#         # allow ε explicitly; other tokens are free-form here
#     return True, ""




# st.set_page_config(page_title="Grammar Toolkit", page_icon="🧩", layout="centered")
# st.title("Grammar Toolkit")


# # st.caption("Quick copy symbols (select and copy):")
# # c1, c2 = st.columns(2)
# # with c1:
# #     st.text_input("Epsilon (copy)", value="ε", key="copy_eps", disabled=True, label_visibility="collapsed")
# # with c2:
# #     st.text_input("Arrow (copy)", value=" -> ", key="copy_arrow", disabled=True, label_visibility="collapsed")







# st.code("""Example:
# S -> iEtS | iEtSeS | a
# E -> b | ε
# """, language="text")


# st.write("Enter grammar rules (one per line). Use ε for epsilon and -> for productions.")

# # Clipboard copy buttons (ε and ->)
# st.caption("Quick copy symbols:")
# col1, col2 = st.columns(2)
# with col1:
#     st.code("ε", language="text")  # has a native copy button
# with col2:
#     st.code(" -> ", language="text")


# if "grammar_text" not in st.session_state:
#     st.session_state.grammar_text = ""

# st.session_state.grammar_text = st.text_area(
#     "Grammar", value=st.session_state.grammar_text, height=220, placeholder="A -> aA | b\nB -> c | ε"
# )

# action = st.selectbox(
#     "Select an operation",
#     ["Remove left recursion", "Remove left factoring", "Find First and Follow"],
#     index=0,
# )

# # if st.button("Run"):
#     # text = st.session_state.grammar_text
#     # if not text.strip():
#     #     st.warning("Please enter your grammar first.")
#     #     st.stop()
# if st.button("Run"):
#     text = st.session_state.grammar_text if "grammar_text" in st.session_state else ""
#     if not text or not text.strip():
#         st.error("Please enter correct grammar. The input cannot be empty.")
#         st.stop()

#     ok, err = validate_grammar_text(text)  # your validator from earlier
#     if not ok:
#         st.error(f"Please enter correct grammar. {err}")
#         st.stop()

#     # Persist grammar to file (UTF-8 to preserve ε)
#     with open("grammar.txt", "w", encoding="utf-8") as f:
#         f.write(text)

#     if action == "Remove left recursion":
#         # Uses your integrated detector + remover
#         changed, outG, report = left_recursion.remove_left_recursion_if_any("grammar.txt")

#         st.subheader("Left Recursion Check")
#         lines = []
#         lines.append("Direct left recursion detected." if report.get("has_direct") else "No direct left recursion.")
#         lines.append("Indirect left recursion suspected (cycles present)." if report.get("has_indirect") else "No indirect left recursion.")
#         st.write("\n".join(lines))

#         if changed:
#             st.subheader("Grammar after removing left recursion")
#             for nt, prods in outG.items():
#                 st.write(f"{nt} -> {' | '.join(prods)}")
#         else:
#             st.info("No left recursion in the given grammar. Nothing to remove.")

#     elif action == "Remove left factoring":
#         grammar = left_factoring.read_grammar_from_file("grammar.txt")
#         factored = left_factoring.left_factoring(grammar)
#         st.subheader("Grammar after left factoring")
#         for nt, prods in factored.items():
#             st.write(f"{nt} -> {' | '.join(prods)}")

#     elif action == "Find First and Follow":
#         # Use first_follow orchestration which removes LR if present
#         grammar_list, changed_lr, shown_text = first_follow.load_prepare_remove_lr_if_needed("grammar.txt")

#         st.subheader("Grammar used for FIRST/FOLLOW")
#         st.text(shown_text)

#         first = first_follow.compute_first(grammar_list)
#         follow = first_follow.compute_follow(grammar_list, first)

#         st.subheader("FIRST sets")
#         for nt in first:
#             shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(first[nt], key=lambda v: (v == "ε", v)))
#             st.write(f"First({nt}) = {{ {shown} }}")

#         st.subheader("FOLLOW sets")
#         for nt in follow:
#             shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(follow[nt], key=lambda v: (v == "ε", v)))
#             st.write(f"Follow({nt}) = {{ {shown} }}")


# st.caption("Develop by Dharmik...")



#-----------------------------------------------


# # -*- coding: utf-8 -*-
# import streamlit as st
# import left_recursion
# import left_factoring
# import first_follow
# import ll1  # NEW

# def validate_grammar_text(text: str):
#     lines = [ln.rstrip() for ln in text.splitlines()]
#     for idx, line in enumerate(lines, start=1):
#         if not line.strip():
#             continue
#         if line.count("->") != 1:
#             return False, f"Line {idx}: each rule must contain exactly one '->'."
#         lhs, rhs = line.split("->", 1)
#         lhs = lhs.strip()
#         rhs = rhs.strip()
#         if not lhs:
#             return False, f"Line {idx}: left-hand side (nonterminal) is empty."
#         if " " in lhs:
#             return False, f"Line {idx}: nonterminal '{lhs}' must not contain spaces."
#         if not rhs:
#             return False, f"Line {idx}: right-hand side is empty."
#         parts = [p.strip() for p in rhs.split("|")]
#         if any(p == "" for p in parts):
#             return False, f"Line {idx}: empty production found; use 'ε' for empty."
#     return True, ""

# st.set_page_config(page_title="Grammar Toolkit", page_icon="🧩", layout="centered")
# st.title("Grammar Toolkit")

# st.code("""Example:
# S -> iEtS | iEtSeS | a
# E -> b | ε
# """, language="text")

# st.write("Enter grammar rules (one per line). Use ε for epsilon and -> for productions.")

# st.caption("Quick copy symbols:")
# col1, col2 = st.columns(2)
# with col1:
#     st.code("ε", language="text")
# with col2:
#     st.code(" -> ", language="text")

# if "grammar_text" not in st.session_state:
#     st.session_state.grammar_text = ""

# st.session_state.grammar_text = st.text_area(
#     "Grammar", value=st.session_state.grammar_text, height=220, placeholder="A -> aA | b\nB -> c | ε"
# )

# action = st.selectbox(
#     "Select an operation",
#     ["Remove left recursion", "Remove left factoring", "Find First and Follow", "LL(1) Table + Parse"],  # NEW
#     index=0,
# )

# if st.button("Run"):
#     text = st.session_state.grammar_text if "grammar_text" in st.session_state else ""
#     if not text or not text.strip():
#         st.error("Please enter correct grammar. The input cannot be empty.")
#         st.stop()

#     ok, err = validate_grammar_text(text)
#     if not ok:
#         st.error(f"Please enter correct grammar. {err}")
#         st.stop()

#     with open("grammar.txt", "w", encoding="utf-8") as f:
#         f.write(text)

#     if action == "Remove left recursion":
#         changed, outG, report = left_recursion.remove_left_recursion_if_any("grammar.txt")
#         st.subheader("Left Recursion Check")
#         lines = []
#         lines.append("Direct left recursion detected." if report.get("has_direct") else "No direct left recursion.")
#         lines.append("Indirect left recursion suspected (cycles present)." if report.get("has_indirect") else "No indirect left recursion.")
#         st.write("\n".join(lines))
#         if changed:
#             st.subheader("Grammar after removing left recursion")
#             for nt, prods in outG.items():
#                 st.write(f"{nt} -> {' | '.join(prods)}")
#         else:
#             st.info("No left recursion in the given grammar. Nothing to remove.")

#     elif action == "Remove left factoring":
#         grammar = left_factoring.read_grammar_from_file("grammar.txt")
#         factored = left_factoring.left_factoring(grammar)
#         st.subheader("Grammar after left factoring")
#         for nt, prods in factored.items():
#             st.write(f"{nt} -> {' | '.join(prods)}")

#     elif action == "Find First and Follow":
#         grammar_list, changed_lr, shown_text = first_follow.load_prepare_remove_lr_if_needed("grammar.txt")
#         st.subheader("Grammar used for FIRST/FOLLOW")
#         st.text(shown_text)
#         first = first_follow.compute_first(grammar_list)
#         follow = first_follow.compute_follow(grammar_list, first)
#         st.subheader("FIRST sets")
#         for nt in first:
#             shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(first[nt], key=lambda v: (v == "ε", v)))
#             st.write(f"First({nt}) = {{ {shown} }}")
#         st.subheader("FOLLOW sets")
#         for nt in follow:
#             shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(follow[nt], key=lambda v: (v == "ε", v)))
#             st.write(f"Follow({nt}) = {{ {shown} }}")

#     elif action == "LL(1) Table + Parse":  # NEW
#         # Build LL(1) artifacts
#         grammar_str, notes, first, follow, table, conflicts, terms = ll1.construct_ll1("grammar.txt")

#         st.subheader("Precondition checks")
#         for n in notes:
#             st.write(f"- {n}")

#         st.subheader("Grammar used")
#         for A, Ps in grammar_str.items():
#             st.write(f"{A} -> {' | '.join(Ps)}")

#         st.subheader("FIRST and FOLLOW")
#         for A, S in first.items():
#             shown = ", ".join(("∈" if x == "ε" else x) for x in sorted(S, key=lambda v: (v == "ε", v)))
#             st.write(f"First({A}) = {{ {shown} }}")
#         for A, S in follow.items():
#             shown = ", ".join(("∈" if x == "ε" else x) for x in sorted(S, key=lambda v: (v == "ε", v)))
#             st.write(f"Follow({A}) = {{ {shown} }}")

#         st.subheader("LL(1) Parsing Table")
#         # Pretty text table
#         st.text(ll1.pretty_table(table, terms))

#         if conflicts:
#             st.error("Conflicts detected (grammar is not LL(1)):")
#             for A, a, old, new in conflicts:
#                 st.write(f"M[{A}, {a}] conflict between [{old}] and [{new}]")
#         else:
#             st.success("No conflicts; grammar appears LL(1).")
#             # Input for string parsing
#             user_str = st.text_input("Enter input string to parse (without $)", key="parse_input")
#             if st.button("Parse"):
#                 if not user_str.strip():
#                     st.warning("Please enter a non-empty string.")
#                 else:
#                     accepted, steps = ll1.parse(table, grammar_str, terms, user_str.strip())
#                     st.subheader("Trace (Stack | Input | Action)")
#                     # Render as a table
#                     for stck, inp, act in steps:
#                         st.write(f"{stck:<25} | {inp:<25} | {act}")
#                     st.write(f"\nResult: {'ACCEPTED' if accepted else 'REJECTED'}")

# st.caption("Develop by Dharmik...")





















# # -*- coding: utf-8 -*-
# import streamlit as st
# import left_recursion
# import left_factoring
# import first_follow
# import ll1  # NEW

# def validate_grammar_text(text: str):
#     lines = [ln.rstrip() for ln in text.splitlines()]
#     for idx, line in enumerate(lines, start=1):
#         if not line.strip():
#             continue
#         if line.count("->") != 1:
#             return False, f"Line {idx}: each rule must contain exactly one '->'."
#         lhs, rhs = line.split("->", 1)
#         lhs = lhs.strip()
#         rhs = rhs.strip()
#         if not lhs:
#             return False, f"Line {idx}: left-hand side (nonterminal) is empty."
#         if " " in lhs:
#             return False, f"Line {idx}: nonterminal '{lhs}' must not contain spaces."
#         if not rhs:
#             return False, f"Line {idx}: right-hand side is empty."
#         parts = [p.strip() for p in rhs.split("|")]
#         if any(p == "" for p in parts):
#             return False, f"Line {idx}: empty production found; use 'ε' for empty."
#     return True, ""

# st.set_page_config(page_title="Grammar Toolkit", page_icon="🧩", layout="centered")
# st.title("Grammar Toolkit")

# st.code("""Example:
# S -> iEtS | iEtSeS | a
# E -> b | ε
# """, language="text")

# st.write("Enter grammar rules (one per line). Use ε for epsilon and -> for productions.")

# st.caption("Quick copy symbols:")
# col1, col2 = st.columns(2)
# with col1:
#     st.code("ε", language="text")
# with col2:
#     st.code(" -> ", language="text")

# if "grammar_text" not in st.session_state:
#     st.session_state.grammar_text = ""

# st.session_state.grammar_text = st.text_area(
#     "Grammar", value=st.session_state.grammar_text, height=220, placeholder="A -> aA | b\nB -> c | ε"
# )

# action = st.selectbox(
#     "Select an operation",
#     ["Remove left recursion", "Remove left factoring", "Find First and Follow", "LL(1) Table + Parse"],  # NEW
#     index=0,
# )

# if st.button("Run"):
#     text = st.session_state.grammar_text if "grammar_text" in st.session_state else ""
#     if not text or not text.strip():
#         st.error("Please enter correct grammar. The input cannot be empty.")
#         st.stop()

#     ok, err = validate_grammar_text(text)
#     if not ok:
#         st.error(f"Please enter correct grammar. {err}")
#         st.stop()

#     with open("grammar.txt", "w", encoding="utf-8") as f:
#         f.write(text)

#     if action == "Remove left recursion":
#         changed, outG, report = left_recursion.remove_left_recursion_if_any("grammar.txt")
#         st.subheader("Left Recursion Check")
#         lines = []
#         lines.append("Direct left recursion detected." if report.get("has_direct") else "No direct left recursion.")
#         lines.append("Indirect left recursion suspected (cycles present)." if report.get("has_indirect") else "No indirect left recursion.")
#         st.write("\n".join(lines))
#         if changed:
#             st.subheader("Grammar after removing left recursion")
#             for nt, prods in outG.items():
#                 st.write(f"{nt} -> {' | '.join(prods)}")
#         else:
#             st.info("No left recursion in the given grammar. Nothing to remove.")

#     elif action == "Remove left factoring":
#         grammar = left_factoring.read_grammar_from_file("grammar.txt")
#         factored = left_factoring.left_factoring(grammar)
#         st.subheader("Grammar after left factoring")
#         for nt, prods in factored.items():
#             st.write(f"{nt} -> {' | '.join(prods)}")

#     elif action == "Find First and Follow":
#         grammar_list, changed_lr, shown_text = first_follow.load_prepare_remove_lr_if_needed("grammar.txt")
#         st.subheader("Grammar used for FIRST/FOLLOW")
#         st.text(shown_text)
#         first = first_follow.compute_first(grammar_list)
#         follow = first_follow.compute_follow(grammar_list, first)
#         st.subheader("FIRST sets")
#         for nt in first:
#             shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(first[nt], key=lambda v: (v == "ε", v)))
#             st.write(f"First({nt}) = {{ {shown} }}")
#         st.subheader("FOLLOW sets")
#         for nt in follow:
#             shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(follow[nt], key=lambda v: (v == "ε", v)))
#             st.write(f"Follow({nt}) = {{ {shown} }}")

#     elif action == "LL(1) Table + Parse":  # NEW
#         # Build LL(1) artifacts
#         grammar_str, notes, first, follow, table, conflicts, terms = ll1.construct_ll1("grammar.txt")

#         st.subheader("Precondition checks")
#         for n in notes:
#             st.write(f"- {n}")

#         st.subheader("Grammar used")
#         for A, Ps in grammar_str.items():
#             st.write(f"{A} -> {' | '.join(Ps)}")

#         st.subheader("FIRST and FOLLOW")
#         for A, S in first.items():
#             shown = ", ".join(("∈" if x == "ε" else x) for x in sorted(S, key=lambda v: (v == "ε", v)))
#             st.write(f"First({A}) = {{ {shown} }}")
#         for A, S in follow.items():
#             shown = ", ".join(("∈" if x == "ε" else x) for x in sorted(S, key=lambda v: (v == "ε", v)))
#             st.write(f"Follow({A}) = {{ {shown} }}")

#         st.subheader("LL(1) Parsing Table")
#         # Pretty text table
#         st.text(ll1.pretty_table(table, terms))

#         if conflicts:
#             st.error("Conflicts detected (grammar is not LL(1)):")
#             for A, a, old, new in conflicts:
#                 st.write(f"M[{A}, {a}] conflict between [{old}] and [{new}]")
#         else:
#             st.success("No conflicts; grammar appears LL(1).")
#             # Input for string parsing
#             user_str = st.text_input("Enter input string to parse (without $)", key="parse_input")
#             if st.button("Parse"):
#                 if not user_str.strip():
#                     st.warning("Please enter a non-empty string.")
#                 else:
#                     accepted, steps = ll1.parse(table, grammar_str, terms, user_str.strip())
#                     st.subheader("Trace (Stack | Input | Action)")
#                     # Render as a table
#                     for stck, inp, act in steps:
#                         st.write(f"{stck:<25} | {inp:<25} | {act}")
#                     st.write(f"\nResult: {'ACCEPTED' if accepted else 'REJECTED'}")

# st.caption("Develop by Dharmik...")


#------------------------------------------------------

















# # app.py
# # -*- coding: utf-8 -*-
# import streamlit as st
# import left_recursion
# import left_factoring
# import first_follow
# import ll1  # make sure ll1.py is in the same folder

# # -------------------- Validation --------------------

# def validate_grammar_text(text: str):
#     """
#     Basic format checks:
#     <NT> -> prod1 | prod2 | ...
#     - exactly one '->' per non-empty line
#     - LHS non-empty, no spaces
#     - RHS non-empty; use 'ε' for empty
#     """
#     lines = [ln.rstrip() for ln in text.splitlines()]
#     for idx, line in enumerate(lines, start=1):
#         if not line.strip():
#             continue
#         if line.count("->") != 1:
#             return False, f"Line {idx}: each rule must contain exactly one '->'."
#         lhs, rhs = line.split("->", 1)
#         lhs = lhs.strip()
#         rhs = rhs.strip()
#         if not lhs:
#             return False, f"Line {idx}: left-hand side (nonterminal) is empty."
#         if " " in lhs:
#             return False, f"Line {idx}: nonterminal '{lhs}' must not contain spaces."
#         if not rhs:
#             return False, f"Line {idx}: right-hand side is empty."
#         parts = [p.strip() for p in rhs.split("|")]
#         if any(p == "" for p in parts):
#             return False, f"Line {idx}: empty production found; use 'ε' for empty."
#     return True, ""

# # -------------------- Page --------------------

# st.set_page_config(page_title="Grammar Toolkit", page_icon="🧩", layout="centered")
# st.title("Grammar Toolkit")

# st.write("Enter grammar rules (one per line). Use ε for epsilon and -> for productions.")

# st.code("""Example:
# S -> iEtS | iEtSeS | a
# E -> b | ε
# """, language="text")

# st.caption("Quick copy symbols (use the copy buttons on the right):")
# c1, c2 = st.columns(2)
# with c1:
#     st.code("ε", language="text")
# with c2:
#     st.code(" -> ", language="text")

# # Persist input text
# if "grammar_text" not in st.session_state:
#     st.session_state.grammar_text = ""

# st.session_state.grammar_text = st.text_area(
#     "Grammar", value=st.session_state.grammar_text, height=220,
#     placeholder="A -> aA | b\nB -> c | ε"
# )

# # Persist selected action
# action = st.selectbox(
#     "Select an operation",
#     ["Remove left recursion", "Remove left factoring", "Find First and Follow", "LL(1) Table + Parse"],
#     index=0,
#     key="action"
# )

# # -------------------- Run Button --------------------

# if st.button("Run", key="run_btn"):
#     text = st.session_state.grammar_text if "grammar_text" in st.session_state else ""
#     if not text or not text.strip():
#         st.error("Please enter correct grammar. The input cannot be empty.")
#         st.stop()

#     ok, err = validate_grammar_text(text)
#     if not ok:
#         st.error(f"Please enter correct grammar. {err}")
#         st.stop()

#     # Save grammar persistently for modules
#     with open("grammar.txt", "w", encoding="utf-8") as f:
#         f.write(text)

#     # Clear stale LL(1) cache on new Run
#     st.session_state.pop("ll1", None)

#     if action == "Remove left recursion":
#         changed, outG, report = left_recursion.remove_left_recursion_if_any("grammar.txt")

#         st.subheader("Left Recursion Check")
#         msgs = []
#         msgs.append("Direct left recursion detected." if report.get("has_direct") else "No direct left recursion.")
#         msgs.append("Indirect left recursion suspected (cycles present)." if report.get("has_indirect") else "No indirect left recursion.")
#         st.write("\n".join(msgs))

#         if changed:
#             st.subheader("Grammar after removing left recursion")
#             for nt, prods in outG.items():
#                 st.write(f"{nt} -> {' | '.join(prods)}")
#         else:
#             st.info("No left recursion in the given grammar. Nothing to remove.")

#     elif action == "Remove left factoring":
#         grammar = left_factoring.read_grammar_from_file("grammar.txt")
#         factored = left_factoring.left_factoring(grammar)
#         st.subheader("Grammar after left factoring")
#         for nt, prods in factored.items():
#             st.write(f"{nt} -> {' | '.join(prods)}")

#     elif action == "Find First and Follow":
#         grammar_list, changed_lr, shown_text = first_follow.load_prepare_remove_lr_if_needed("grammar.txt")

#         st.subheader("Grammar used for FIRST/FOLLOW")
#         st.text(shown_text)

#         first = first_follow.compute_first(grammar_list)
#         follow = first_follow.compute_follow(grammar_list, first)

#         st.subheader("FIRST sets")
#         for nt in first:
#             shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(first[nt], key=lambda v: (v == "ε", v)))
#             st.write(f"First({nt}) = {{ {shown} }}")

#         st.subheader("FOLLOW sets")
#         for nt in follow:
#             shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(follow[nt], key=lambda v: (v == "ε", v)))
#             st.write(f"Follow({nt}) = {{ {shown} }}")

#     elif action == "LL(1) Table + Parse":
#         # Build and cache LL(1) data
#         G, notes, first, follow, table, conflicts, terms = ll1.construct_ll1("grammar.txt")
#         st.session_state.ll1 = {
#             "grammar_str": G,
#             "notes": notes,
#             "first": first,
#             "follow": follow,
#             "table": table,
#             "conflicts": conflicts,
#             "terms": terms,
#         }

# # -------------------- LL(1) Section (stable across reruns) --------------------

# if st.session_state.get("action") == "LL(1) Table + Parse":
#     state = st.session_state.get("ll1")
#     if state:
#         G = state["grammar_str"]
#         notes = state["notes"]
#         first = state["first"]
#         follow = state["follow"]
#         table = state["table"]
#         conflicts = state["conflicts"]
#         terms = state["terms"]

#         st.subheader("Precondition checks")
#         for n in notes:
#             st.write(f"- {n}")

#         st.subheader("Grammar used")
#         for A, Ps in G.items():
#             st.write(f"{A} -> {' | '.join(Ps)}")

#         st.subheader("FIRST and FOLLOW")
#         for A, S in first.items():
#             shown = ", ".join(("∈" if x == "ε" else x) for x in sorted(S, key=lambda v: (v == "ε", v)))
#             st.write(f"First({A}) = {{ {shown} }}")
#         for A, S in follow.items():
#             shown = ", ".join(("∈" if x == "ε" else x) for x in sorted(S, key=lambda v: (v == "ε", v)))
#             st.write(f"Follow({A}) = {{ {shown} }}")

#         # st.subheader("LL(1) Parsing Table")
#         # st.text(ll1.pretty_table(table, terms))

#         st.subheader("LL(1) Parsing Table")
#         headers, rows = ll1.ll1_table_as_rows(table, terms)
#         import pandas as pd
#         df = pd.DataFrame(rows, columns=headers)
#         st.table(df) # or st.dataframe(df, use_container_width=True)


#         if conflicts:
#             st.error("Conflicts detected (grammar is not LL(1)). Parsing is disabled.")
#             for A, a, old, new in conflicts:
#                 st.write(f"M[{A}, {a}] conflict between [{old}] and [{new}]")
#         else:
#             st.success("No conflicts; grammar appears LL(1).")
#             parse_str = st.text_input("Enter input string to parse (without $)", key="parse_input")
#             if st.button("Parse", key="parse_btn"):
#                 if not parse_str.strip():
#                     st.warning("Please enter a non-empty string.")
#                 else:
#                     accepted, steps = ll1.parse(table, G, terms, parse_str.strip())
#                     st.subheader("Trace (Stack | Input | Action)")
#                     # Display each step; align monospaced by wrapping in code
#                     for stck, inp, act in steps:
#                         st.code(f"{stck:<25} | {inp:<25} | {act}", language="text")
#                     st.write(f"\nResult: {'ACCEPTED' if accepted else 'REJECTED'}")

# st.caption("Develop by Dharmik...")





















# app.py
# -*- coding: utf-8 -*-
import streamlit as st
import left_recursion
import left_factoring
import first_follow
import ll1  # LL(1) features
import lr0_slr1 as lr  # LR(0)/SLR(1) features
import clr_lalr as clr  # NEW: CLR/LALR(1) features
import pandas as pd
import graphviz


# -------------------- Validation --------------------
def validate_grammar_text(text: str):
    lines = [ln.rstrip() for ln in text.splitlines()]
    for idx, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        if line.count("->") != 1:
            return False, f"Line {idx}: each rule must contain exactly one '->'."
        lhs, rhs = line.split("->", 1)
        lhs = lhs.strip()
        rhs = rhs.strip()
        if not lhs:
            return False, f"Line {idx}: left-hand side (nonterminal) is empty."
        if " " in lhs:
            return False, f"Line {idx}: nonterminal '{lhs}' must not contain spaces."
        if not rhs:
            return False, f"Line {idx}: right-hand side is empty."
        parts = [p.strip() for p in rhs.split("|")]
        if any(p == "" for p in parts):
            return False, f"Line {idx}: empty production found; use 'ε' for empty."
    return True, ""

# -------------------- Page --------------------
st.set_page_config(page_title="Grammar Toolkit", page_icon="🧩", layout="centered")
st.title("Grammar Toolkit")

st.write("Enter grammar rules (one per line). Use ε for epsilon and -> for productions.")

st.code("""Example:
S -> iEtS | iEtSeS | a
E -> b | ε
""", language="text")

st.caption("Quick copy symbols (use the copy buttons on the right):")
c1, c2 = st.columns(2)
with c1:
    st.code("ε", language="text")
with c2:
    st.code(" -> ", language="text")

# Persist input text
if "grammar_text" not in st.session_state:
    st.session_state.grammar_text = ""

st.session_state.grammar_text = st.text_area(
    "Grammar", value=st.session_state.grammar_text, height=220,
    placeholder="A -> aA | b\nB -> c | ε"
)

# Persist selected action
action = st.selectbox(
    "Select an operation",
    [
        "Remove left recursion",
        "Remove left factoring",
        "Find First and Follow",
        "LL(1) Table + Parse",
        "LR(0)/SLR(1) + Parse",
        "CLR/LALR(1) + Parse",  # NEW
    ],

    index=0,
    key="action"
)

# -------------------- Run Button --------------------
if st.button("Run", key="run_btn"):
    text = st.session_state.grammar_text if "grammar_text" in st.session_state else ""
    if not text or not text.strip():
        st.error("Please enter correct grammar. The input cannot be empty.")
        st.stop()

    ok, err = validate_grammar_text(text)
    if not ok:
        st.error(f"Please enter correct grammar. {err}")
        st.stop()

    # Save grammar persistently for modules
    with open("grammar.txt", "w", encoding="utf-8") as f:
        f.write(text)

    # Clear caches on new run
    st.session_state.pop("ll1", None)
    st.session_state.pop("lr", None)

    if action == "Remove left recursion":
        changed, outG, report = left_recursion.remove_left_recursion_if_any("grammar.txt")

        st.subheader("Left Recursion Check")
        msgs = []
        msgs.append("Direct left recursion detected." if report.get("has_direct") else "No direct left recursion.")
        msgs.append("Indirect left recursion suspected (cycles present)." if report.get("has_indirect") else "No indirect left recursion.")
        st.write("\n".join(msgs))

        if changed:
            st.subheader("Grammar after removing left recursion")
            for nt, prods in outG.items():
                st.write(f"{nt} -> {' | '.join(prods)}")
        else:
            st.info("No left recursion in the given grammar. Nothing to remove.")

    elif action == "Remove left factoring":
        grammar = left_factoring.read_grammar_from_file("grammar.txt")
        factored = left_factoring.left_factoring(grammar)
        st.subheader("Grammar after left factoring")
        for nt, prods in factored.items():
            st.write(f"{nt} -> {' | '.join(prods)}")

    elif action == "Find First and Follow":
        grammar_list, changed_lr, shown_text = first_follow.load_prepare_remove_lr_if_needed("grammar.txt")

        st.subheader("Grammar used for FIRST/FOLLOW")
        st.text(shown_text)

        first = first_follow.compute_first(grammar_list)
        follow = first_follow.compute_follow(grammar_list, first)

        st.subheader("FIRST sets")
        for nt in first:
            shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(first[nt], key=lambda v: (v == "ε", v)))
            st.write(f"First({nt}) = {{ {shown} }}")

        st.subheader("FOLLOW sets")
        for nt in follow:
            shown = ", ".join(("∈" if s == "ε" else s) for s in sorted(follow[nt], key=lambda v: (v == "ε", v)))
            st.write(f"Follow({nt}) = {{ {shown} }}")

    elif action == "LL(1) Table + Parse":
        # Build and cache LL(1) data
        G, notes, first, follow, table, conflicts, terms = ll1.construct_ll1("grammar.txt")
        st.session_state.ll1 = {
            "grammar_str": G,
            "notes": notes,
            "first": first,
            "follow": follow,
            "table": table,
            "conflicts": conflicts,
            "terms": terms,
        }

    elif action == "LR(0)/SLR(1) + Parse":
        # Build canonical sets
        Gaug, Glst, S_dash, S, states, trans = lr.build_lr0("grammar.txt")
        nt_index, prod_index = lr.build_order_indices(Gaug)

        # Build tables
        ACTION0, GOTO0, terms0, nts0, lr0_conflicts = lr.build_lr0_table(Glst, S_dash, states, trans)
        ACTION1, GOTO1, terms1, nts1, slr_conflicts, follow = lr.build_slr1_table(Glst, S_dash, states, trans)

        # Cache everything
        st.session_state.lr = {
            "Gaug": Gaug, "Glst": Glst, "S_dash": S_dash, "S": S,
            "states": states, "trans": trans, "nt_index": nt_index, "prod_index": prod_index,
            "ACTION0": ACTION0, "GOTO0": GOTO0, "terms0": terms0, "nts0": nts0, "lr0_conflicts": lr0_conflicts,
            "ACTION1": ACTION1, "GOTO1": GOTO1, "terms1": terms1, "nts1": nts1, "slr_conflicts": slr_conflicts,
            "follow": follow,
        }

        # st.subheader("LR(0) Automaton Diagram")
        # diagram = lr.render_lr_automaton(
        #     S["states"],
        #     S["trans"],
        #     lambda idx, state: lr.state_to_str(idx, state, S["nt_index"], S["prod_index"])
        # )
        # st.graphviz_chart(diagram)
        S = st.session_state.get("lr")
        if not isinstance(S, dict):
            st.warning("LR(0)/SLR(1) structures have not been built yet. Run the analysis first.")
        else:
            st.subheader("LR(0) Automaton Diagram")
            diagram = lr.render_lr_automaton(
                S["states"],
                S["trans"],
                lambda idx, state: lr.state_to_str(idx, state, S["nt_index"], S["prod_index"])
            )
        st.graphviz_chart(diagram)
        
    elif action == "CLR/LALR(1) + Parse":
        # Build CLR/LALR artifacts
        Gstr = clr.read_strings("grammar.txt")
        Gaug, S_dash, S0 = clr.augment_grammar(Gstr)
        Glst = clr.to_symbol_lists(Gaug)

        # CLR canonical collection
        first = clr.compute_first(Glst)
        clr_states, clr_trans = clr.canonical_lr1(Glst, S_dash, first)

        # Production numbering
        prod_num, prod_list = clr.number_productions(Gaug, Glst)

        # CLR table
        ACTION_CLR, GOTO_CLR, terms, nts, clr_conf = clr.build_lr1_table(
            Glst, S_dash, clr_states, clr_trans, prod_num
        )

        # Merge CLR -> LALR
        (lalr_states, lalr_trans,
        clr_to_merged_idx, merged_idx_to_label,
        sequence_labels, merged_flag) = clr.merge_clr_with_labels(clr_states, clr_trans)

        # LALR labeled table rows
        ACTION_LALR, GOTO_LALR, terms2, nts2, lalr_conf, headers, rows = clr.build_lalr_table_labeled(
            Glst, S_dash, lalr_states, lalr_trans, merged_idx_to_label, prod_num
        )

        # Store everything in session state for later use (e.g., UI traces, diagrams)
        st.session_state.clr = {
            "Gaug": Gaug, "Glst": Glst, "S_dash": S_dash, "S": S0,
            "first": first,
            "clr_states": clr_states, "clr_trans": clr_trans,
            "ACTION_CLR": ACTION_CLR, "GOTO_CLR": GOTO_CLR, "terms": terms, "nts": nts, "clr_conf": clr_conf,
            "prod_num": prod_num, "prod_list": prod_list,
            "lalr_states": lalr_states, "lalr_trans": lalr_trans,
            "merged_idx_to_label": merged_idx_to_label, "sequence_labels": sequence_labels, "merged_flag": merged_flag,
            "ACTION_LALR": ACTION_LALR, "GOTO_LALR": GOTO_LALR, "terms2": terms2, "nts2": nts2,
            "lalr_conf": lalr_conf, "headers": headers, "rows": rows,
            # Optionally pre-render diagrams for CLR/LALR:
            # (call this only if you have the LR automaton diagram function shared)
            "diagram_clr": clr.render_lr_automaton(
                clr_states, clr_trans, clr.state_lr1_str_merged_lookaheads
            ),
            "diagram_lalr": clr.render_lr_automaton(
                lalr_states, lalr_trans,
                lambda idx, state: clr.state_str_with_label(merged_idx_to_label[idx], state)
            )
    }

    # elif action == "CLR/LALR(1) + Parse":
    #     # Build CLR/LALR artifacts
    #     Gstr = clr.read_strings("grammar.txt")
    #     Gaug, S_dash, S = clr.augment_grammar(Gstr)
    #     Glst = clr.to_symbol_lists(Gaug)

    #     # CLR canonical collection
    #     first = clr.compute_first(Glst)
    #     clr_states, clr_trans = clr.canonical_lr1(Glst, S_dash, first)

    #     # Production numbering
    #     prod_num, prod_list = clr.number_productions(Gaug, Glst)

    #     # CLR table
    #     ACTION_CLR, GOTO_CLR, terms, nts, clr_conf = clr.build_lr1_table(Glst, S_dash, clr_states, clr_trans, prod_num)

    #     # Merge CLR -> LALR
    #     (lalr_states, lalr_trans,
    #      clr_to_merged_idx, merged_idx_to_label,
    #      sequence_labels, merged_flag) = clr.merge_clr_with_labels(clr_states, clr_trans)

    #     # LALR labeled table rows
    #     ACTION_LALR, GOTO_LALR, terms2, nts2, lalr_conf, headers, rows = clr.build_lalr_table_labeled(
    #         Glst, S_dash, lalr_states, lalr_trans, merged_idx_to_label, prod_num
    #     )

    #     # Cache everything
    #     st.session_state.clr = {
    #         "Gaug": Gaug, "Glst": Glst, "S_dash": S_dash, "S": S,
    #         "first": first,
    #         "clr_states": clr_states, "clr_trans": clr_trans,
    #         "ACTION_CLR": ACTION_CLR, "GOTO_CLR": GOTO_CLR, "terms": terms, "nts": nts, "clr_conf": clr_conf,
    #         "prod_num": prod_num, "prod_list": prod_list,
    #         "lalr_states": lalr_states, "lalr_trans": lalr_trans,
    #         "merged_idx_to_label": merged_idx_to_label, "sequence_labels": sequence_labels, "merged_flag": merged_flag,
    #         "ACTION_LALR": ACTION_LALR, "GOTO_LALR": GOTO_LALR, "terms2": terms2, "nts2": nts2,
    #         "lalr_conf": lalr_conf, "headers": headers, "rows": rows,
    #     }


# -------------------- LL(1) Section (stable across reruns) --------------------
if st.session_state.get("action") == "LL(1) Table + Parse":
    state = st.session_state.get("ll1")
    if state:
        G = state["grammar_str"]
        notes = state["notes"]
        first = state["first"]
        follow = state["follow"]
        table = state["table"]
        conflicts = state["conflicts"]
        terms = state["terms"]

        st.subheader("Precondition checks")
        for n in notes:
            st.write(f"- {n}")

        st.subheader("Grammar used")
        for A, Ps in G.items():
            st.write(f"{A} -> {' | '.join(Ps)}")

        st.subheader("FIRST and FOLLOW")
        for A, Sset in first.items():
            shown = ", ".join(("∈" if x == "ε" else x) for x in sorted(Sset, key=lambda v: (v == "ε", v)))
            st.write(f"First({A}) = {{ {shown} }}")
        for A, Sset in follow.items():
            shown = ", ".join(("∈" if x == "ε" else x) for x in sorted(Sset, key=lambda v: (v == "ε", v)))
            st.write(f"Follow({A}) = {{ {shown} }}")

        st.subheader("LL(1) Parsing Table")
        headers, rows = ll1.ll1_table_as_rows(table, terms)
        df = pd.DataFrame(rows, columns=headers)
        st.table(df)

        if conflicts:
            st.error("Conflicts detected (grammar is not LL(1)). Parsing is disabled.")
            for A, a, old, new in conflicts:
                st.write(f"M[{A}, {a}] conflict between [{old}] and [{new}]")
        else:
            st.success("No conflicts; grammar appears LL(1).")
            parse_str = st.text_input("Enter input string to parse (without $)", key="parse_input_ll1")
            if st.button("Parse", key="parse_btn_ll1"):
                if not parse_str.strip():
                    st.warning("Please enter a non-empty string.")
                else:
                    accepted, steps = ll1.parse(table, G, terms, parse_str.strip())
                    st.subheader("Trace (Stack | Input | Action)")
                    for stck, inp, act in steps:
                        st.code(f"{stck:<25} | {inp:<25} | {act}", language="text")
                    st.write(f"\nResult: {'ACCEPTED' if accepted else 'REJECTED'}")

# -------------------- LR(0)/SLR(1) Section (stable across reruns) --------------------
if st.session_state.get("action") == "LR(0)/SLR(1) + Parse":
    S = st.session_state.get("lr")
    if S:
        Gaug = S["Gaug"]; Glst = S["Glst"]; S_dash = S["S_dash"]; states = S["states"]; trans = S["trans"]
        nt_index = S["nt_index"]; prod_index = S["prod_index"]
        ACTION0 = S["ACTION0"]; GOTO0 = S["GOTO0"]; terms0 = S["terms0"]; nts0 = S["nts0"]; lr0_conflicts = S["lr0_conflicts"]
        ACTION1 = S["ACTION1"]; GOTO1 = S["GOTO1"]; terms1 = S["terms1"]; nts1 = S["nts1"]; slr_conflicts = S["slr_conflicts"]
        follow = S["follow"]

        st.subheader("Augmented grammar")
        for A, prods in Gaug.items():
            st.write(f"{A} -> {' | '.join(prods)}")

        st.subheader("Canonical LR(0) item sets")
        for i, I in enumerate(states):
            st.text(lr.state_to_str(i, I, nt_index, prod_index))

        st.subheader("GOTO transitions")
        st.text(lr.transitions_to_str(trans))

        # LR(0) Table
        st.subheader("LR(0) Parsing Table")
        # Convert to DataFrame
        action_cols0 = terms0 + ["$"]
        goto_cols0 = [A for A in nts0 if A != nts0[0]]
        rows0 = []
        for i in range(len(ACTION0)):
            rows0.append(
                [f"I{i}"] +
                [ACTION0[i].get(a, "") for a in action_cols0] +
                [GOTO0[i].get(A, "") for A in goto_cols0]
            )
        # Build rows with string values only
        action_cols0 = terms0 + ["$"]
        goto_cols0 = [A for A in nts0 if A != nts0[0]]
        rows0 = []
        for i in range(len(ACTION0)):
            row = [f"I{i}"]
            row += [str(ACTION0[i].get(a, "")) for a in action_cols0]
            row += [str(GOTO0[i].get(A, "")) for A in goto_cols0]
            rows0.append(row)
        cols0 = ["State"] + action_cols0 + goto_cols0
        df0 = pd.DataFrame(rows0, columns=cols0, dtype="string")
        st.table(df0)

        # df0 = pd.DataFrame(rows0, columns=["State"] + action_cols0 + goto_cols0)
        # st.table(df0)
        if lr0_conflicts:
            st.error("LR(0) conflicts present; entries may show shift/reduce or reduce/reduce collisions.")
            for i, sym, old, new in lr0_conflicts:
                st.write(f"I{i}, on '{sym}': {old} vs {new}")
        else:
            st.success("No conflicts in LR(0) table.")

        # SLR(1) Table
        st.subheader("SLR(1) Parsing Table")
        action_cols1 = terms1 + ["$"]
        goto_cols1 = [A for A in nts1 if A != nts1[0]]
        rows1 = []
        for i in range(len(ACTION1)):
            rows1.append(
                [f"I{i}"] +
                [ACTION1[i].get(a, "") for a in action_cols1] +
                [GOTO1[i].get(A, "") for A in goto_cols1]
            )
        action_cols1 = terms1 + ["$"]
        goto_cols1 = [A for A in nts1 if A != nts1[0]]
        rows1 = []
        for i in range(len(ACTION1)):
            row = [f"I{i}"]
            row += [str(ACTION1[i].get(a, "")) for a in action_cols1]
            row += [str(SLR_GOTO := GOTO1[i].get(A, "")) for A in goto_cols1]
            rows1.append(row)
        cols1 = ["State"] + action_cols1 + goto_cols1
        df1 = pd.DataFrame(rows1, columns=cols1, dtype="string")
        st.table(df1)

        # df1 = pd.DataFrame(rows1, columns=["State"] + action_cols1 + goto_cols1)
        # st.table(df1)
        if slr_conflicts:
            st.error("SLR(1) conflicts present; entries may show shift/reduce or reduce/reduce collisions.")
            for i, sym, old, new in slr_conflicts:
                st.write(f"I{i}, on '{sym}': {old} vs {new}")
        else:
            st.success("No conflicts in SLR(1) table.")

        # FOLLOW sets (for SLR)
        st.subheader("FOLLOW sets (SLR)")
        for A, Sset in follow.items():
            st.write(f"Follow({A}) = {{ {', '.join(sorted(Sset))} }}")

        # Enable parsing if at least one table is conflict-free
        lr0_ok = len(lr0_conflicts) == 0
        slr_ok = len(slr_conflicts) == 0

        if not lr0_ok and not slr_ok:
            st.warning("Both LR(0) and SLR(1) tables have conflicts. Parsing is disabled.")
        else:
            parse_str2 = st.text_input("Enter input string to parse (without $)", key="parse_input_lr")
            if st.button("Parse with LR tables", key="parse_btn_lr"):
                if not parse_str2.strip():
                    st.warning("Please enter a non-empty string.")
                else:
                    if lr0_ok:
                        st.subheader("LR(0) parse trace")
                        trace0 = lr.lr0_parse(parse_str2.strip(), ACTION0, GOTO0, terms0, nts0, states, Glst, S_dash)
                        st.code(f"{'STATE STACK':<24} | {'INPUT':<18} | ACTION", language="text")
                        for stck, inp, act in trace0:
                            st.code(f"{stck:<24} | {inp:<18} | {act}", language="text")
                    else:
                        st.info("Skipping LR(0) parse due to conflicts.")

                    if slr_ok:
                        st.subheader("SLR(1) parse trace")
                        trace1 = lr.lr0_parse(parse_str2.strip(), ACTION1, GOTO1, terms1, nts1, states, Glst, S_dash)
                        st.code(f"{'STATE STACK':<24} | {'INPUT':<18} | ACTION", language="text")
                        for stck, inp, act in trace1:
                            st.code(f"{stck:<24} | {inp:<18} | {act}", language="text")
                    else:
                        st.info("Skipping SLR(1) parse due to conflicts.")




# -------------------- CLR/LALR(1) Section (stable across reruns) --------------------
if st.session_state.get("action") == "CLR/LALR(1) + Parse":
    S = st.session_state.get("clr")
    if S:
        Gaug = S["Gaug"]; Glst = S["Glst"]; S_dash = S["S_dash"]
        first = S["first"]
        clr_states = S["clr_states"]; clr_trans = S["clr_trans"]
        ACTION_CLR = S["ACTION_CLR"]; GOTO_CLR = S["GOTO_CLR"]; terms = S["terms"]; nts = S["nts"]; clr_conf = S["clr_conf"]
        prod_list = S["prod_list"]
        lalr_states = S["lalr_states"]; lalr_trans = S["lalr_trans"]
        merged_idx_to_label = S["merged_idx_to_label"]; sequence_labels = S["sequence_labels"]; merged_flag = S["merged_flag"]
        ACTION_LALR = S["ACTION_LALR"]; GOTO_LALR = S["GOTO_LALR"]; terms2 = S["terms2"]; nts2 = S["nts2"]; lalr_conf = S["lalr_conf"]
        headers = S["headers"]; rows = S["rows"]

        st.subheader("Augmented grammar")
        for A, Ps in Gaug.items():
            st.write(f"{A} -> {' | '.join(Ps)}")

        #--------------------------
        st.subheader("CLR(1) Automaton Diagram")
        clr_diagram = clr.render_lr_automaton(
            S["clr_states"], S["clr_trans"],
            clr.state_lr1_str_merged_lookaheads
        )
        st.graphviz_chart(clr_diagram)

        st.subheader("LALR(1) Automaton Diagram")
        lalr_diagram = clr.render_lr_automaton(
            S["lalr_states"], S["lalr_trans"],
            lambda idx, state: clr.state_str_with_label(S["merged_idx_to_label"][idx], state)
        )
        st.graphviz_chart(lalr_diagram)
        #--------------------------

        st.subheader("CLR item sets (merged lookaheads)")
        for i, I in enumerate(clr_states):
            st.text(clr.state_lr1_str_merged_lookaheads(i, I))

        st.subheader("GOTO transitions (CLR)")
        st.text(clr.transitions_to_str(clr_trans))

        st.subheader("CLR Parsing Table")
        cols = ["State"] + (terms + ["$"]) + [A for A in nts if A != nts[0]]
        rows_clr = []
        for i in range(len(ACTION_CLR)):
            rows_clr.append(
                [f"I{i}"] +
                [str(ACTION_CLR[i].get(a, "")) for a in (terms + ["$"])] +
                [str(GOTO_CLR[i].get(A, "")) for A in [A for A in nts if A != nts[0]]]
            )
        df_clr = pd.DataFrame(rows_clr, columns=cols, dtype="string")
        st.table(df_clr)
        if clr_conf:
            st.error("CLR conflicts present; entries may show shift/reduce or reduce/reduce collisions.")
            for i, sym, old, new in clr_conf:
                st.write(f"I{i}, on '{sym}': {old} vs {new}")
        else:
            st.success("No conflicts in CLR table.")

        st.subheader("CLR indices mapped to LALR labels")
        st.text(", ".join(f"I{lab}" for lab in sequence_labels))

        if not merged_flag:
            st.info("No sets to merge; LALR equals CLR.")
        else:
            st.subheader("LALR merged item sets")
            for mi in range(len(lalr_states)):
                lab = merged_idx_to_label[mi]
                st.text(clr.state_str_with_label(lab, lalr_states[mi]))
            st.text(clr.transitions_str_labeled(lalr_trans, merged_idx_to_label))

        st.subheader("LALR(1) Parsing Table (labeled rows)")
        df_lalr = pd.DataFrame(rows, columns=headers, dtype="string")
        st.table(df_lalr)
        if lalr_conf:
            st.error("LALR conflicts present; entries may show shift/reduce or reduce/reduce collisions.")
            for i, sym, old, new in lalr_conf:
                st.write(f"I{merged_idx_to_label[i]}, on '{sym}': {old} vs {new}")
        else:
            st.success("No conflicts in LALR table.")

        # Enable parsing if at least one table is conflict-free
        clr_ok = len(clr_conf) == 0
        lalr_ok = len(lalr_conf) == 0

        if not clr_ok and not lalr_ok:
            st.warning("Both CLR and LALR tables have conflicts. Parsing is disabled.")
        else:
            parse_str3 = st.text_input("Enter input string to parse (without $)", key="parse_input_clr")
            if st.button("Parse with CLR/LALR tables", key="parse_btn_clr"):
                if not parse_str3.strip():
                    st.warning("Please enter a non-empty string.")
                else:
                    if clr_ok:
                        st.subheader("CLR parse trace")
                        tr = clr.parse_with_rnums(parse_str3.strip(), ACTION_CLR, GOTO_CLR, prod_list)
                        st.code(f"{'STATE STACK':<24} | {'INPUT':<18} | ACTION", language="text")
                        for stck, inp, act in tr:
                            st.code(f"{stck:<24} | {inp:<18} | {act}", language="text")
                    else:
                        st.info("Skipping CLR parse due to conflicts.")

                    if lalr_ok:
                        st.subheader("LALR(1) parse trace")
                        tr = clr.parse_with_rnums(parse_str3.strip(), ACTION_LALR, GOTO_LALR, prod_list)
                        st.code(f"{'STATE STACK':<24} | {'INPUT':<18} | ACTION", language="text")
                        for stck, inp, act in tr:
                            st.code(f"{stck:<24} | {inp:<18} | {act}", language="text")
                    else:
                        st.info("Skipping LALR(1) parse due to conflicts.")





st.caption("Develop by Dharmik...")
