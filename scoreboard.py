
def drawScoreboard(game, players):
    canvas = game.visualiser.canvas
    canvas.create_rectangle(25, 25, 325, 125 + len(players) * 40, fill="white", outline="black", width=3)

    currentPlayIndex = game.get_current_player()
    currentPlayType = players[currentPlayIndex].type

    canvas.create_text(50, 50, anchor="w", text=f"Current turn: Player {currentPlayIndex + 1}", fill="black", font=("Arial", 20, "bold"))
    canvas.create_text(50, 80, anchor="w", text=f"Agent: {currentPlayType}", fill="black", font=("Arial", 20, "bold"))

    canvas.create_text(50, 110, anchor="w", text="Scores:", font=("Arial", 20, "bold"))
    startY = 140
    for i, score in enumerate(game.state.scores):
        agentType = players[i].type
        # highlight current player with special color
        if i == currentPlayIndex:
            canvas.create_text(50, startY + 25 * i, anchor="w", text=f"Player {i + 1} ({agentType}): {score}", font=("Arial", 15), fill = "green")
        else:
            canvas.create_text(50, startY + 25 * i, anchor="w", text=f"Player {i + 1} ({agentType}): {score}", font=("Arial", 15), fill="black")


