# A rough scheduler for running validation tests

import importlib

import util.variables

# A non-smart way to just go and run what's in the validations dict
# First step to improvement will be to use the multiprocessing bits
# for parallelism
def run():

    # This will be created at run time when the config files are parsed
    validations = { 
                 "Example Validator" : 
                    {
                      "Module" : "validation.example.example_validator",
                      "Location" : util.variables.input_dir + "/dome",
                      "DataFiles" : ["dome.0062.p001.nc"],
                      "RunArgs" : ""
                    }
                }
    for val_name, val_conf in validations.iteritems():
        #print val_conf["Module"]
        #m = __import__(val_conf["Module"])
        #import validation.example.example_validator as m
        m = importlib.import_module(val_conf["Module"])
        m.run(val_conf['Location'], val_conf['DataFiles'], val_conf['RunArgs'])

# Who knows what goes here


