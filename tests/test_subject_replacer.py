import unittest

class SimpleTestCase(unittest.TestCase):
    def test_sum(self):
        assert sum([1, 2, 3]) == 6, "Should be 6"

    def test_sum_tuple(self):
        assert sum((1, 2, 2)) == 5, "Should be 6"

    def test_uppercase(self):
        assert "loud noises".upper() == "LOUD NOISES"

    def test_reversed(self):
        assert list(reversed([1, 2, 3, 4])) == [4, 3, 2, 1]

    def test_some_primes(self):
        assert 37 in {
            num
            for num in range(1, 50)
            if num != 1 and not any([num % div == 0 for div in range(2, num)])
            }

if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
