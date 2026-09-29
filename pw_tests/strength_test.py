import unittest
# Import all functions from your implementation file (e.g., password_evaluator.py)

from pwCheck.strength import (
    calculate_entropy,
    checkLength,
    checkRepeat,
    checkSequences,
    checkPoolSize,
    evaluate_Password
)

class TestCalculateEntropy(unittest.TestCase):
    
    def test_empty_string(self):
        entropy, pool_size = calculate_entropy("")
        self.assertEqual(entropy, 0)
        self.assertEqual(pool_size, 0)

    def test_lowercase_only(self):
        # Pool size: 26. Entropy: 5 * log2(26) ≈ 23.50
        entropy, pool_size = calculate_entropy("hello")
        self.assertEqual(pool_size, 26)
        self.assertAlmostEqual(entropy, 23.50, places=2)

    def test_all_character_types(self):
        # Pool size: 26 + 26 + 10 + 32 = 94
        # Entropy: 8 * log2(94) ≈ 52.43
        entropy, pool_size = calculate_entropy("A1!aB2@b")
        self.assertEqual(pool_size, 94)
        self.assertAlmostEqual(entropy, 52.43, places=2)


class TestHelperFunctions(unittest.TestCase):

    def test_check_length(self):
        self.assertTrue(checkLength("12345678"))   # Length <= 8 -> issue present
        self.assertFalse(checkLength("123456789")) # Length > 8  -> issue absent

    def test_check_repeat(self):
        self.assertTrue(checkRepeat("passs123"))   # 'sss' repeats 3 times
        self.assertFalse(checkRepeat("pass123"))   # 'ss' repeats 2 times

    def test_check_sequences(self):
        self.assertTrue(checkSequences("pass1234word")) # Contains 4 digits
        self.assertFalse(checkSequences("pass123word"))  # Contains 3 digits

    def test_check_pool_size(self):
        self.assertTrue(checkPoolSize("onlyletters"))   # Single type (26)
        self.assertFalse(checkPoolSize("Letters123"))   # Mixed types (52)


class TestEvaluatePasswordIntegration(unittest.TestCase):

    def test_weak_password(self):
        result = evaluate_Password("abc")
        self.assertEqual(result["rating"], "weak")
        self.assertIn("Password is 8 characters or fewer", result["issues"])
        self.assertIn("Only uses one character type", result["issues"])

    def test_fair_password(self):
        # Pass12345 length 9, pool size 62 -> entropy ~53.59
        result = evaluate_Password("Pass12345")
        self.assertEqual(result["rating"], "fair")
        self.assertIn("Contains a sequence of digits", result["issues"])

    def test_strong_password(self):
        # K9#mX2$pL!8vQz length 14, pool size 94 -> entropy ~91.76
        result = evaluate_Password("K9#mX2$pL!8vQz")
        self.assertEqual(result["rating"], "strong")
        self.assertEqual(len(result["issues"]), 0)


if __name__ == "__main__":
    unittest.main()
