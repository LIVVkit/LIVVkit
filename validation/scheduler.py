# A rough scheduler for running validation tests

import importlib

import util.variables

# A non-smart way to just go and run what's in the validations dict
# First step to improvement will be to use the multiprocessing bits
# for parallelism
def run():
    # This will be created at run time when the config files are parsed
    validations = { 
                 #"Example Validator" : 
                 #   {
                 #     "Module" : "validation.example.example_validator",
                 #     "Location" : util.variables.input_dir + "/dome",
                 #     "DataFiles" : ["dome.0062.p001.nc"],
                 #     "RunArgs" : ""
                 #   }
                  "Ice Sheet Coverage" : 
                    {
                      "Module" : "validation.coverage.coverage",
                      "ModelDir" : util.variables.input_dir + "/gis",
                      "BenchDir" : util.variables.input_dir + "/gis",
                      "ModelData" : "gis.nc",
                      "BenchData" : "gis.nc",
                      "RunArgs" : ""
                    }
                }
    
    # Go through and run the tests
    for val_name, val_conf in validations.iteritems():
        m = importlib.import_module(val_conf["Module"])
        m.run(
                val_conf['ModelDir'], 
                val_conf['BenchDir'], 
                val_conf['ModelData'],
                val_conf['BenchData'],
                val_conf['RunArgs']
              )

# Who knows what goes here


