import pytest

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from .utils import *
from .addons import *

import qcdb
import qcengine as qcng

@pytest.fixture
def h2o():
    return """
    O
    H 1 R
    H 1 R 2 A

    R=0.958
    A=104.5
"""

@pytest.fixture
def nh2():
    return """
    0 2
    N
    H 1 R
    H 1 R 2 A
    
    R=1.008
    A=105.0
"""


@pytest.mark.parametrize('mtd,opts', [
    pytest.param('c4-mp2', {'cfour_basis': 'qz2p', 'cfour_scf_conv': 12}, marks=using_cfour),
    pytest.param('c4-mp2', {'basis': 'cfour-qz2p', 'cfour_scf_conv': 12}, marks=using_cfour),
    pytest.param('gms-mp2', {'basis': 'cfour-qz2p', 'gamess_mp2__nacore': 0}, marks=using_gamess),
    pytest.param('nwc-mp2', {'basis': 'cfour-qz2p', 'qc_module': 'tce'}, marks=using_nwchem),
    pytest.param('nwc-mp2', {'basis': 'cfour-qz2p'}, marks=using_nwchem),
    pytest.param('p4-mp2', {'basis': 'cfour-qz2p'}, marks=using_psi4),
])
def test_sp_hf_rhf_full(mtd, opts, h2o):
    """cfour/???/input.dat
    #! single point MP2/qz2p on water

    """
    h2o = qcdb.set_molecule(h2o)
    qcdb.set_options(opts)

    e, jrec = qcdb.energy(mtd, return_wfn=True, molecule=h2o)

    # from cfour
    scftot = -76.0627484601
    mp2tot = -76.332940127333
    mp2corl = mp2tot - scftot
    atol = 5.e-5

    assert compare_values(mp2tot, e, tnm() + ' Returned', atol=atol)
    assert compare_values(mp2tot, qcdb.variable('current energy'), tnm() + ' Current', atol=atol)
    assert compare_values(mp2tot, qcdb.variable('mp2 total energy'), tnm() + ' MP2', atol=atol)
                                                                                               
    assert compare_values(mp2corl, qcdb.variable('current correlation energy'), tnm() + ' MP2 Corl', atol=atol)
    assert compare_values(mp2corl, qcdb.variable('mp2 correlation energy'), tnm() + ' MP2 Corl', atol=atol)

    assert compare_values(scftot, qcdb.variable('hf total energy'), tnm() + ' SCF', atol=atol)
    assert compare_values(scftot, qcdb.variable('scf total energy'), tnm() + ' SCF', atol=atol)



@pytest.mark.parametrize('mtd,opts', [
    pytest.param('c4-mp2', {'cfour_basis': 'qz2p', 'cfour_dropmo': [1], 'cfour_scf_conv': 12}, marks=using_cfour),
    pytest.param('c4-mp2', {'basis': 'cfour-qz2p', 'cfour_dropmo': 1, 'cfour_scf_conv': 12}, marks=using_cfour),
    pytest.param('gms-mp2', {'basis': 'cfour-qz2p', 'nwchem_mp2__freeze': 1}, marks=using_gamess),
    pytest.param('nwc-mp2', {'basis': 'cfour-qz2p', 'qc_module': 'tce', 'nwchem_tce__freeze': 1}, marks=using_nwchem),
    pytest.param('nwc-mp2', {'basis': 'cfour-qz2p', 'nwchem_mp2__freeze': 1}, marks=using_nwchem),
    pytest.param('p4-mp2', {'basis': 'cfour-qz2p', 'psi4_freeze_core': True}, marks=using_psi4),
])
def test_sp_hf_rhf_fc(mtd, opts, h2o):
    """cfour/???/input.dat
    #! single point MP2/qz2p on water

    """
    h2o = qcdb.set_molecule(h2o)
    qcdb.set_options(opts)

    e, jrec = qcdb.energy(mtd, return_wfn=True, molecule=h2o)

    # from cfour
    scftot = -76.062748460117
    mp2tot = -76.307900312177
    mp2corl = mp2tot - scftot
    atol = 5.e-5

    assert compare_values(mp2tot, e, tnm() + ' Returned', atol=atol)
    assert compare_values(mp2tot, qcdb.variable('current energy'), tnm() + ' Current', atol=atol)
    assert compare_values(mp2tot, qcdb.variable('mp2 total energy'), tnm() + ' MP2', atol=atol)
                                                                                               
    assert compare_values(mp2corl, qcdb.variable('current correlation energy'), tnm() + ' MP2 Corl', atol=atol)
    assert compare_values(mp2corl, qcdb.variable('mp2 correlation energy'), tnm() + ' MP2 Corl', atol=atol)

    assert compare_values(scftot, qcdb.variable('hf total energy'), tnm() + ' SCF', atol=atol)
    assert compare_values(scftot, qcdb.variable('scf total energy'), tnm() + ' SCF', atol=atol)





@pytest.mark.parametrize('mtd,opts', [
    pytest.param('c4-mp2', {'cfour_basis': 'qz2p', 'cfour_reference': 'uhf', 'cfour_scf_conv': 12}, marks=using_cfour),
    pytest.param('c4-mp2', {'basis': 'cfour-qz2p', 'cfour_reference': 'uhf', 'cfour_scf_conv': 12}, marks=using_cfour),
    pytest.param('gms-mp2', {'basis': 'cfour-qz2p', 'gamess_contrl__scftyp': 'uhf', 'gamess_mp2__nacore': 0}, marks=using_gamess),
    pytest.param('nwc-mp2', {'basis': 'cfour-qz2p', 'qc_module': 'tce', 'nwchem_scf__uhf': True}, marks=using_nwchem),
    pytest.param('nwc-mp2', {'basis': 'cfour-qz2p', 'nwchem_scf__uhf': True}, marks=using_nwchem),
    pytest.param('p4-mp2', {'basis': 'cfour-qz2p', 'reference': 'uhf'}, marks=using_psi4),
])
def test_sp_hf_uhf_full(mtd, opts, nh2):
    """cfour/???/input.dat
    #! single point MP2/qz2p on water

    """
    nh2 = qcdb.set_molecule(nh2)
    qcdb.set_options(opts)

    e, jrec = qcdb.energy(mtd, return_wfn=True, molecule=nh2)

    # from cfour
    scftot = -55.5893469688
    mp2tot = -55.784877360093
    mp2corl = mp2tot - scftot
    atol = 5.e-5

    assert compare_values(mp2tot, e, tnm() + ' Returned', atol=atol)
    assert compare_values(mp2tot, qcdb.variable('current energy'), tnm() + ' Current', atol=atol)
    assert compare_values(mp2tot, qcdb.variable('mp2 total energy'), tnm() + ' MP2', atol=atol)
                                                                                               
    assert compare_values(mp2corl, qcdb.variable('current correlation energy'), tnm() + ' MP2 Corl', atol=atol)
    assert compare_values(mp2corl, qcdb.variable('mp2 correlation energy'), tnm() + ' MP2 Corl', atol=atol)

    assert compare_values(scftot, qcdb.variable('hf total energy'), tnm() + ' SCF', atol=atol)
    assert compare_values(scftot, qcdb.variable('scf total energy'), tnm() + ' SCF', atol=atol)



@pytest.mark.parametrize('mtd,opts', [
    pytest.param('c4-mp2', {'cfour_basis': 'qz2p', 'cfour_reference': 'uhf', 'cfour_dropmo': [1], 'cfour_scf_conv': 12}, marks=using_cfour),
    pytest.param('c4-mp2', {'basis': 'cfour-qz2p', 'cfour_reference': 'uhf', 'cfour_dropmo': 1, 'cfour_scf_conv': 12}, marks=using_cfour),
    pytest.param('gms-mp2', {'basis': 'cfour-qz2p', 'gamess_contrl__scftyp': 'uhf', 'nwchem_mp2__freeze': 1}, marks=using_gamess),
    pytest.param('nwc-mp2', {'basis': 'cfour-qz2p', 'qc_module': 'tce', 'nwchem_tce__freeze': 1, 'nwchem_scf__uhf': True}, marks=using_nwchem),
    pytest.param('nwc-mp2', {'basis': 'cfour-qz2p', 'nwchem_scf__uhf': True, 'nwchem_mp2__freeze': 1}, marks=using_nwchem),
    pytest.param('p4-mp2', {'basis': 'cfour-qz2p', 'reference': 'uhf', 'psi4_freeze_core': True}, marks=using_psi4),
])
def test_sp_hf_uhf_fc(mtd, opts, nh2):
    """cfour/???/input.dat
    #! single point MP2/qz2p on water

    """
    nh2 = qcdb.set_molecule(nh2)
    qcdb.set_options(opts)

    e, jrec = qcdb.energy(mtd, return_wfn=True, molecule=nh2)

    # from cfour
    scftot = -55.5893469688
    mp2tot = -55.760531091893
    mp2corl = mp2tot - scftot
    atol = 5.e-5

    assert compare_values(mp2tot, e, tnm() + ' Returned', atol=atol)
    assert compare_values(mp2tot, qcdb.variable('current energy'), tnm() + ' Current', atol=atol)
    assert compare_values(mp2tot, qcdb.variable('mp2 total energy'), tnm() + ' MP2', atol=atol)
                                                                                               
    assert compare_values(mp2corl, qcdb.variable('current correlation energy'), tnm() + ' MP2 Corl', atol=atol)
    assert compare_values(mp2corl, qcdb.variable('mp2 correlation energy'), tnm() + ' MP2 Corl', atol=atol)

    assert compare_values(scftot, qcdb.variable('hf total energy'), tnm() + ' SCF', atol=atol)
    assert compare_values(scftot, qcdb.variable('scf total energy'), tnm() + ' SCF', atol=atol)




@pytest.mark.parametrize('mtd,opts', [
    pytest.param('c4-mp2', {'cfour_basis': 'qz2p', 'cfour_reference': 'rohf', 'cfour_scf_conv': 12}, marks=using_cfour),
    pytest.param('c4-mp2', {'basis': 'cfour-qz2p', 'cfour_reference': 'rohf', 'cfour_scf_conv': 12}, marks=using_cfour),
    pytest.param('gms-mp2', {'basis': 'cfour-qz2p', 'gamess_contrl__scftyp': 'rohf', 'gamess_mp2__nacore': 0, 'gamess_mp2__nbcore': 0}, marks=using_gamess),
    pytest.param('nwc-mp2', {'basis': 'cfour-qz2p', 'qc_module': 'tce', 'nwchem_scf__rohf': True}, marks=using_nwchem),
    ##pytest.param('nwc-mp2', {'basis': 'cfour-qz2p', 'nwchem_scf__rohf': True}, marks=using_nwchem), # not possible
    #pytest.param('p4-ccsd', {'basis': 'cfour-qz2p', 'reference': 'rohf'}, marks=using_psi4),
])
def test_sp_hf_rohf_full(mtd, opts, nh2):
    """cfour/???/input.dat
    #! single point MP2/qz2p on water

    """
    nh2 = qcdb.set_molecule(nh2)
    qcdb.set_options(opts)

    e, jrec = qcdb.energy(mtd, return_wfn=True, molecule=nh2)

    # from cfour
    scftot = -55.5847372601
    mp2tot = -55.785276787341
    mp2corl = mp2tot - scftot
    atol = 5.e-5

    if mtd.startswith('gms') or mtd.startswith('nwc'):
        atol = 5.e-2 # GAMESS uses ZAPT for ROHF. Is that different from MBPT?

    assert compare_values(mp2tot, e, tnm() + ' Returned', atol=atol)
    assert compare_values(mp2tot, qcdb.variable('current energy'), tnm() + ' Current', atol=atol)
    assert compare_values(mp2tot, qcdb.variable('mp2 total energy'), tnm() + ' MP2', atol=atol)
                                                                                               
    assert compare_values(mp2corl, qcdb.variable('current correlation energy'), tnm() + ' MP2 Corl', atol=atol)
    assert compare_values(mp2corl, qcdb.variable('mp2 correlation energy'), tnm() + ' MP2 Corl', atol=atol)

    assert compare_values(scftot, qcdb.variable('hf total energy'), tnm() + ' SCF', atol=atol)
    assert compare_values(scftot, qcdb.variable('scf total energy'), tnm() + ' SCF', atol=atol)



@pytest.mark.parametrize('mtd,opts', [
    pytest.param('c4-mp2', {'cfour_basis': 'qz2p', 'cfour_reference': 'rohf', 'cfour_dropmo': [1], 'cfour_scf_conv': 12}, marks=using_cfour),
    pytest.param('c4-mp2', {'basis': 'cfour-qz2p', 'cfour_reference': 'rohf', 'cfour_dropmo': 1, 'cfour_scf_conv': 12}, marks=using_cfour),
    pytest.param('gms-mp2', {'basis': 'cfour-qz2p', 'gamess_contrl__scftyp': 'rohf', 'nwchem_mp2__freeze': 1}, marks=using_gamess),
    pytest.param('nwc-mp2', {'basis': 'cfour-qz2p', 'qc_module': 'tce', 'nwchem_tce__freeze': 1, 'nwchem_scf__rohf': True}, marks=using_nwchem),
    #pytest.param('nwc-mp2', {'basis': 'cfour-qz2p', 'nwchem_scf__rohf': True, 'nwchem_mp2__freeze': 1}, marks=using_nwchem),
    #pytest.param('p4-mp2', {'basis': 'cfour-qz2p', 'reference': 'rohf', 'psi4_freeze_core': True}, marks=using_psi4),
])
def test_sp_hf_uhf_fc(mtd, opts, nh2):
    """cfour/???/input.dat
    #! single point MP2/qz2p on water

    """
    nh2 = qcdb.set_molecule(nh2)
    qcdb.set_options(opts)

    e, jrec = qcdb.energy(mtd, return_wfn=True, molecule=nh2)

    # from cfour
    scftot = -55.5847372601
    mp2tot = -55.760853566660764
    mp2corl = mp2tot - scftot
    atol = 5.e-5
    if mtd.startswith('gms') or mtd.startswith('nwc'):
        atol = 5.e-2 # GAMESS uses ZAPT for ROHF. Is that different from MBPT?

    assert compare_values(mp2tot, e, tnm() + ' Returned', atol=atol)
    assert compare_values(mp2tot, qcdb.variable('current energy'), tnm() + ' Current', atol=atol)
    assert compare_values(mp2tot, qcdb.variable('mp2 total energy'), tnm() + ' MP2', atol=atol)
                                                                                               
    assert compare_values(mp2corl, qcdb.variable('current correlation energy'), tnm() + ' MP2 Corl', atol=atol)
    assert compare_values(mp2corl, qcdb.variable('mp2 correlation energy'), tnm() + ' MP2 Corl', atol=atol)

    assert compare_values(scftot, qcdb.variable('hf total energy'), tnm() + ' SCF', atol=atol)
    assert compare_values(scftot, qcdb.variable('scf total energy'), tnm() + ' SCF', atol=atol)




