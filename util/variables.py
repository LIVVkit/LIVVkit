'''
Storage for global variables.  These are set upon startup in the main 
livv.py module

Created on May 5th, 2015
@author arbennett
'''
cwd            = ''
configDir      = ''
inputDir       = ''
benchmarkDir   = ''
performanceDir = ''
outputDir      = ''
imgDir         = ''
comment        = ''
timestamp      = ''
user           = ''
websiteDir     = ''
templateDir    = ''
indexDir       = ''
verification   = ''
performance    = ''
validation     = ''

# Modules that need to be loaded on big machines
modules = []

# A list of the information that should be looked for in the stdout of model output
parserVars = []

# Variables to measure when parsing through timing summaries
timingVars = []

# Dycores to try to parse output for
dycores = []


# Provide a way to update this when loading a configuration
def update(vars):
    globals().update(vars)
