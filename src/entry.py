class Entry:
    def __init__(
        self,
        name: str,
        initiative: int = 0,
        init_bonus: int = 0,
        ac: int = 0,
        hp_max: int = 0,
        hp: int = 0,
        hidden: bool = False,
    ) -> None:
        self.name = name
        self.initiative = initiative
        self.init_bonus = init_bonus
        self.ac = ac
        self.hp_max = hp_max
        self.hp = hp
        self.hidden = hidden

    def __lt__(self, other):
        return self.initiative < other.initiative

    def __le__(self, other):
        return self.initiative <= other.initiative

    def __eq__(self, other):
        return self.initiative == other.initiative

    def __ne__(self, other):
        return self.initiative != other.initiative

    def __gt__(self, other):
        return self.initiative > other.initiative

    def __ge__(self, other):
        return self.initiative >= other.initiative

    def heal(self, amount: int) -> None:
        self.hp += amount

    def damage(self, amount: int) -> None:
        self.heal(-amount)

    def toggle_hidden(self) -> None:
        self.hidden = not self.hidden

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "initiative": self.initiative,
            "init_bonus": self.init_bonus,
            "ac": self.ac,
            "hp_max": self.hp_max,
            "hp": self.hp,
            "hidden": self.hidden,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name", ""),
            initiative=data.get("initiative", 0),
            init_bonus=data.get("init_bonus", 0),
            ac=data.get("ac", 0),
            hp_max=data.get("hp_max", 0),
            hp=data.get("hp", 0),
            hidden=data.get("hidden", False),
        )
