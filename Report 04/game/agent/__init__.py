from . import Human, MiniMax


AGENTS = [
        ("Human", Human.HumanAgent), 
        ("MiniMax agent(depth 2)", lambda col: MiniMax.MiniMaxAgent(color=col,
            depth=2)),
        ("MiniMax agent(depth 3)", lambda col: MiniMax.MiniMaxAgent(color=col,
            depth=3)),
        ("MiniMax agent(depth 4)", lambda col: MiniMax.MiniMaxAgent(color=col,
            depth=4)),
        ("MiniMax agent(depth 5)", lambda col: MiniMax.MiniMaxAgent(color=col,
            depth=5)),
        ("MiniMax agent(depth 6)", lambda col: MiniMax.MiniMaxAgent(color=col,
            depth=6)),
        ("MiniMax agent(depth 7)", lambda col: MiniMax.MiniMaxAgent(color=col,
            depth=7)),
        ("MiniMax agent(depth 8)", lambda col: MiniMax.MiniMaxAgent(color=col,
            depth=8)),
        ("MiniMax agent(depth 9)", lambda col: MiniMax.MiniMaxAgent(color=col,
            depth=9)),
        ("MiniMax agent(depth 10)", lambda col: MiniMax.MiniMaxAgent(color=col,
            depth=10)),
        ("MiniMax agent(depth 11 - up to 10 seconds)", lambda col: MiniMax.MiniMaxAgent(color=col,
            depth=11)),
        ("MiniMax agent(depth 12 - up to 100 seconds)", lambda col: MiniMax.MiniMaxAgent(color=col,
            depth=12)),
        ]
