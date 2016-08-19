#!/usr/bin/env python3

import os
import sys
import glob

import livvkit
from livvkit.util import TexHelper as th
from livvkit.util import functions

datadir = sys.argv[1] 
outdir = sys.argv[2]
functions.mkdir_p(outdir)

data_files = glob.glob(datadir + "/**/*.json", recursive=True)
data_files = [datadir + '/verification/dome.json']
#data_files = [datadir + '/index.json']


for each in data_files:
    data = functions.read_json(each)
    tex = th.translate_page(data)
    outfile = os.path.join(outdir, os.path.basename(each).replace('json', 'tex'))
    with open(outfile, 'w') as f:
        f.write(tex)

