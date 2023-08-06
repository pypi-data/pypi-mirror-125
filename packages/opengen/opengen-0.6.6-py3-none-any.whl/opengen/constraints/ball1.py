from .constraint import Constraint
from .simplex import Simplex
import numpy as np


class Ball1(Constraint):
    """Ball1 aka Norm-1 Ball

    Ball-1 with given radius.

    """

    def __init__(self, radius: float = 1.0):  # unless specified, alpha=1
        """Constructor for a Ball1

        Args:
            :param radius: ball radius (default: 1)

        Returns:
            :return: New instance of Ball1 with given radius
        """
        if radius <= 0:
            raise ValueError("radius must be a positive number")

        self.__radius = float(radius)

    @property
    def radius(self):
        """Returns the radius of this ball"""
        return self.__radius

    def distance_squared(self, u):
        raise NotImplementedError()

    def project(self, u):
        """Project on the current Ball-1

        Args:
            :param u: vector u

        Returns:
            :return: projection of u onto the current ball-1

        """
        if np.linalg.norm(u, 1) <= self.radius:
            return u

        n = len(u)
        simplex = Simplex(self.radius)
        x = simplex.project(abs(u))
        z = np.zeros(n)
        for i, (ui, xi) in enumerate(zip(u, x)):
            z[i] = np.sign(ui) * xi
        return z

    def is_convex(self):
        return True

    def is_compact(self):
        return True
