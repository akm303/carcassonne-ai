from wingedsheep.carcassonne.objects.actions.action import Action


class PassAction(Action):
    def __str__(self):
        return "pass"

    def __repr__(self):
        return "PassAction()"
