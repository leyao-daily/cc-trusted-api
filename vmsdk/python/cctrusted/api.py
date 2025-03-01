"""
CC Trusted API Implementation.
"""
import logging

# pylint: disable=unused-import
from cctrusted_base.imr import TcgIMR
from cctrusted_base.tcg import TcgAlgorithmRegistry
from cctrusted_base.tdx.report import TdReport
from .cvm import ConfidentialVM, TdxVM

LOG = logging.getLogger(__name__)

def get_default_algorithms() -> TcgAlgorithmRegistry:
    """
    Get default algorithms ID supported by platform
    """
    cvm_inst = ConfidentialVM.inst()
    return TcgAlgorithmRegistry(cvm_inst.default_algo_id)

def get_measurement_count() -> int:
    """
    Get IMR register value according to given index
    """
    cvm_inst = ConfidentialVM.inst()
    return len(cvm_inst.imrs)

def get_measurement(imr_select:[int, int]) -> TcgIMR:
    """
    Get IMR register value according to given index
    """
    cvm_inst = ConfidentialVM.inst()
    cvm_inst.dump()

    imr_index = imr_select[0]
    algo_id = imr_select[1]

    if imr_index not in cvm_inst.imrs:
        LOG.error("Invalid select index for IMR.")
        return None

    if algo_id is None or algo_id is TcgAlgorithmRegistry.TPM_ALG_ERROR:
        algo_id = cvm_inst.default_algo_id

    return cvm_inst.imrs[imr_index].digest(algo_id)

def get_tdx_report() -> TdReport:
    """
    Get TDX Report
    """
    cvm_inst = ConfidentialVM.inst()
    cvm_inst.dump()

    assert isinstance(cvm_inst, TdxVM)
    return cvm_inst.tdreport
