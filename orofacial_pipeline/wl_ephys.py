import datajoint as dj
from . import wanglab as lab
from . import reference

schema = dj.schema(dj.config.get('database.prefix', '') + 'wl_ephys')


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
