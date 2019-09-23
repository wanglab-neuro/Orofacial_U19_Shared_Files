import sys
import os

import datajoint as dj
from . import wanglab as lab
from . import reference

schema = dj.schema(dj.config.get('database.prefix', '') + 'tgvirt')

@schema
class Session(dj.Manual):
    definition = """
    -> lab.Subject
    session  : int   # session within 
    --- 
    -> lab.Study
    session_date       : date         # session date 
    session_suffix='': char(2)         # suffix used by experimenter when identifying session by date
    session_notes='' : varchar(4000)   # free-text notes
    session_folder='': varchar(255)    # path to session data for data import
    recording_type  : varchar(20)   # e.g. acute   
    """


@schema
class CueType(dj.Lookup):
    definition = """
    cue_type : varchar(20)  
    """
    contents = zip(['cuetip', 'whiskerstim', 'piezo_deflection',
                    'touch_panel', 'pole', 'start', 'response'])


@schema
class WhiskerBehavior(dj.Imported):
    definition = """
    -> Session
    ---
    angle         : longblob   # (degrees) deviation
    curve         : longblob   # (radians/mm)   
    frame_times   : longblob   # (s)
    retract_times   : longblob  # (s)    
    protract_times  : longblob  # (s)
    """


@schema
class OptoStim(dj.Manual):
    definition = """  # Optogenetic stimulation information for the sesssion
    -> Session
    -> TargetRegion
    site_number   : tinyint  #  optogenetic site number  
    ---
    description : varchar(255)   # optogenetic site description
    """

    class StimParam(dj.Part):
        definition = """  # Optogenetic stimulation parameters
        -> master
        stim_number   : tinyint  #  optogenetic stim sequence number  
        ---
        stimulation_method  : varchar(255)
        device   : varchar(60)
        location_x  : decimal(4,2)  # mm
        location_y  : decimal(4,2)  # mm
        laser_wavelength : decimal(4,1)  # nm 
        laser_power : decimal(4,1)  # mW
        pulse_duration : smallint # ms
        pulse_frequency : smallint # Hz
        pulse_per_train : smallint #
        """


@schema
class Ephys(dj.Manual):
    definition = """  # Ephys recording for this session
    -> Session
    -> lab.Rig
    -> lab.Probe
    -> TargetRegion
    ---
    # posterior :  decimal(3,2)   # (mm) #useless
    # lateral  :  decimal(3,2)   # (mm) #useless

    recording_marker: varchar(30)  # e.g. "stereotaxic" or "implant"
    # ground_x  : decimal(4,2)   # (mm) #no need for those
    # ground_y  : decimal(4,2)   # (mm)
    # ground_z  : decimal(4,2)   # (mm)
    recording_notes='' : varchar(4000)   # free-text notes 
    """


@schema
class Phototag(dj.Manual):
    definition = """
    -> Ephys
    -> OptoStim
    ---
    responses  : varchar(30)   # Yes / No / MU / SU
    responsive_channels= null : varchar(30)  # responsive channels
    """


@schema
class SpikeSorting(dj.Imported):
    definition = """
    -> Ephys
    -> reference.SpikeSortingMethod
    """


@schema
class Unit(dj.Imported):
    definition = """  #  Resultant unit(s) from spike-sorting routine
    -> SpikeSorting
    unit  : smallint   # single unit number in recording
    ---
    spike_times : longblob  # (s) with respect to the start-time of the Ephys recording session
    """
        
    class CellType(dj.Part):
        definition = """  # cell type of this unit, (potentially multiple types per unit)
        -> master
        ---
        -> reference.CellType
        """
        
    class Waveform(dj.Part):
        definition = """  # spike waveform of this unit manifested at a given electrode
        -> master
        -> lab.Probe.Electrode
        ---
        waveform : longblob   # uV 
        """


@schema
class Trial(dj.Imported):
    definition = """  # Trial within a session
    -> Session
    trial   : smallint   # trial number within session
    ---
    start_time : float   # (s) synchronized
    stop_time  : float   # (s) synchronized
    trial_type : varchar(12)
    """
        
    class Cue(dj.Part):
        definition = """
        -> master
        -> CueType 
        ---
        cue_time  : double                      # synchronized
        """
 
    class Stim(dj.Part):
        definition = """
        -> master
        -> OptoStim 
        ---
        stim_time  : double                      # synchronized
        """
        
    class UnitInTrial(dj.Part):
        definition = """
        -> master 
        -> Unit
        """
