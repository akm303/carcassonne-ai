from wingedsheep.carcassonne.objects.actions.action import Action


class PassAction(Action):
    def __str__(self):
        return "pass"

    def __repr__(self):
        return "P()"

    def __eq__(self, other):
        return isinstance(other, PassAction)

    def __hash__(self):
        return hash("PassAction")
