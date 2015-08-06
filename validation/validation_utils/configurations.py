
import util.variables

def parse_configs():
    """ This will parse a configuration file for validation testing """
    if util.variables.validation == "False": return dict()
    print("Validation configuration parser activated.")
    return dict()

