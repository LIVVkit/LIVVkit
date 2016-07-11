# This is what an actual validation test may someday look like
# We will probably want to store data inside of here too, but that's later

import util.variables
import validation.validation_utils.example_plot

def run(data_dir, data_files, run_args):
    print("Running example validation on "  + data_files[0])
    output_dir = util.variables.output_dir
    validation.validation_utils.example_plot.save(data_dir, data_files[0], output_dir)    

