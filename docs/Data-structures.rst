LIVV's data structures are grouped generally by their functionality.
Each set of functionality below has a listing of its own data structures
that are used. Dictionaries are denoted by {key\_description :
value\_description}. Arrays are denoted by [value1, value2, ...,
valueN].

Verification
------------

-  bit\_for\_bit\_details:

   -  A summary of the bit or bit tests conducted by a test object.
   -  {'Test Case' : {'NetCDF Filename' : [Status , {variable : [max
      err, rmse err]} } }

-  file\_test\_details

   -  A summary of the standard ouptut files parsed by a test object.
   -  {'Test Case' : ['Output Filename', {variable : value}] }

-  model\_configs / bench\_configs

   -  A summary of the test and benchmark configuration files parsed.
   -  {'Test Case' : {'Config Filename : {'Section Name' : {variable :
      value} } }

-  summary

   -  Key details from the overall test object
   -  {'Test Case' : [ number std out files, number config matches,
      number config files, number bit matches, number bit tests] }

Performance
-----------

-  plot\_details

   -  Keeps track of plot files and descriptions.
   -  {'Test Case' : [[filename, description],...]}

-  file\_test\_details

   -  A summary of the standard ouptut files parsed by a test object.
   -  {'Test Case' : ['Output Filename', {variable : value}] }

-  model\_configs / bench\_configs

   -  A summary of the test and benchmark configuration files parsed.
   -  {'Test Case' : {'Config Filename : {'Section Name' : {variable :
      value} } }

-  model\_timing\_data / bench\_timing\_data

   -  A summary of the timing files parsed.
   -  {'Test Case' : {'Processor Count' : {variable : [mean, max, min]}
      } }
