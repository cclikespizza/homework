__author__ = 'elmira'

import unittest


def drink(word):
    if word in ['выпив', ' выпивши', 'выпить']:
        return True
    return False


def fib(n):
    if type(n) != int:
        return -1
    a,b = 1,1
    for i in range(n-1):
        a,b = b,a+b
    return a


class FibTest(unittest.TestCase):
    def test_math(self):
        self.assertEqual(fib(0), 1)
        self.assertEqual(fib(1), 1)
        self.assertEqual(fib(8), 21)

    def test_bad_data(self):
        self.assertEqual(fib('котик'), -1)


class DrinkTest(unittest.TestCase):
    verb = ['выпил', ' выпила', ' выпило', 'выпью', 'выпил', ' выпила', ' выпило', 'выпьешь', 'выпей', 'выпил', ' выпила', ' выпило', 'выпьет', 'выпили', 'выпьем', 'выпьем', ' выпьемте', 'выпили', 'выпьете', 'выпейте', 'выпили', 'выпьют']
    gerund = ['выпив', ' выпивши', 'выпить']
    participle = ['выпивший', 'выпившая', 'выпившее', 'выпившие', 'выпившего', 'выпившей', 'выпившего', 'выпивших', 'выпившему', 'выпившей', 'выпившему', 'выпившим', 'выпившего', ' выпивший', 'выпившую', 'выпившее', 'выпивших', ' выпившие', 'выпившим', 'выпившей', ' выпившею', 'выпившим', 'выпившими', 'выпившем', 'выпившей', 'выпившем', 'выпивших', 'выпитый', 'выпитая', 'выпитое', 'выпитые', 'выпитого', 'выпитой', 'выпитого', 'выпитых', 'выпитому', 'выпитой', 'выпитому', 'выпитым', 'выпитого', ' выпитый', 'выпитую', 'выпитое', 'выпитых', ' выпитые', 'выпитым', 'выпитой', ' выпитою', 'выпитым', 'выпитыми', 'выпитом', 'выпитой', 'выпитом', 'выпитых', 'выпит', 'выпита', 'выпито', 'выпиты']

    def test_participle(self):
        for i in self.participle:
            self.assertEqual(drink(i), True)

    def test_verb(self):
        for i in self.verb:
            self.assertEqual(drink(i), True)

    def test_gerund(self):
        for i in self.gerund:
            self.assertEqual(drink(i), True)

    def test_random(self):
        self.assertEqual(drink('выпитутуту'), False)
        self.assertEqual(drink('туту'), False)
        self.assertEqual(drink('выпи'), False)

if __name__ == "__main__":
    unittest.main(verbosity=1)