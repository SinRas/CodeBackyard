# Modules
import json

# Parameters

# Methods
## JDump
def jdump( obj, fp, ensure_ascii=False, sort_keys=True, indent=1 ):
    with open(fp, 'w') as out_file:
        json.dump(
            obj, out_file,
            ensure_ascii=ensure_ascii,
            sort_keys=sort_keys,
            indent=indent
        )
    return
## JLoad
def jload( fp ):
    with open(fp, 'r') as in_file:
        result = json.load(in_file)
    return result

# Classes

# Main