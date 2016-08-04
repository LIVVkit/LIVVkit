#!/usr/bin/env python3

import os
import glob

import livvkit
from livvkit.util import TexHelper as th
from livvkit.util import functions

# TODO: Replace this with the right thing
datadir = "vv_2016-07-30"
functions.mkdir_p(outdir)

data_files = glob.glob(datadir + "/**/*.json", recursive=True)
data_files = [datadir + '/index.json']

for each in data_files:
    data = functions.read_json(each)
    tex = th.translate_page(data)
    outfile = os.path.join(outdir, os.path.basename(each).replace('json', 'tex'))
    with open(outfile, 'w') as f:
        f.write(tex)

