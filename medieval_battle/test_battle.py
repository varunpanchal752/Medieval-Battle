import unittest
from battle import Platoon, UnitClass, BattlePlanner

class BattleAssignTest(unittest.TestCase):
    def test_strength(self):
        """
        Verify strength_against doubles count correctly when advantage exists.
        Spearmen should have advantage over Heavy Cavalry.
        """
        a = Platoon(UnitClass.SPEARMEN, 100)
        b = Platoon(UnitClass.HEAVY_CAVALRY, 200)
        # Effective strength: 100*2/200 = 1.0
        self.assertEqual(a.strength_against(b), 200 / 200)

    def test_optimal_plan(self):
        ours = [
            "Spearmen#10","Militia#30","FootArcher#20",
            "LightCavalry#1000","HeavyCavalry#120"
        ]
        theirs = [
            "Militia#10","Spearmen#10","FootArcher#1000",
            "LightCavalry#120","CavalryArcher#100"
        ]
        ours_p = [Platoon.from_str(x) for x in ours]
        theirs_p = [Platoon.from_str(x) for x in theirs]
        plan = BattlePlanner(ours_p, theirs_p).find_optimal_order()
        self.assertIsNotNone(plan)       # Ensure a strategy was found
        self.assertEqual(len(plan), 5)   # All 5 platoons are assigned

        wins = sum(
            p.strength_against(t) > 1
            for p, t in zip(plan, theirs_p)
        )
        self.assertGreaterEqual(wins, 3)

if __name__ == "__main__":
    unittest.main()
