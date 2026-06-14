from dataclasses import dataclass
from enum import Enum




@dataclass(frozen=True, slots=True, kw_only=True)
class NewMatch:
    point
    game
    tennis_set
    tie_briek

    def __to_dict(self):
        pass