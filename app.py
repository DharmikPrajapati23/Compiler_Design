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




















import streamlit as st
import first_follow
import left_recursion

st.title("Grammar Analysis with Left Recursion Removal")

st.write("Enter grammar rules (one per line), e.g.:")
st.code("""S -> aBDh
B -> cC
C -> bC | ε
D -> EF
E -> g | ε
F -> f | ε
""", language='text')

grammar_input = st.text_area("Enter your grammar here", height=250)

if st.button("Process Grammar"):
    if not grammar_input.strip():
        st.warning("Please enter your grammar first.")
    else:
        # Save input grammar to file with UTF-8 encoding
        with open("grammar.txt", "w", encoding="utf-8") as f:
            f.write(grammar_input)

        # Read and convert for left recursion removal
        grammar = first_follow.read_grammar_from_file("grammar.txt")
        grammar_str = {nt: [''.join(prod) for prod in prods] for nt, prods in grammar.items()}

        # Remove left recursion
        grammar_no_lr = left_recursion.remove_left_recursion(grammar_str)

        # Display grammar after removing left recursion
        st.subheader("Grammar After Removing Left Recursion:")
        for nt, prods in grammar_no_lr.items():
            st.write(f"{nt} -> {' | '.join(prods)}")

        # Convert back for first/follow calculation
        grammar_processed = {}
        for nt, prods in grammar_no_lr.items():
            grammar_processed[nt] = [list(prod) if prod != 'ε' else ['ε'] for prod in prods]

        # Compute first and follow
        first = first_follow.compute_first(grammar_processed)
        follow = first_follow.compute_follow(grammar_processed, first)

        # Display First sets
        st.subheader("FIRST sets:")
        for nt in first:
            first_set = ', '.join('∈' if s == 'ε' else s for s in sorted(first[nt]))
            st.write(f"First({nt}) = {{ {first_set} }}")

        # Display Follow sets
        st.subheader("FOLLOW sets:")
        for nt in follow:
            follow_set = ', '.join('∈' if s == 'ε' else s for s in sorted(follow[nt]))
            st.write(f"Follow({nt}) = {{ {follow_set} }}")
