# Copyright (c) 2015, UT-BATTELLE, LLC
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Analyze the ice-sheet time series.  For more information check documentation for 
the run() function.

Created on Jan 2, 2016

@author: arbennett, jhkennedy, JeremyFyke
"""

import os
import re
import sys
import glob
import gzip
import pandas
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


from validation.base import AbstractTest
import util.variables

#General function to extract data associated with particular diagnostic
def ExtractTSData(TS,line,ValuePosition):
    #If the string associated with the Series 'name' attribute is matched...
    if re.search(re.escape(TS.name),line):
       #...then extract numerical value from string position...
       ExtractedValue=np.float(line.split()[ValuePosition])
       #...and append to time series object.
       TS=TS.set_value(len(TS),ExtractedValue)
    return TS

#General function to plot output time series.  This plot also contains
#a warning about zero-length time series, which is likely an indication
#of either bad paths/filenames, or a change to the formatting of CISM2
#output.
def WritePlot(Series,SeriesName,CISM2time,pd):
    if Series.empty:
        print ''
        print 'Warning: '+SeriesName+' time series contains no data.'
        print 'You may not be pointing correctly to glc.log.*.gz files,'
        print 'or these files may not contain '+SeriesName+' information.'
        print 'In any case, '+SeriesName+'.png not written.'
    else:
        print 'Plotting: '+SeriesName+' timeseries.'
        plt.close("all")
        ax=plt.plot(CISM2time,Series)
        plt.xlabel('CISM2 Model year')
        plt.ylabel(Series.name)
        Seriesmean=Series.mean()
        Seriesregress=np.polyfit(CISM2time,Series,1)[0]/Seriesmean*100
        plt.annotate( 'Mean='+str(Seriesmean) , xy=(0.1,0.9) , xycoords='axes fraction')
        plt.annotate( 'Linear trend='+str(Seriesregress)+' %/yr' , xy=(0.1,0.8) , xycoords='axes fraction')	
        plt.savefig(os.path.join(pd.output_file_base,SeriesName+'.png'))    


class plotData():
    """
    A class to hold the data to be passed to the plot function.
    """
    pass


class Test(AbstractTest):

    def run(self, *args, **kwargs):
        """
        Runs the analysis of the coverage of the ice sheet over the land mass.
        Produces both an overall coverage percentage metric and a coverage plot.
    
        Required args:
            plot_script:  full path to the ncl script used to plot the data
            model_data: full path to the output from the model data
            bench_data: full path to the output from the benchmark data
        """
        self.description = kwargs.get('description')
       
        pd = plotData()

        # Get the data out of the config file
        pd.log_dir    = kwargs.get('log_dir')
        

        if not os.path.exists(pd.log_dir):
            # Add more handling here -- what do we want to return for failed tests
            print("ERROR: Could not find necessary data to run the time series validation!")
            print(pd.log_dir)
            print("")
            return
    
        # Generate the script
        pd.output_file_base = util.variables.index_dir + os.sep + 'validation' + os.sep + self.name + os.sep + 'imgs'
        self.plot_time_series(pd)
    
    
    def plot_time_series(self, pd):
        """ 
        Performs the time-series analyses and then plots the results.
    
        Args:
             pd: A plotData class instance that holds all the needed analyses and plot data.
    
        Returns:
            TBD
        """
   
        #First: define separate, empty Pandas Series for each time series.
        #The 'name' attribute is used both as a regex to find the relevant
        #output in the log files, and also to label the y-axis of the 
        #resulting plots.
        CISM2time=pandas.Series(name='Diagnostic output, time',dtype=float)
        Area=pandas.Series(name='Total ice area (km^2)',dtype=float)
        Volume=pandas.Series(name='Total ice volume (km^3)',dtype=float)
        Energy=pandas.Series(name='Total ice energy (J)',dtype=float)
        MeanThickness=pandas.Series(name='Mean thickness (m)',dtype=float)
        MeanTemperature=pandas.Series(name='Mean temperature (C)',dtype=float)
        MeanSMB=pandas.Series(name='Mean accum/ablat (m/yr)',dtype=float)
        MeanBasalMelt=pandas.Series(name='Mean basal melt (m/yr)',dtype=float)
        MaxThickness=pandas.Series(name='Max thickness (m)',dtype=float)
        MaxTemperature=pandas.Series(name='Max temperature',dtype=float)
        MinTemperature=pandas.Series(name='Min temperature',dtype=float)
        MaxSurfaceSpeed=pandas.Series(name='Max sfc spd (m/yr)',dtype=float)
        MaxBasalSpeed=pandas.Series(name='Max base spd (m/yr)',dtype=float)

        #Second: for each log file (in order) open using gzip.open (no need
        #to unzip) and send each line to ExtractTSData.  For each diagnostic,
        #if the string associated with the Pandas Series is matched, then
        #the relevant numerical value is found (using hard-coded line.split 
        #count value to extract correct substring associated with numerical 
        #value) and appended to the time series.
        for src_name in glob.glob(os.path.join(pd.log_dir, 'glc.log.*.gz')):
            print 'Reading log file: '+src_name
            base=os.path.basename(src_name)
            with gzip.open(src_name,'rb') as f:
                for line in f:
                    CISM2time=ExtractTSData(CISM2time,line,5)
                    Area=ExtractTSData(Area,line,5)
                    Volume=ExtractTSData(Volume,line,5)
                    Energy=ExtractTSData(Energy,line,5)
                    MeanThickness=ExtractTSData(MeanThickness,line,4)
                    MeanTemperature=ExtractTSData(MeanTemperature,line,4)
                    MeanSMB=ExtractTSData(MeanSMB,line,4)
                    MeanBasalMelt=ExtractTSData(MeanBasalMelt,line,5)
                    MaxThickness=ExtractTSData(MaxThickness,line,6)	
                    MaxTemperature=ExtractTSData(MaxTemperature,line,6)
                    MinTemperature=ExtractTSData(MinTemperature,line,6)	
                    MaxSurfaceSpeed=ExtractTSData(MaxSurfaceSpeed,line,7)
                    MaxBasalSpeed=ExtractTSData(MaxBasalSpeed,line,7)	    

        #Third: generate time series plots, including minimal statistics,
        #for each diagnostic.
        WritePlot(Area,'Area',CISM2time,pd)
        WritePlot(Volume,'Volume',CISM2time,pd)
        WritePlot(Energy,'Energy',CISM2time,pd)
        WritePlot(MeanThickness,'MeanThickness',CISM2time,pd)
        WritePlot(MeanTemperature,'MeanTemperature',CISM2time,pd)
        WritePlot(MeanSMB,'MeanSMB',CISM2time,pd)
        WritePlot(MeanBasalMelt,'MeanBasalMelt',CISM2time,pd)
        WritePlot(MaxThickness,'MaxThickness',CISM2time,pd)
        WritePlot(MaxTemperature,'MaxTemperature',CISM2time,pd)
        WritePlot(MinTemperature,'MinTemperature',CISM2time,pd)
        WritePlot(MaxSurfaceSpeed,'MaxSurfaceSpeed',CISM2time,pd)
        WritePlot(MaxBasalSpeed,'MaxBasalSpeed',CISM2time,pd)


        #FIXME: Need better error check here!
        #if not os.path.exists(output_file_base):
        #    print("****************************************************************************")
        #    print("*** Error saving "+output_file_base)
        #    print("*** Details of the error follow: ")
        #    print("")
        #    print(stdOut)
        #    print(stdErr)
        #    print("****************************************************************************")    
    
    
