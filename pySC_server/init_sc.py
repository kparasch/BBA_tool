import petra_SC as pSC
from pySC.utils import logging_tools
from pySC.correction.bba import orbit_bba
from pySC.core.beam import bpm_reading
from pySC.correction.orbit_trajectory import correct
from pySC.lattice_properties.response_model import SCgetModelRM
import numpy as np



LOGGER = logging_tools.get_logger(__name__)

def initSC():
    seed = 18
    Pem = pSC.PetraErrorModel()
    p424 = 'p4_H6BA_v4_2_4.mat'
    SC = pSC.register_petra_stuff(p424, Pem)
    pSC.number_of_elements(SC)
    knobs = pSC.PetraKnobs(SC.RING)
    SC.plot = False
    repr_file = f'after_RF_setup_seed{seed}.repr'
    SC.RING = pSC._load_repr(repr_file)
    SC.RING = pSC.fix_apertures(SC.RING)

    SC.INJ.Z0 = np.zeros(6)
    SC.INJ.trackMode = 'ORB'

    bo = 3392
    
    ORM = np.load(f'ORM_ideal.npz')['arr_0']
    SC.ORM = ORM
    SC.knobs = knobs

    mag_ords = np.tile(knobs.bba_sextupoles, (2, 1))
    bpm_ords = np.tile(knobs.bpms_disp_bump, (2, 1))
    quad_is_skew = True

    n_k1_steps = 12
    max_dk1 = 70e-6
    n_k2_steps = 2
    max_dk2 = 1e-2
    return SC

def do_BBA(SC, bpm_index):
    bpm_id = SC.ORD.BPM[bpm_index]

    if bpm_id in SC.knobs.bpms_disp_bump:
        ii = np.where(SC.knobs.bpms_disp_bump == bpm_id)[0][0]
        mag_id = SC.knobs.bba_sextupoles[ii]
        quad_is_skew = True
    else:
        ii = np.where(SC.knobs.bpms_no_disp == bpm_id)[0][0]
        mag_id = SC.knobs.bba_quads[ii]
        quad_is_skew = False
    
    bpm_ords = np.tile(bpm_id, (2, 1))
    mag_ords = np.tile(mag_id, (2, 1))

    n_k1_steps = 5
    max_dk1 = 30e-6
    n_k2_steps = 2
    max_dk2 = 1e-2

    SC.orbits = []
    SC.bps = []
    SC, bba_offsets, bba_offset_errors = orbit_bba(SC, bpm_ords, mag_ords, quad_is_skew,
                                                             n_k1_steps, max_dk1, n_k2_steps, max_dk2, RM=SC.ORM,
                                                             plot_results=False)
    SC.RING[bpm_id].Offset -= bba_offsets[:,0]
    return SC.bps, SC.orbits, bba_offsets, bba_offset_errors
