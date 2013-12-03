import unittest
import numpy as np
from mpi4py import MPI
import math

from skylark import cskylark

from helper.test import svd_bound
from helper.test import test_helper

import elem

_M = 10000
_N = 100
_R = 1000

class JLT_test(unittest.TestCase):

    def setUp(self):
        # We do not initialize Skylark so it will take the seed
        # from system time (new seed each time).
        # To be clean, and have every test self contained, we reinitalize
        # Skylark with a new time based seed
        cskylark.initialize()

        #params
        self.num_repeats = 5
        self.accuracy    = 0.5
        _R = _N / self.accuracy**2

    def tearDown(self):
        # No real need to do this...
        cskylark.finalize()

    def test_apply_colwise(self):
        A = elem.DistMatrix_d_VR_STAR()

        #FIXME: Christos, use your matrix problem factory here
        elem.Uniform(A, _M, _N)

        measures    = [svd_bound] #.. add more measures to be computed in a test
        results     = svd_test_helper(A, _M, _N, _R, cskylark.JLT, measures)

        suc = np.zeros(len(results[0].success))
        avg = np.zeros(len(results[0].average))
        for result in results:
            avg = avg + result.average
            suc = np.logical_or(suc, result.success)

        # check if at leaste one was successful
        self.assertTrue(np.all(suc))

        # check if average is in bounds
        avg = avg / num_repeats
        self.assertTrue(np.all(avg <= accuracy))


if __name__ == '__main__':
    unittest.main()