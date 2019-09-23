import datajoint as dj
from . import wanglab as lab # this has to be done locally (or add remote location to python path)
from . import reference # same

schema = dj.schema(dj.config.get('database.prefix', '') + 'wl_whisker_experiment')

@schema
class Session(dj.Manual):
    definition = """
    -> lab.Subject
    session  : int   # session within 
    --- 
    -> lab.Study
    session_date       : date         # session date
    -> lab.User
    -> lab.Rig 
    session_suffix='': char(2)         # suffix used by experimenter when identifying session by date
    session_notes='' : varchar(4000)   # free-text notes
    session_folder='': varchar(255)    # path to session data for data import
    recording_type  : varchar(20)   # e.g. acute   
    """

@schema
class CueType(dj.Lookup):
    definition = """
    -> Session
    cue_type : varchar(20)  
    """
    contents = zip(['cuetip', 'whiskerstim', 'piezo_deflection',
                    'touch_panel', 'pole', 'start', 'response',
                    'visual_cue','audio_cue'])


@schema
class WhiskerBehavior(dj.Imported):
    definition = """
    -> Session
    ---
    angle         : longblob   # (degrees)
    amplitude     : longblob   # (degrees)
    midpoint      : longblob   # (degrees)
    phase         : longblob   # (radians)   
    velocity      : longblob   # (degrees/s)
    frame_times   : longblob   # (s)
    """

    #retract_times   : longblob  # (s)    
    #protract_times  : longblob  # (s)

@schema
class BrainLocation(dj.Manual):
    definition = """
    brain_location_name: varchar(32)  # unique name of this brain location (could be hash of the non-primary attr)
    ---
    -> lab.TargetRegion
    -> lab.Hemisphere
    -> lab.SkullReference
    """


@schema
class Task(dj.Manual):
    definition = """
    # Type of tasks
    task            : varchar(12)                  # task type
    ----
    task_description : varchar(4000)
    """


@schema
class TaskProtocol(dj.Manual):
    definition = """
    # SessionType
    -> Task
    task_protocol : tinyint # task protocol
    ---
    task_protocol_description : varchar(4000)
    """


@schema
class PhotoStim(dj.Manual):
    definition = """
    -> Session
    photo_stim :  smallint 
    ---
    -> lab.PhotostimDevice
    -> BrainLocation
    ml_location=null: float # um from ref ; right is positive; based on manipulator coordinates/reconstructed track
    ap_location=null: float # um from ref; anterior is positive; based on manipulator coordinates/reconstructed track
    dv_location=null: float # um from dura; ventral is positive; based on manipulator coordinates/reconstructed track
    ml_angle=null: float # Angle between the manipulator/reconstructed track and the Medio-Lateral axis. A tilt towards the right hemishpere is positive.
    ap_angle=null: float # Angle between the manipulator/reconstructed track and the Anterior-Posterior axis. An anterior tilt is positive.
    """

    class PhotoStimParam(dj.Part):
        definition = """  # Optogenetic stimulation parameters
        -> master
        ---
        pulse_duration=null:  decimal(8,4)   # (s)
        pulse_frequency : decimal(6,3) # Hz
        pulse_per_train : smallint #
        waveform=null:  longblob       # normalized to maximal power. The value of the maximal power is specified for each PhotostimTrialEvent individually
        """

@schema
class ElectricalStim(dj.Manual):
    definition = """
    -> Session
    elec_stim :  smallint 
    ---
    -> lab.ElecStimDevice
    -> BrainLocation
    ml_location=null: float # um from ref ; right is positive; based on manipulator coordinates/reconstructed track
    ap_location=null: float # um from ref; anterior is positive; based on manipulator coordinates/reconstructed track
    dv_location=null: float # um from dura; ventral is positive; based on manipulator coordinates/reconstructed track
    ml_angle=null: float # Angle between the manipulator/reconstructed track and the Medio-Lateral axis. A tilt towards the right hemishpere is positive.
    ap_angle=null: float # Angle between the manipulator/reconstructed track and the Anterior-Posterior axis. An anterior tilt is positive.
    """

    class ElecStimParam(dj.Part):
        definition = """  # Electrical stimulation parameters
        -> master
        ---
        pulse_duration=null:  decimal(8,4)   # (s)
        pulse_frequency : decimal(6,3) # Hz
        pulse_per_train : smallint #
        waveform=null:  longblob       # normalized to maximal power. The value of the maximal power is specified for each PhotostimTrialEvent individually
        """

@schema
class SessionTrial(dj.Imported):
    definition = """
    -> Session
    trial : smallint        # trial number
    ---
    trial_uid : int  # unique across sessions/animals
    start_time : decimal(8, 4)  # (s) relative to session beginning 
    stop_time : decimal(8, 4)  # (s) relative to session beginning 
    trial_type=null : varchar(12)
    """
        

@schema 
class TrialNoteType(dj.Lookup):
    definition = """
    trial_note_type : varchar(12)
    """
    contents = zip(('autolearn', 'protocol #', 'bad', 'bitcode'))


@schema
class TrialNote(dj.Imported):
    definition = """
    -> SessionTrial
    -> TrialNoteType
    ---
    trial_note  : varchar(255) 
    """


@schema
class TrainingType(dj.Manual):
    definition = """
    # Mouse training
    training_type : varchar(100) # mouse training
    ---
    training_type_description : varchar(2000) # description
    """


@schema
class SessionTraining(dj.Manual):
    definition = """
    -> Session
    -> TrainingType
    """


@schema
class SessionTask(dj.Manual):
    definition = """
    -> Session
    -> TaskProtocol
    """


@schema
class SessionComment(dj.Manual):
    definition = """
    -> Session
    session_comment : varchar(767)
    """


@schema
class Period(dj.Lookup):
    definition = """
    period: varchar(12)
    ---
    period_start: float  # (s) start of this period relative to event
    period_end: float    # (s) end of this period relative to event
    """
    contents = [('sample', -2.4, -1.2),
                ('delay', -1.2, 0.0),
                ('response', 0.0, 1.2),
                ('prestim', -0.5, 0.0),
                ('poststim', 0.0, 0.5)]


# ---- behavioral trials ----

@schema
class TrialInstruction(dj.Lookup):
    definition = """
    # Instruction to mouse or type of trial
    trial_instruction  : varchar(8) 
    """
    contents = zip(('left', 'right',
                    'go', 'nogo','other',
                    'far','near',
                    'rough','smooth','neutral'))

 
@schema
class Outcome(dj.Lookup):
    definition = """
    outcome : varchar(32)
    """
    contents = zip(('hit', 'miss', 'false alarm', 'correct rejection',
     'grasp', 'fail', 'drop', 'wipe', 'groom', 'lick', 'ignore'))


@schema
class EarlyResponse(dj.Lookup):
    definition = """
    early_response  :  varchar(32)
    ---
    early_response_description : varchar(4000)
    """
    contents = [
        ('early', 'early response during sample and/or delay'),
        ('early, presample only', 'early response in the presample period, after the onset of the scheduled wave but before the sample period'),
        ('no early', '')]


@schema
class BehaviorTrial(dj.Imported):
    definition = """
    -> SessionTrial
    ----
    -> TaskProtocol
    -> TrialInstruction
    -> EarlyResponse
    -> Outcome
    """


@schema
class TrialEventType(dj.Lookup):
    definition = """
    trial_event_type  : varchar(12)  
    """
    contents = zip(('delay', 'go', 'sample', 'stim', 'presample', 'trialend'))


@schema
class TrialEvent(dj.Imported):
    definition = """
    -> BehaviorTrial 
    trial_event_id: smallint
    ---
    -> TrialEventType
    -> CueType 
    trial_event_time : decimal(8, 4)   # (s) from trial start, not session start
    duration : decimal(8,4)  #  (s)  
    """


@schema
class ActionEventType(dj.Lookup):
    definition = """
    action_event_type : varchar(32)
    ----
    action_event_description : varchar(1000)
    """
    contents =[  
       ('left lick', ''), 
       ('right lick', ''),
       ('protraction', 'whisker protraction phase begins'),
       ('retraction', 'whisker retraction phase begins'),
       ('stick slip', 'stick slip events'),
       ('whisker pump', 'at start of pump protraction'),
       ('whisker touch', 'all other types of touch events'),
       ('cross', 'gap crossing begins'),
       ('face grooming start', ''),
       ('face grooming end', '')
       ]


@schema
class ActionEvent(dj.Imported):
    definition = """
    -> BehaviorTrial
    action_event_id: smallint
    ---
    -> ActionEventType
    action_event_time : decimal(8,4)  # (s) from trial start
    """

# ---- Photostim trials ----

@schema
class PhotostimTrial(dj.Imported):
    definition = """
    -> SessionTrial
    """


@schema
class PhotostimEvent(dj.Imported):
    definition = """
    -> PhotostimTrial
    photostim_event_id: smallint
    ---
    -> PhotoStim
    photostim_event_time : decimal(8,3)   # (s) from trial start
    power : decimal(8,3)   # Maximal power (mW)
    """

# ---- Electrical stim trials ----

@schema
class ElectricalStimTrial(dj.Imported):
    definition = """
    -> SessionTrial
    """


@schema
class ElectricalStimTrialEvent(dj.Imported):
    definition = """
    -> ElectricalStimTrial
    elecstim_event_id: smallint
    ---
    -> ElectricalStim
    elecstim_event_time : decimal(8,3)   # (s) from trial start
    current : decimal(6,4)   # Maximal power (uA)
    """


