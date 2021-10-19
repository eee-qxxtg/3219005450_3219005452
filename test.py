import unittest
import four_arithmetic


# 部分函数测试
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.calculate_gcd = four_arithmetic.calculate_gcd  # 辗转相除法求两整数最大公因数
        self.reduce_fraction = four_arithmetic.reduce_fraction  # 对分数进行约分
        self.true_fraction = four_arithmetic.true_fraction  # 将分子大于分母的分数化为真分数
        self.operate1 = four_arithmetic.operate  # 两数运算结果为负数、除数或者分母为0时，返回 False
        self.operate2 = four_arithmetic.operate
        self.num_test2 = four_arithmetic.num_test
        self.num_test3 = four_arithmetic.num_test
        self.normalize_num = four_arithmetic.normalize_num  # 化为分数

    def tearDown(self):
        self.calculate_gcd = None
        self.reduce_fraction = None
        self.true_fraction = None
        self.operate = None
        self.num_test = None
        self.normalize_num = None

    def test(self):
        self.assertEqual(self.calculate_gcd(100, 125), 25)
        self.assertEqual(self.reduce_fraction("24/44"), "6/11")
        self.assertEqual(self.true_fraction("18", "16"), "1’1/8")
        self.assertEqual(self.operate1("-4", '+', "3"), False)
        self.assertEqual(self.operate2("10", '/', "0",), False)
        self.assertEqual(self.num_test2("22/2"), False)
        self.assertEqual(self.num_test3("6/7"), True)
        self.assertEqual(self.normalize_num("1’2/5"), "7/5")


def suite():
    s = unittest.TestCase()
    s.addTest(MyTestCase('test'))
    return s


if __name__ == '__main__':
    unittest.main()
