# This will actually save the resources that we want to display to the user
import os
import plots.nclfunc

def save(data_dir, data_file, output_dir):
    var = 'thk'
    out_name = 'validation_example.png'
    plots.nclfunc.plot_diff(var, data_dir + os.sep + data_file, data_dir + os.sep + data_file, output_dir + os.sep + out_name)

