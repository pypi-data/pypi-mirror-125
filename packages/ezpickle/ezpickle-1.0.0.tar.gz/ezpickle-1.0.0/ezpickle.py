"""
Helper functions to simplify pickling and unpickling objects to/from files.
    - pickle_data() : simplify the process of pickling an object (such as a dictionary) and writing it to a file
    - unpickle_data() : load a pickled object from a file

    
Releases:
1.0
    2021-10-26, J. Burnett
    * Initial release
"""

from __future__ import annotations

from pathlib import Path
import pickle
from typing import Iterable


__version__ = '1.0.0'


#%% Save & retrieve pickled data
def pickle_data(data, filepath: Path | str, overwrite: bool = False):
    filepath = Path(filepath)  # ensure we have a Path object, not just a string

    # Add default extension if none specified
    if not filepath.suffix:
        filepath = filepath.parent / (filepath.name + '.pkl')

    if not filepath.exists() or overwrite:
        with open(filepath, 'wb') as data_file:
            pickle.dump(data, data_file)
    else:
        raise FileExistsError(f'File already exists: {filepath}')


def unpickle_data(filepath: Path | str, dict_keys: str | Iterable | None = None):
    with open(filepath, 'rb') as data_file:
        data = pickle.load(data_file)

    if dict_keys is None:
        # No keys specified: return all data in original format
        return data
    elif type(dict_keys) == str:
        # Single string specified: return just the value associated with this key
        return data[dict_keys]
    else:
        # Return list of values associated with list of keys or indices
        return [data[key] for key in dict_keys]
