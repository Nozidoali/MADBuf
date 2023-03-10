#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
Author: Hanyu Wang
Created time: 2023-03-11 21:46:43
Last Modified by: Hanyu Wang
Last Modified time: 2023-03-12 12:32:35
'''

from MADBuf import *
from TestCases.TestCases import *
from TestCases.Generators import *


class TestMappingToFloat(TestCases):

    def test(self) -> None:
        for file in fpl_dfg_files():

            # these files are floating point operations
            dot = read_dfg(file)

            mappings = mapping_to_unfloating(dot)

            # check if there are still floating point operations
            for node in dot.nodes():
                assert node not in floating_point_operations()

            for mapping in mappings.mappings:
                floating, unfloating, use_buffer = mapping
                assert floating in floating_point_operations()
                assert unfloating not in floating_point_operations()

            # check if the mapping is correct 