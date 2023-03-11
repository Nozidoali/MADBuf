from TestCases.TestCases import TestCases

from TestCases.Utils import *
from TestCases.SubjectGraph import *
from TestCases.IO import *
from TestCases.Synthesis import *

registered_tests = [
    # TestMADBuf(),
    # TestCutLoopback(),
    # TestDynamaticIO(),
    # TestFloatingPointMapping(),
    TestSubjectGraph(),
    TestUtils(),
    TestIO(),
    TestSynthesis(),
]

class TestAll(TestCases):

    def run(self):
        for test in registered_tests:
            test.test()