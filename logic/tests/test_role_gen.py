import random
import unittest

# Assuming your function and Role enum/class are defined like this:
class Role:
    VILLAGER = "Villager"
    WEREWOLF = "Werewolf"
    SEER = "Seer"

def assign_roles(players_name: list, amount_roles: dict, rng=None) -> dict[str, Role]:
    role_list = []
    # Note: Fixed 'd.items()' to 'amount_roles.items()' from your original snippet
    for k, v in amount_roles.items():
        role_list.extend([k] * v)

    rand = rng or random
    rand.shuffle(role_list)

    return dict(zip(players_name, role_list))


class TestAssignRoles(unittest.TestCase):

    def setUp(self):
        self.players = ["Alice", "Bob", "Charlie", "David"]
        self.roles_input = {Role.VILLAGER: 2, Role.WEREWOLF: 1, Role.SEER: 1}

    def test_assignments_are_correct_length(self):
        """Ensure every player gets exactly one role."""
        assignments = assign_roles(self.players, self.roles_input)
        self.assertEqual(len(assignments), len(self.players))
        
        # Ensure all players are keys in the resulting dictionary
        for player in self.players:
            self.assertIn(player, assignments)

    def test_role_counts_are_preserved(self):
        """Ensure the exact number of requested roles are distributed."""
        assignments = assign_roles(self.players, self.roles_input)
        
        # Count how many of each role were actually assigned
        assigned_counts = {}
        for role in assignments.values():
            assigned_counts[role] = assigned_counts.get(role, 0) + 1

        self.assertEqual(assigned_counts[Role.VILLAGER], 2)
        self.assertEqual(assigned_counts[Role.WEREWOLF], 1)
        self.assertEqual(assigned_counts[Role.SEER], 1)

    def test_deterministic_with_seeded_rng(self):
        """Ensure that providing a seeded RNG produces reproducible results."""
        rng1 = random.Random(42)
        rng2 = random.Random(42)

        res1 = assign_roles(self.players, self.roles_input, rng=rng1)
        res2 = assign_roles(self.players, self.roles_input, rng=rng2)

        self.assertEqual(res1, res2)

if __name__ == "__main__":
    unittest.main()