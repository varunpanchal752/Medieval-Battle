import numpy as np
from enum import Enum
from typing import List, Optional
from scipy.optimize import linear_sum_assignment
from datetime import datetime

class UnitClass(Enum):
    MILITIA = "Militia"
    SPEARMEN = "Spearmen"
    LIGHT_CAVALRY = "LightCavalry"
    HEAVY_CAVALRY = "HeavyCavalry"
    FOOT_ARCHER = "FootArcher"
    CAVALRY_ARCHER = "CavalryArcher"

# Mapping of which classes have advantage over others
ADVANTAGE = {
    UnitClass.MILITIA: {UnitClass.SPEARMEN, UnitClass.LIGHT_CAVALRY},
    UnitClass.SPEARMEN: {UnitClass.LIGHT_CAVALRY, UnitClass.HEAVY_CAVALRY},
    UnitClass.LIGHT_CAVALRY: {UnitClass.FOOT_ARCHER, UnitClass.CAVALRY_ARCHER},
    UnitClass.HEAVY_CAVALRY: {UnitClass.MILITIA, UnitClass.FOOT_ARCHER, UnitClass.LIGHT_CAVALRY},
    UnitClass.CAVALRY_ARCHER: {UnitClass.SPEARMEN, UnitClass.HEAVY_CAVALRY},
    UnitClass.FOOT_ARCHER: {UnitClass.MILITIA, UnitClass.CAVALRY_ARCHER},
}

class Platoon:
    def __init__(self, unit_class: UnitClass, count: int):
        self.unit_class = unit_class
        self.count = count

    @classmethod
    def from_str(cls, token: str) -> 'Platoon':
        """
        Alternative constructor to create a Platoon from a string token.
        Parse a token formatted as "Class#Number" into a Platoon.
        Example: "Spearmen#10".
        """
        name, num = token.split("#")
        return cls(UnitClass(name), int(num))

    def strength_against(self, other: 'Platoon') -> float:
        """
        Calculate effective strength ratio:
        - Double the count if this platoon has class advantage.
        - Divide by opponent's count to get relative strength.
        """
        eff = self.count * (2 if other.unit_class in ADVANTAGE[self.unit_class] else 1)
        return eff / other.count

    def __repr__(self):
        return f"{self.unit_class.value}#{self.count}"

class BattlePlanner:
    """
    Plans the optimal assignment of your platoons to enemy platoons
    using the Hungarian algorithm to maximize the number of victories.
    """
    def __init__(self, ours: List[Platoon], theirs: List[Platoon]):
        self.ours = ours
        self.theirs = theirs

    def find_optimal_order(self) -> Optional[List[Platoon]]:
        """
        Returns a list of your platoons ordered to fight each enemy in input order.
        If fewer than 3 wins are possible with the best assignment, returns None.
        """
        n = len(self.ours)

        # Build a score matrix: +1 win, 0 draw, -1 loss
        matrix = np.zeros((n, n), dtype=int)
        for i, ours in enumerate(self.ours):
            for j, theirs in enumerate(self.theirs):
                ratio = ours.strength_against(theirs)
                matrix[i, j] = 1 if ratio > 1 else (0 if ratio == 1 else -1)

        # Solve assignment: maximize total score without reuse of rows/columns
        rows, cols = linear_sum_assignment(matrix, maximize=True)
        wins = sum(matrix[r, c] == 1 for r, c in zip(rows, cols))
        if wins < 3:
            return None

        # return our platoons arranged in opponent's order
        result = [None] * n
        for r, c in zip(rows, cols):
            result[c] = self.ours[r]
        return result
