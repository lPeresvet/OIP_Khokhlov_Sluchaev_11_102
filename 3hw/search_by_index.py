import json

output_file = "../out/inverted_index.json"

with open(output_file, 'r', encoding='utf-8') as infile:
    loaded_index = json.load(infile)

def boolean_search(index, query):
    """
    Выполняет булев поиск по инвертированному индексу.
    Поддерживает операторы AND, OR и NOT, а также скобки для указания приоритета операций.
    """

    def tokenize(query):
        query = query.replace("(", " ( ").replace(")", " ) ") # Добавляем пробелы вокруг скобок
        return query.split()

    def parse_query(tokens):
        output = []
        operators = []

        precedence = {"NOT": 3, "AND": 2, "OR": 1, "(": 0}

        for token in tokens:
            if token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    output.append(operators.pop())
                operators.pop()
            elif token in ["AND", "OR", "NOT"]:
                while operators and operators[-1] != "(" and precedence[token] <= precedence[operators[-1]]:
                    output.append(operators.pop())
                operators.append(token)
            else:
                output.append(token)

        while operators:
            output.append(operators.pop())

        return output

    def evaluate_rpn(rpn_tokens, index):
        stack = []
        for token in rpn_tokens:
            if token in ["AND", "OR", "NOT"]:
                if token == "NOT":
                    operand = stack.pop()
                    stack.append(evaluate_not(operand, index))
                else:
                    operand2 = stack.pop()
                    operand1 = stack.pop()

                    operand1 = set(operand1)
                    operand2 = set(operand2)


                    if token == "AND":
                        stack.append(list(operand1.intersection(operand2)))
                    elif token == "OR":
                        stack.append(list(operand1.union(operand2)))
            else:
                if token in index:
                    stack.append(index[token])
                else:
                    stack.append([])

        return stack[0] if stack else []


    def evaluate_not(operand, index):
          all_docs = set()
          for doc_list in index.values():
              all_docs = all_docs.union(set(doc_list))

          operand = set(operand)

          return list(all_docs.difference(operand))


    tokens = tokenize(query)

    rpn_tokens = parse_query(tokens)

    results = evaluate_rpn(rpn_tokens, index)

    return results

user_query = input()

res = boolean_search(loaded_index, user_query)

print(f"Results for '{user_query}': {len(res)}: {res}")


