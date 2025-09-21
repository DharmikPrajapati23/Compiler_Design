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

















# -*- coding: utf-8 -*-
import streamlit as st
import left_recursion
import left_factoring
import first_follow





def validate_grammar_text(text: str):
    """
    Returns (ok: bool, error_msg: str). Checks minimal CFG line format:
    <NT> -> prod1 | prod2 | ...
    - requires '->' exactly once per non-empty line
    - LHS non-empty, no spaces
    - each RHS production non-empty after strip, or equals 'ε'
    """
    lines = [ln.rstrip() for ln in text.splitlines()]
    for idx, line in enumerate(lines, start=1):
        if not line.strip():
            # allow blank lines; skip
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
        # allow ε explicitly; other tokens are free-form here
    return True, ""




st.set_page_config(page_title="Grammar Toolkit", page_icon="🧩", layout="centered")
st.title("Grammar Toolkit")


# st.caption("Quick copy symbols (select and copy):")
# c1, c2 = st.columns(2)
# with c1:
#     st.text_input("Epsilon (copy)", value="ε", key="copy_eps", disabled=True, label_visibility="collapsed")
# with c2:
#     st.text_input("Arrow (copy)", value=" -> ", key="copy_arrow", disabled=True, label_visibility="collapsed")







st.code("""Example:
S -> iEtS | iEtSeS | a
E -> b | ε
""", language="text")


st.write("Enter grammar rules (one per line). Use ε for epsilon and -> for productions.")

# Clipboard copy buttons (ε and ->)
st.caption("Quick copy symbols:")
col1, col2 = st.columns(2)
with col1:
    st.code("ε", language="text")  # has a native copy button
with col2:
    st.code(" -> ", language="text")


if "grammar_text" not in st.session_state:
    st.session_state.grammar_text = ""

st.session_state.grammar_text = st.text_area(
    "Grammar", value=st.session_state.grammar_text, height=220, placeholder="A -> aA | b\nB -> c | ε"
)

action = st.selectbox(
    "Select an operation",
    ["Remove left recursion", "Remove left factoring", "Find First and Follow"],
    index=0,
)

# if st.button("Run"):
    # text = st.session_state.grammar_text
    # if not text.strip():
    #     st.warning("Please enter your grammar first.")
    #     st.stop()
if st.button("Run"):
    text = st.session_state.grammar_text if "grammar_text" in st.session_state else ""
    if not text or not text.strip():
        st.error("Please enter correct grammar. The input cannot be empty.")
        st.stop()

    ok, err = validate_grammar_text(text)  # your validator from earlier
    if not ok:
        st.error(f"Please enter correct grammar. {err}")
        st.stop()

    # Persist grammar to file (UTF-8 to preserve ε)
    with open("grammar.txt", "w", encoding="utf-8") as f:
        f.write(text)

    if action == "Remove left recursion":
        # Uses your integrated detector + remover
        changed, outG, report = left_recursion.remove_left_recursion_if_any("grammar.txt")

        st.subheader("Left Recursion Check")
        lines = []
        lines.append("Direct left recursion detected." if report.get("has_direct") else "No direct left recursion.")
        lines.append("Indirect left recursion suspected (cycles present)." if report.get("has_indirect") else "No indirect left recursion.")
        st.write("\n".join(lines))

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
        # Use first_follow orchestration which removes LR if present
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


st.caption("Develop by Dharmik...")