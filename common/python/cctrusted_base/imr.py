"""
Integrated Measurement Register packages.
"""

from abc import ABC, abstractmethod
from cctrusted_base.tcg import TcgDigest, TcgAlgorithmRegistry

class TcgIMR(ABC):
    """
    Common Integrated Measurement Register class
    """

    _INVALID_IMR_INDEX = -1

    def __init__(self, index, default_alg_id, default_digest_hash):
        self._index = index
        self._digests:dict[int, TcgDigest] = \
            {default_alg_id:TcgDigest(default_alg_id, default_digest_hash)}

    @property
    def index(self) -> int:
        """
        The index of IMR register
        """
        return self._index

    @property
    def digests(self) -> dict:
        """
        Digests dict
        """
        return self._digests

    def digest(self, alg_id):
        """
        The digest value of IMR
        """
        if alg_id not in self._digests:
            return None
        return self._digests[alg_id]

    @property
    @abstractmethod
    def max_index(self):
        """
        The max index value of IMR
        """
        raise NotImplementedError("Need implemented in different arch")

    def is_valid(self):
        """
        Check whether IMR is valid or not
        """
        return self._index != TcgIMR._INVALID_IMR_INDEX and \
            self._index <= self.max_index

class TdxRTMR(TcgIMR):
    """
    RTMR class defined for Intel TDX
    """

    @property
    def max_index(self):
        return 3

    def __init__(self, index, digest_hash):
        super().__init__(index, TcgAlgorithmRegistry.TPM_ALG_SHA384,
                        digest_hash)

class TpmPCR(TcgIMR):
    """
    PCR class defined for TPM
    """

    @property
    def max_index(self):
        return 23
