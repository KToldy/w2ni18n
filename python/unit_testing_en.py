# SPDX-FileCopyrightText: 2016 - Akshay Nagpal <akshaynagpal@user.noreplay.github.com>
# SPDX-FileCopyrightText: 2021 - Sebastian Ritter <bastie@users.noreply.github.com>
# SPDX-License-Identifier: MIT

import unittest
import sys
import logging
from word2numberi18n import w2n

class TestW2N(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        super(TestW2N, cls).setUpClass()
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
        log = logging.getLogger("SYSTEM")
        log.info(f"Testsystem is {sys.implementation.name} v{sys.version_info.major}.{sys.version_info.minor}@{sys.platform}")
    
    
    def test_positives_en(self):
        self.assertEqual(w2n.word_to_num("two million three thousand nine hundred and eighty four"), 2003984)
        self.assertEqual(w2n.word_to_num("nineteen"), 19)
        self.assertEqual(w2n.word_to_num("two thousand and nineteen"), 2019)
        self.assertEqual(w2n.word_to_num("two million three thousand and nineteen"), 2003019)
        self.assertEqual(w2n.word_to_num('three billion'), 3000000000)
        self.assertEqual(w2n.word_to_num('three million'), 3000000)
        self.assertEqual(w2n.word_to_num('one hundred twenty three million four hundred fifty six thousand seven hundred and eighty nine'), 123456789)
        self.assertEqual(w2n.word_to_num('eleven'), 11)
        self.assertEqual(w2n.word_to_num('nineteen billion and nineteen'), 19000000019)
        self.assertEqual(w2n.word_to_num('one hundred and forty two'), 142)
        self.assertEqual(w2n.word_to_num('112'), 112)
        self.assertEqual(w2n.word_to_num('11211234'), 11211234)
        self.assertEqual(w2n.word_to_num('five'), 5)
        self.assertEqual(w2n.word_to_num('two million twenty three thousand and forty nine'), 2023049)
        self.assertEqual(w2n.word_to_num('two point three'), 2.3)
        self.assertEqual(w2n.word_to_num('two million twenty three thousand and forty nine point two three six nine'), 2023049.2369)
        self.assertEqual(w2n.word_to_num('one billion two million twenty three thousand and forty nine point two three six nine'), 1002023049.2369)
        self.assertEqual(w2n.word_to_num('nine trillion one billion two million twenty three thousand and forty nine point two three six nine'), 9001002023049.2369)
        self.assertEqual(w2n.word_to_num('point one'), 0.1)
        self.assertEqual(w2n.word_to_num('point'), 0)
        self.assertEqual(w2n.word_to_num('point nineteen'), 0)
        self.assertEqual(w2n.word_to_num('one hundred thirty-five'), 135)
        self.assertEqual(w2n.word_to_num('hundred'), 100)
        self.assertEqual(w2n.word_to_num('thousand'), 1000)
        self.assertEqual(w2n.word_to_num('million'), 1000000)
        self.assertEqual(w2n.word_to_num('billion'), 1000000000)
        self.assertEqual(w2n.word_to_num('trillion'), 1000000000000)
        self.assertEqual(w2n.word_to_num("one million and thousand"), 1_001_000)
        self.assertEqual(w2n.word_to_num('nine point nine nine nine'), 9.999)
        self.assertEqual(w2n.word_to_num('seventh point nineteen'), 0)
        self.assertEqual(w2n.word_to_num('seven million, eight hundred, and sixty three thousand, two hundred, and fifty four'), 7863254)
        self.assertEqual(w2n.word_to_num('two hundreds'), 200)

        # test cases https://github.com/akshaynagpal/w2n/issues/54
        self.assertEqual(w2n.word_to_num('three point nine seven'), 3.97)
        self.assertEqual(w2n.word_to_num('two point seven eight'), 2.78)
        self.assertEqual(w2n.word_to_num('one point eight six'), 1.86)
        self.assertEqual(w2n.word_to_num('two point seven two'), 2.72)
        self.assertEqual(w2n.word_to_num('one point eight four'), 1.84)
        self.assertEqual(w2n.word_to_num('two point two eight'), 2.28)
        self.assertEqual(w2n.word_to_num('two point four seven'), 2.47)
        self.assertEqual(w2n.word_to_num('one point five nine'), 1.59)
        
        # test for kylosnite repository
        self.assertEqual(w2n.word_to_num("nine million nine thousand"), 9009000)
        
        # in different to w2n it is ok, in result of str:112 is not different to int:112
        self.assertEqual(w2n.word_to_num('112'), 112)
        self.assertEqual(w2n.word_to_num(112),112)
        
        # special name
        self.assertEqual(w2n.word_to_num('dozen'), 12)
        
        # https://github.com/akshaynagpal/w2n/issues/38
        self.assertEqual(w2n.word_to_num("hundred and twenty"),120)

        # https://github.com/akshaynagpal/w2n/issues/44
        self.assertEqual(w2n.word_to_num('two million one thousand'),2_001_000)
        
        #https://github.com/akshaynagpal/w2n/issues/27
        self.assertEqual(w2n.word_to_num("one million one hundred and eighty two thousand"),1_182_000)
        self.assertEqual(w2n.word_to_num("one million eighty two thousand"),1_082_000)
        
        #https://github.com/akshaynagpal/w2n/issues/58
        self.assertEqual(w2n.word_to_num("Example title - Chapter One Hundred Fifteen"), 115)
        self.assertEqual(w2n.word_to_num("Example title - Ninety-Eight"), 98)

    def test_negatives_en(self):
        self.assertRaises(ValueError, w2n.word_to_num, '112-')
        self.assertRaises(ValueError, w2n.word_to_num, '-')
        self.assertRaises(ValueError, w2n.word_to_num, 'on')
        self.assertRaises(ValueError, w2n.word_to_num, 'million million')
        self.assertRaises(ValueError, w2n.word_to_num, 'three million million')
        self.assertRaises(ValueError, w2n.word_to_num, 'million four million')
        self.assertRaises(ValueError, w2n.word_to_num, 'thousand million')
        self.assertRaises(ValueError, w2n.word_to_num, 'thousand trillion')
        self.assertRaises(ValueError, w2n.word_to_num, 'one billion point two million twenty three thousand and forty nine point two three six nine')
        self.assertRaises(ValueError, w2n.word_to_num, 'one thousand five million')
        self.assertRaises(ValueError, w2n.word_to_num, 'three million point two million')
        self.assertRaises(ValueError, w2n.word_to_num, 'three million point two hundred and five')
        
        
    def test_null_en(self):
        noneValue :str = None 
        self.assertRaises(ValueError, w2n.word_to_num, noneValue)
        noneValue = ""
        self.assertRaises(ValueError, w2n.word_to_num, noneValue)


if __name__ == '__main__':
    unittest.main()
