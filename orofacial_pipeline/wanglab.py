import datajoint as dj

schema = dj.schema(dj.config.get('database.prefix', '') + 'wanglab')


@schema
class Lab(dj.Manual):
    definition = """ # Lab
    lab : varchar(255)  #  lab conducting the study
    ----
    institution  : varchar(255)  # Institution to which the lab belongs
    """


@schema
class Keyword(dj.Lookup):
    definition = """
    # Tag of study types
    keyword : varchar(24)  
    """
    contents = zip(['behavior', 'extracellular', 'phototagging'])


@schema
class Study(dj.Manual):
    definition = """
    # Study 
    study : varchar(8)    # short name of the study
    --- 
    study_description : varchar(255)   #  
    -> Lab
    """


@schema
class StudyKeyword(dj.Manual):
    definition = """
    # Study keyword (see general/notes)
    -> Study
    -> Keyword
    """


@schema
class Publication(dj.Manual):
    definition = """
    # Publication
    doi  : varchar(60)   # publication DOI
    ----
    full_citation : varchar(4000)
    authors='' : varchar(4000)
    title=''   : varchar(1024)
    """


@schema
class RelatedPublication(dj.Manual):
    definition = """
    -> Study
    -> Publication
    """


@schema
class AnimalSource(dj.Lookup):
    definition = """
    animal_source  : varchar(30) 
    """
    contents = zip(['Jackson Labs', 'Allen Institute', 'Charles River', 'MMRRC', 'Taconic', 'Lab-made', 'Other'])


@schema
class Strains(dj.Lookup):
    definition = """  # Mouse strain
    strain  : varchar(30)  # mouse strain    
    """
    contents = zip(['C57BL6', 'Ai14', 'Ai32', 'Ai35', 'Ai65D',
                    'Emx1_Cre', 'GAD2_Cre', 'vGLut2_Cre', 'Pv_Cre',
                    'Pv_CreERt2', 'Pv_CreN', 'TrpV1_Cre', 'Netrin_G1_Cre',
                    'FosTVA', 'Rphi_AP', 'Rphi_tomato', 'Rphi_GFP',
                    'ChodlPLAP', 'Unspecified'])


@schema
class VectorSources(dj.Lookup):
    definition = """
    virus_source   : varchar(60)
    """
    contents = zip(['Janelia', 'UPenn', 'Addgene', 'UNC', 'Other'])


@schema
class VectorTypes(dj.Manual):
    definition = """
    vector_type   : varchar(60)
    """
    contents = zip(['Dextran', 'CTb', 'AAV', 'AAV2', 'AAV2_1',
                    'AAV2_5', 'AAV2_8', 'AAV8', 'AAV2_9', 'AAV9', 'AAV',
                    'retroAAV', 'LV', 'FuGB2_LV', 'RG_LV', 'CANE_LV',
                    'EnVA_SAD_dG_RV', 'RG_CVS_N2cdG_RV', 'CANE_RV', 
                    'KainicAcid','Other'])


@schema
class Constructs(dj.Lookup):
    definition = """  # payload
    construct  : varchar(60)  # type of construct that the vector carries    
    """
    contents = zip(['Alexa568', 'TMR', 'GFP', 'EGFP', 'mNeonG',
                    'tdTomato', 'mCherry', 'RFP', 'Cre', 'Syn_Cre', 'CreC',
                    'EF1a_mCherry_IRES_WGA_Cre', 'EF1a_Flex_ChR2',
                    'Flex_TVAmCherry', 'Flex_TVA_RG_GFP','Other','None'])


@schema
class User(dj.Lookup):
    definition = """
    # User (lab member)
    user_name  : varchar(24) #  database user name
    ----
    full_name = ''  : varchar(60)
    """


@schema
class Vectors(dj.Lookup):
    definition = """
    vector_id : int unsigned
    ---
    -> VectorSources 
    -> VectorTypes
    -> Constructs
    -> User
    titer           : Decimal(20,1) # 
    order_date      : date
    remarks         : varchar(256)
    """

    class Notes(dj.Part):
        definition = """
        # Notes about the vector
        -> Vectors
        note_id     : int
        ---
        note        : varchar(256)
        """


@schema
class Rig(dj.Lookup):
    definition = """
    # Rig (experimental setup)
    rig_name  : varchar(30)   # experimental rig. E.g., in_vivo_ephys_1
    ----
    recording_system = '' : varchar(30) # e.g., Blackrock (very imnportant to determine AD V/bits)
    location = '' : varchar(20) # e.g., 318
    rig_description = ''  : varchar(1024) #
    """

@schema
class Subject(dj.Manual):
    definition = """
    subject_id  : int   # institution animal ID  
    --- 
    -> [nullable] User        # person responsible for the animal
    species        : varchar(30)
    date_of_birth=null : date  # YYYY-MM-DD optional  
    sex='U' : enum('M', 'F', 'U')   #
    cage_card=null : int # cage card optional
    location       : varchar(30) # e.g., 009_colony
    project_use    : varchar(255)
    -> [nullable] AnimalSource # where was the animal ordered from
    """

    class Strain(dj.Part):
        definition = """
        -> Subject
        -> Strains
        ---
        zygosity = 'Unknown' : enum('Het', 'Hom', 'Unknown')
        type = 'Unknown'     : enum('Knock-in', 'Transgene', 'Unknown')
        """

@schema
class WaterRestriction(dj.Manual):
    definition = """
    -> Subject
    ---
    wr_start_date               : date
    wr_start_weight             : Decimal(6,3)
    wr_threshold_weight         : Decimal(6,3)
    """


@schema
class TargetRegion(dj.Manual):
    definition = """
    brain_region: varchar(32)
    ---
    description = null : varchar (4000) # describes brain region
    """
    #contents = zip(['PrV', 'FN', 'VPM', 'PO', 'WhiskerPad', 'Tongue', 'Masster', 'SpVi',
    # 'SpVir', 'S1', 'S2', 'Barrel', 'PPC', 'V1', 'CeA', 'BNST', 'ovBNST', 'PreLimbCx',
    # 'InfLimbCx', 'CingCx', 'M1', 'NAc', 'CPu', 'InsCx', 'PMCo', 'PLCo',
    # 'TeA', 'EctCx', 'PFCx', 'EntCx', 'SubTh', 'MBTh', 'MDTh', 'PAG', 'PBN',
    # 'RT', 'SolT', 'Cerebellum', 'SC', 'XII', 'brainstem','vIRt', 'other', 'sham'])


@schema
class SkullReference(dj.Lookup):
    definition = """
    skull_reference   : varchar(60)
    """
    contents = zip(['Bregma', 'Lambda','InkMark','Other'])

@schema
class Hemisphere(dj.Lookup):
    definition = """
    hemisphere: varchar(32)
    """
    contents = zip(['left', 'right', 'both'])

@schema
class Surgery(dj.Manual):
    definition = """
    -> Subject
    surgery_id          : int      # surgery number
    ---
    -> User
    start_time          : datetime # start time
    end_time            : datetime # end time
    surgery_description : varchar(256)
    """
    class InjectionParameters(dj.Part):
        definition = """
        # injections
        -> master
        injection_id : int
        ---
        -> Vectors
        -> SkullReference
        ml_location     : Decimal(8,3) # um from ref left is positive 
        ap_location     : Decimal(8,3) # um from ref anterior is positive
        dv_location     : Decimal(8,3) # um from dura dorsal is positive 
        volume          : Decimal(10,3) # in nl
        dilution        : Decimal (10, 2) # 1 to how much
        description     : varchar(256)
        """

    class Procedure(dj.Part):
        definition = """
        # Other procedures than injection
        -> master
        procedure_id : int
        ---
        -> SkullReference
        ml_location=null     : Decimal(8,3) # um from ref left is positive
        ap_location=null     : Decimal(8,3) # um from ref anterior is positive
        dv_location=null     : Decimal(8,3) # um from dura dorsal is positive 
        surgery_procedure_description     : varchar(1000)
        """


@schema
class SurgeryLocation(dj.Manual):
    definition = """ # For surgeries that are not injections
    -> Surgery.Procedure
    ---
    -> Hemisphere
    -> TargetRegion 
    """


@schema
class ProbeType(dj.Lookup):
    definition = """
    probe_type: varchar(32)    
    """
    contents = zip(['silicon_probe', 'tetrode_array', 'neuropixel','single_electrode'])


@schema
class Probe(dj.Lookup):
    definition = """ # Description of a particular model of probe.
    probe_name: varchar(128)  # String naming probe model
    ---
    -> ProbeType
    channel_counts: tinyint  # number of channels in the probe
    shank_counts: tinyint    # number of shanks in the probe
    probe_comment='' :  varchar(1000)
    """

    class Electrode(dj.Part):
        definition = """
        -> master
        electrode : int   # electrode on probe
        shank_id: tinyint  # the shank id of this probe this channel is located on 
        ---
        x_coord=NULL: float   # (um) x coordinate of the electrode within the probe
        y_coord=NULL: float   # (um) y coordinate of the electrode within the probe
        z_coord=NULL: float   # (um) z coordinate of the electrode within the probe
        """


@schema
class ElectrodeConfig(dj.Lookup):
    definition = """
    -> Probe
    electrode_config_name: varchar(16)  # user friendly name
    ---
    electrode_config_hash: varchar(36)  # hash of the group and group_member (ensure uniqueness)
    unique index (electrode_config_hash)
    """

    class ElectrodeGroup(dj.Part):
        definition = """
        # grouping of electrodes to be clustered together (e.g. a neuropixel electrode config - 384/960)
        -> master
        electrode_group: int  # electrode group
        """

    class Electrode(dj.Part):
        definition = """
        -> master.ElectrodeGroup
        -> Probe.Electrode
        """

@schema
class PhotoStimDevice(dj.Manual):
    definition = """ # Change it to a lookup table
    photo_stim_device  : varchar(20)
    ---
    excitation_wavelength :  decimal(5,1)  # (nm) 
    photostim_device_description : varchar(255)
    """

@schema
class ElecStimDevice(dj.Manual):
    definition = """ # For all devices passing current
    electrical_stim_device  : varchar(20)
    ---
    electrical_stim_device_description : varchar(255)
    """
