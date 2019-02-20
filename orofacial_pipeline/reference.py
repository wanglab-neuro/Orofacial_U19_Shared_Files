import datajoint as dj

schema = dj.schema(dj.config.get('database.prefix', '') + 'reference')


@schema
class CellType(dj.Lookup):
    definition = """
    cell_type  : varchar(12)
    """
    contents = zip(['pyramidal', 'FS'])


@schema
class SpikeSortingMethod(dj.Lookup):
    definition = """
    spike_sort_method           : varchar(12)           # spike sort short name
    ---
    spike_sort_description      : varchar(1024)
    """
    #contents = [('default', 'spyking_circus')] # waveform shape ChR tagging and collision test
