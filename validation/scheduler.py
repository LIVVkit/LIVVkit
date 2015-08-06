# A rough scheduler for running validation tests

import importlib

# A non-smart way to just go and run what's in the validations dict
# First step to improvement will be to use the multiprocessing bits
# for parallelism
def run():

    # This will be created at run time when the config files are parsed
    validations = { 
                 "Example Validator" : 
                    {
                      "Module" : "validation.example.example_validator",
                      "Location" : "/home/bzq/livv-dev/LIVV/reg_test/linux-gnu/higher-order/dome",
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


