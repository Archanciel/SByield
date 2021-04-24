'''
This test suite is usefull on Android. It runs on Pydroid 3, but not on QPython 3
since it has a dependency on Kivy resources which are not supported by QPython 3.
It has no dependency on the sl4a library, supported by QPython 3, but not by Pydroid 3.
It can be executed as well in Pycharm on Windows !
'''

from unittest import TestLoader, TextTestRunner, TestSuite

from testpricerequester import TestPriceRequester
from testcryptofiatratecomputer import TestCryptoFiatRateComputer
from testsbyieldratecomputer import TestSBYieldRateComputer
from testownerdeposityieldcomputer import TestOwnerDepositYieldComputer
from testprocessor import TestProcessor
from testcontroller import TestController


if __name__ == "__main__":
    '''
    This test suite runs on Android in Pydroid, but fails in QPython !
    '''
    loader = TestLoader()
    suite = TestSuite((loader.loadTestsFromTestCase(TestPriceRequester),
                       loader.loadTestsFromTestCase(TestCryptoFiatRateComputer),
                       loader.loadTestsFromTestCase(TestCryptoFiatRateComputer),
                       loader.loadTestsFromTestCase(TestSBYieldRateComputer),
                       loader.loadTestsFromTestCase(TestOwnerDepositYieldComputer),
                       loader.loadTestsFromTestCase(TestProcessor),
                       loader.loadTestsFromTestCase(TestController)
    ))
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
