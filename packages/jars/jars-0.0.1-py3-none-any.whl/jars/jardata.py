from typing import Tuple

import jax
import polars

class JarData:
    """
    Jar data object

    Jar objects provide interfaces
    as well as transparent support
    for omics datasets.
    """
    def __init__(self, data):
        self.data = data

    @property
    def shape(self) -> Tuple[int, int]:
        """Shape of data, all observations and variables combined (:attr:`n_obs`, :attr:`n_var`)."""
        return self.n_obs, self.n_vars
    
    @property
    def n_obs(self) -> int:
        """
        Total number of observations
        """
        return 0
    
    @property
    def n_vars(self) -> int:
        """
        Total number of variables
        """
        return 0
