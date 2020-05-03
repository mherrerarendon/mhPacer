import unittest

from colorama import init, Fore, Style
import RunningPaceConverter_test
import SpeedStrParser_test

if __name__ == '__main__':
    init(autoreset=True)
    testSuite = unittest.defaultTestLoader.loadTestsFromModule(RunningPaceConverter_test)
    testSuite.addTests(unittest.defaultTestLoader.loadTestsFromModule(SpeedStrParser_test))
    results = unittest.TestResult()
    testSuite.run(results)
    if results.wasSuccessful():
        print(Fore.GREEN + 'All {} tests passed'.format(results.testsRun))
    elif len(results.errors) > 0:
        errors = results.errors
        print(Style.BRIGHT + '{} ERRORS:'.format(len(errors)))
        for testCase, traceback in errors:
            print(Fore.RED + testCase.id())
            print(traceback)
    elif len(results.failures) > 0:
        failures = results.failures
        print(Style.BRIGHT + '{} FAILURES:'.format(len(failures)))
        for testCase, traceback in failures:
            print(Fore.RED + testCase.id())
            print(traceback)
