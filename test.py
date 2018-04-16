# -*- coding: utf-8 -*-

from unittest import TestLoader, TextTestRunner, TestSuite
from test.grids import TestGridsService
from test.grid import TestGridService
from test.cells import TestCellsService


def main():
    loader = TestLoader()
    tests = [
        loader.loadTestsFromTestCase(test)
        for test in (TestGridService, TestGridsService, TestCellsService)
    ]
    suite = TestSuite(tests)
    runner = TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':
    main()
