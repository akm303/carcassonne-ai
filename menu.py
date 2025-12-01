import tkinter as tk
from tkinter import ttk


class CarcassonneMenu:

    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("400x600")

        # variables that store values for out buttons
        self.numPlayers = tk.IntVar(value=2)
        self.choiceScoreboard = tk.BooleanVar(value=False)
        self.numSpeed = tk.DoubleVar(value=0.0)

        # stores input from the menu, set the initial values for quick agent check
        self.input = {"num_players": 2, "speed": 0.0, "scoreboard": False, "agents": []}

        # To store all widgets for agents, so we can display them depending on the number
        self.agentValues = []
        self.agentLabelsWid = []
        self.agentButtonsWid = []

        self.createMenu()


    def createMenu(self):
        # create labels for the menu
        # ---------------------------#
        l1 = tk.Label(self.root, text="Menu", font=("Arial", 33, "bold"))
        l1.grid(row=0, column=0, columnspan=2, pady=5)
        l2 = tk.Label(self.root, text="Welcome to Carcassonne!", font=("Helvetica", 22, "bold"))
        l2.grid(row=1, column=0, columnspan=2, pady=20)
        l3 = tk.Label(self.root, text="Game Speed:")
        l3.grid(row=2, column=0, padx=10, pady=5)
        l4 = tk.Label(self.root, text="Scoreboard Info:")
        l4.grid(row=3, column=0, padx=10, pady=5)
        l5 = tk.Label(self.root, text="Number of Agents:")
        l5.grid(row=4, column=0, padx=10, pady=5)
        l6 = tk.Label(self.root, text="Choose Agents Wisely!")
        l6.grid(row=5, column=0, columnspan=2, pady=15)


        # Create buttons for the menu
        # ---------------------------#
        frameAgentNumChoice = tk.Frame(self.root)
        frameAgentNumChoice.grid(row=4, column=1)
        options = [2,3,4,5]
        # create radio buttons, so only one choice of number of agents is possible. Add them into the frame from left
        for count in options:
            tk.Radiobutton(frameAgentNumChoice, text=str(count), variable=self.numPlayers, value=count, command=self.drawAgentChoice).pack(side = "left", padx=5)
        # scoreboard check if it should be visible in the game
        tk.Checkbutton(self.root, text="Show Score", variable=self.choiceScoreboard).grid(row=3, column=1)
        # additional speed adjust system ---- so we can track agents' moves more precise
        tk.Scale(self.root, from_=0.0, to=2.0, resolution=0.1, orient="horizontal", variable=self.numSpeed).grid(row=2, column=1)
        agents = ["Random", "Q-Learning", "MCTS", "Human (Not Available)", "Sarsa (Not Available)", "... coming soon"]
        # create 5 rows for maximum number of agents. Extra ones won't be displayed
        for i in range(5):
            # connect value to the dropdown choice
            value = tk.StringVar(value="Random")
            self.agentValues.append(value)
            label = tk.Label(self.root, text=f"Player - {i + 1} Agent:")
            self.agentLabelsWid.append(label)
            choice = ttk.Combobox(self.root, textvariable=value, values=agents, state="readonly")
            self.agentButtonsWid.append(choice)
        tk.Button(self.root, text="START",command=self.startPressed).grid(row=12, column=0, columnspan=2, pady=20)


        # call agent choice function to show first two agent selections as base case
        self.drawAgentChoice()

    def drawAgentChoice(self):
        count = self.numPlayers.get()
        # draw agent choices depending on radio button
        start = 6

        for i in range(5):
            if i < count:
                self.agentLabelsWid[i].grid(row=start + i , column=0, padx=10, pady=5)
                self.agentButtonsWid[i].grid(row=start + i  , column=1, padx=10,pady=5)
            else:
                self.agentLabelsWid[i].grid_forget()
                self.agentButtonsWid[i].grid_forget()

    def startPressed(self):
        self.input["num_players"] = self.numPlayers.get()
        self.input["speed"] = self.numSpeed.get()
        self.input["scoreboard"] = self.choiceScoreboard.get()

        # get agents depending on the radio button number
        count = self.input["num_players"]
        self.input["agents"] = [self.agentValues[i].get() for i in range(count)]

        # stop the mainloop, so we return to run and return player's input
        self.root.quit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        # check if the player chose available agents
        if not self.input["agents"]:
            return None
        return self.input