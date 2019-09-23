import datajoint as dj

schema = dj.schema(dj.config.get('database.prefix', '') + 'reference')


@schema
class CellType(dj.Lookup):
    definition = """
    #
    cell_type  :  varchar(100)
    ---
    cell_type_description :  varchar(4000)
    """
    contents = [
        ('Pyr', 'putative pyramidal'),
        ('FS', 'fast spiking'),
        ('Proj', 'projection cell'),
        ('not classified', ''),
        ('all', 'all types')
    ]


@schema
class SpikeSortingMethod(dj.Lookup):
    definition = """
    spike_sort_method           : varchar(12)           # spike sort short name
    ---
    spike_sort_description      : varchar(1024)
    """
    contents = [('SC', 'SpykingCircus'),
    ('MS', 'MountainSort'),
    ('JRC', 'JRclust'),
    ('KS', 'KiloSort'),
    ('POS', 'PlexonOfflineSorter'),
    ('KK', 'KlustaKwick'),
    ('MC', 'MClust'),
    ('WC','WaveClus'),
    ('S2','Spike2'),
    ('WS','WaveformTemplate'),
    ('PT','PhotoTagging'),
    ('OM','OtherMethod')
    ] 
