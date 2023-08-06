# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Atmosphere solver
-----------------
"""


import inspect
import numpy as np

from alexandria.data_structs.array import ensure_ndarray, find_nearest_entry


class atmosphere:

    def __init__(self,
                 h=None, t=None, p=None, d=None,
                 n=10000,
                 hrange=None,
                 solve=True):
        """
        :param h: Altitude    [km]
        :param t: Temperature [K]
        :param p: Pressure    [Pa]
        :param d: Density     [kg/m^3]
        """
        for item in inspect.signature(atmosphere).parameters:
            setattr(self, item, ensure_ndarray(eval(item)) if item != 'hrange' else eval(item))
            if not hasattr(self, 'driver'):
                if not isinstance(eval(item), type(None)):
                    self.driver = (item, ensure_ndarray(eval(item)))

        assert not(all([isinstance(v, type(None)) for v in self.__dict__.values()]))

        self._solve()

    def _solve(self):
        if self.driver[0] == 'h':
            self._run(self.h)
        else:
            if self.driver[1].size == 1:
                self.h = self._binary_search(self.driver[1])
            else:
                self.h = self._np_search()
            self._run(self.h)

    def _binary_search(self, target):
        """
        Perform a binary search over the image of a monotonical function.
        """
        # Objective
        accuracy = target/self.n

        # Domain
        domain = np.array([0, max(list(self.bounds.values()))] if isinstance(self.hrange, type(None)) else self.hrange,
                          dtype=float)
        m_incr = domain[1] > domain[0]      # Is the function monotonically increasing

        # Function
        def f(h):
            self._run(h)
            return getattr(self, self.driver[0])

        # Binary search
        solved = False
        reclim = 100

        # Quick exit
        if abs(f(domain[0]) - target) < accuracy:
            return domain[0]
        if abs(f(domain[1]) - target) < accuracy:
            return domain[1]

        n = 0
        while not solved and n < reclim:
            n += 1
            h                  = domain.mean()
            fn                 = f(h)
            error              = abs(fn - target)
            solved             = error < accuracy
            right              = m_incr and (target > fn)
            domain[int(right)] = h

        return h

    def _np_search(self):
        """
        Temperature is a not a monotonic function of altitude: the solution is thus inaccurate and
        will favor whichever point in the n-point sweep has a temperature value closest to the input.
          Current fix:
              - Height ranges
        """
        # Domain
        if isinstance(self.hrange, type(None)):
            h = np.linspace(0, max(list(self.bounds.values())), self.n)
        else:
            h = np.linspace(self.hrange[0], self.hrange[1], self.n)

        # Image
        self._run(h)

        # Search over NumPy array
        if self.driver[1].size == 1:
            idx = find_nearest_entry(getattr(self, self.driver[0]), self.driver[1])[0]
        else:
            idx = np.array([find_nearest_entry(getattr(self, self.driver[0]), v)[0] for v in self.driver[1]])

        # Output
        return h[idx]
