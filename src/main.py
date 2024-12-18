# TODO: switch to PyQt6

import models


def main() -> None:
    running = True
    graph_type_index = int(input(
        "Which your graph type will be? Type index.\n" + 
        '\n'.join([f"{i} {kind}" for i, kind in enumerate(models.graph_actions)]) +
        '\n'
    ))
    graph_type: str = list(models.graph_actions.keys())[graph_type_index]
    graph: models.BaseGraph = eval(f"models.{graph_type}")()
    while running:
        graph.show(1000, -10, 10)
        user_action_prompt = input(
            "Type index of graph change! Or type 'quit' to exit\n" + 
            '\n'.join(f"{i} {action}" for i, action in enumerate(models.graph_actions[graph_type])) +
            '\n'
            )
        if user_action_prompt == "quit":
            print("Bye!")
            running = False
            break
        user_action = int(user_action_prompt)
        value = float(input("Type value\n"))
        getattr(graph, models.graph_actions[graph_type][user_action])(value)


if __name__ == "__main__":
    main()