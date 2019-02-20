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
    reference_atlas : varchar(255)   # e.g. "paxinos"
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
    contents = zip(['JAX', 'LabMade', 'Other'])


@schema
class Strain(dj.Lookup):
    definition = """  # Mouse strain
    strain  : varchar(30)  # mouse strain    
    """
    contents = zip(['C57BL6', 'Ai14', 'Ai32', 'Ai35', 'Ai65D',
                    'Emx1_Cre', 'GAD2_Cre', 'vGLut2_Cre', 'Pv_Cre',
                    'Pv_CreERt2', 'Pv_CreN', 'TrpV1_Cre', 'Netrin_G1_Cre',
                    'FosTVA', 'Rphi_AP', 'Rphi_tomato', 'Rphi_GFP', 'ChodlPLAP'])


@schema
class Vectors(dj.Lookup):
    definition = """  # vector type
    vector  : varchar(30)  # type of compound to inject    
    """
    contents = zip(['Dextran', 'CTb', 'AAV', 'AAV2', 'AAV2_1',
                    'AAV2_5', 'AAV2_8', 'AAV8', 'AAV2_9', 'AAV9', 'AAV',
                    'retroAAV', 'LV', 'FuGB2_LV', 'RG_LV', 'CANE_LV',
                    'EnVA_SAD_dG_RV', 'RG_CVS_N2cdG_RV', 'CANE_RV', 'KainicAcid'])


@schema
class Construct(dj.Lookup):
    definition = """  # payload
    construct  : varchar(60)  # type of construct that the vector carries    
    """
    contents = zip(['Alexa568', 'TMR', 'GFP', 'EGFP', 'mNeonG',
                    'tdTomato', 'mCherry', 'RFP', 'Cre', 'Syn_Cre', 'CreC',
                    'EF1a_mCherry_IRES_WGA_Cre', 'EF1a_Flex_ChR2',
                    'Flex_TVAmCherry', 'Flex_TVA_RG_GFP'])


@schema
class User(dj.Lookup):
    definition = """
    # User (lab member)
    username  : varchar(16) #  database username
    ----
    full_name = ''  : varchar(60)
    """


@schema
class Rig(dj.Lookup):
    definition = """
    # Rig (experimental setup)
    rig_name  : varchar(30)   # experimental rig
    ----
    rig_description = ''  : varchar(60) #
    ephys_system = ''  : varchar(30) # e.g., Blackrock
    ephys_ad_bits : tinyint   # A/D converter bits 
    """


@schema
class Subject(dj.Manual):
    definition = """
    subject_id  : int   # institution animal ID  
    --- 
    species        : varchar(30)
    date_of_birth=null : date  # YYYY-MM-DD optional  
    sex='U' : enum('M', 'F', 'U')   #
    cage_card=null : int # cage card optional
    location       : varchar(30) # e.g., 009_colony
    project_use    : varchar(255)
    -> [nullable] AnimalSource
    """

    class Strain(dj.Part):
        definition = """
        -> Subject
        -> Strain
        """


@schema
class Probe(dj.Lookup):
    definition = """ # Description of a particular model of probe.
    probe_name: varchar(128)  # String naming probe model
    channel_counts: tinyint  # number of channels in the probe
    shank_counts: tinyint    # number of shanks in the probe
    """

    class Electrode(dj.Part):
        definition = """
        -> master
        electrode : tinyint   # electrode on probe
        shank_id: tinyint  # the shank id of this probe this channel is located on 
        ---
        electrode_x  : decimal(6,4)  # (mm) electrode map
        electrode_y  : decimal(6,4)  # (mm) electrode map
        electrode_z  : decimal(6,4)  # (mm) electrode map
        """
