import unittest

from pwCheck.strength import (
    calculate_entropy,
    checkLength,
    checkRepeat,
    checkSequences,
    checkPoolSize,
    checkCommon,
    evaluate_Password
)

class TestNewChecks(unittest.TestCase):

    def test_common_password(self):
        self.assertTrue(checkCommon("Password1"))
        self.assertFalse(checkCommon("xK9#mQ2$vL7!wR4pZ"))

    def test_common_password_rated_weak(self):
        result = evaluate_Password("qwertyuiop")
        self.assertEqual(result["rating"], "weak")
        self.assertIn("Common password", result["issues"])

    def test_letter_sequence(self):
        self.assertTrue(checkSequences("xxabcdxx"))

    def test_keyboard_sequence(self):
        self.assertTrue(checkSequences("myqwerpass"))
        self.assertFalse(checkSequences("xK9#mQ2$vL"))

class TestCalculateEntropy(unittest.TestCase):
    
    def test_empty_string(self):
        entropy, pool_size = calculate_entropy("")
        self.assertEqual(entropy, 0)
        self.assertEqual(pool_size, 0)

    def test_lowercase_only(self):
        # Pool size: 26
        # Entropy: 5 * log2(26) = 23.50
        entropy, pool_size = calculate_entropy("hello")
        self.assertEqual(pool_size, 26)
        self.assertAlmostEqual(entropy, 23.50, places=2)

    def test_all_character_types(self):
        # Pool size: 26 + 26 + 10 + 32 = 94
        # Entropy: 8 * log2(94) = 52.43
        entropy, pool_size = calculate_entropy("A1!aB2@b")
        self.assertEqual(pool_size, 94)
        self.assertAlmostEqual(entropy, 52.44, places=2)


class TestHelperFunctions(unittest.TestCase):

    def test_check_length(self):
        #length < = 8
        self.assertTrue(checkLength("12345678")) 
        #length > 8
        self.assertFalse(checkLength("123456789"))

    def test_check_repeat(self):
        #s repeats 3 times
        self.assertTrue(checkRepeat("passs123")) 
        # s repeats 2 times
        self.assertFalse(checkRepeat("pass123")) 

    def test_check_sequences(self):
        #contains 4 digits
        self.assertTrue(checkSequences("pass1234word")) 
        #contains 3 digits
        self.assertFalse(checkSequences("pass123word")) 

    def test_check_pool_size(self):
        #only 1 type
        self.assertTrue(checkPoolSize("onlyletters")) 
        #mixed types
        self.assertFalse(checkPoolSize("Letters123")) 


class TestEvaluatePasswordIntegration(unittest.TestCase):

    def test_weak_password(self):
        result = evaluate_Password("abc")
        self.assertEqual(result["rating"], "weak")
        self.assertIn("Password less than 8 characters", result["issues"])
        self.assertIn("Only one character type", result["issues"])

    def test_fair_password(self):
        # Pass12345 length 9, pool size 62 -> entropy ~53.59
        result = evaluate_Password("Pass12345")
        self.assertEqual(result["rating"], "fair")
        self.assertIn("There's a sequence", result["issues"])

    def test_strong_password(self):
        # K9#mX2$pL!8vQz length 14, pool size 94 -> entropy ~91.76
        result = evaluate_Password("K9#mX2$pL!8vQz")
        self.assertEqual(result["rating"], "strong")
        self.assertEqual(len(result["issues"]), 0)


if __name__ == "__main__":
    unittest.main()
