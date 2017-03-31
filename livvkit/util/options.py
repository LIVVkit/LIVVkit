# Copyright (c) 2015,2016, UT-BATTELLE, LLC
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
# 3. Neither the name of the copyright holder nor the names of its contributor
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

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import time
import pkgutil
import argparse
import importlib

import livvkit
from livvkit import bundles
from livvkit import resources


def parse_args(args=None):
    """
    Handles the parsing of options for LIVV's command line interface

    Args:
        args: The list of arguments, typically sys.argv[1:]
    """
    parser = argparse.ArgumentParser(description="Main script to run LIVV.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     fromfile_prefix_chars='@')

    parser.add_argument('-o', '--out-dir',
                        default=os.path.join(os.getcwd(), "vv_" + time.strftime("%Y-%m-%d")),
                        help='Location to output the LIVV webpages.')

    parser.add_argument('-v', '--verify',
                        nargs=2,
                        default=None,
                        help=' '.join([
                                       'Specify the locations of the test and bench bundle to',
                                       'compare (respectively).'
                                       ])
                        )

    parser.add_argument('-V', '--validate',
                        action='store',
                        nargs='+',
                        default=None,
                        help='Specify the location of the configuration files for validation tests.')

    parser.add_argument('-p', '--publish',
                        action='store_true',
                        help=' '.join([
                                       'Also produce a publication quality copy of the figure in',
                                       'the output directory (eps, 600d pi).'
                                       ])
                        )

    return init(parser.parse_args(args))


def init(options):
    """ Initialize some defaults """

    # Set matlplotlib's backend so LIVVkit can plot to files.
    import matplotlib
    matplotlib.use('agg')

    livvkit.resource_dir = os.sep.join(resources.__path__)
    livvkit.output_dir = os.path.abspath(options.out_dir)
    livvkit.index_dir = livvkit.output_dir
    livvkit.verify = True if options.verify is not None else False
    livvkit.validate = True if options.validate is not None else False
    livvkit.publish = options.publish

    # Get a list of bundles that provide model specific implementations
    available_bundles = [mod for imp, mod, ispkg in pkgutil.iter_modules(bundles.__path__)]

    if options.verify is not None:
        # rstrip accounts for trailing path separators
        livvkit.model_dir = options.verify[0].rstrip(os.sep)
        livvkit.bench_dir = options.verify[1].rstrip(os.sep)
        if not os.path.isdir(livvkit.model_dir):
            print("")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("                       UH OH!")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("    Your comparison directory does not exist; please check")
            print("    the path:")
            print("\n"+livvkit.model_dir+"\n\n")
            sys.exit(1)

        if not os.path.isdir(livvkit.bench_dir):
            print("")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("                       UH OH!")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("    Your benchmark directory does not exist; please check")
            print("    the path:")
            print("\n"+livvkit.bench_dir+"\n\n")
            sys.exit(1)

        livvkit.model_bundle = livvkit.model_dir.split(os.sep)[-1]
        livvkit.bench_bundle = livvkit.bench_dir.split(os.sep)[-1]

        if livvkit.model_bundle in available_bundles:
            livvkit.numerics_model_config = os.sep.join(
                bundles.__path__ + [livvkit.model_bundle, "numerics.json"])
            livvkit.numerics_model_module = importlib.import_module(
                ".".join(["livvkit.bundles", livvkit.model_bundle, "numerics"]))

            livvkit.verification_model_config = os.sep.join(
                 bundles.__path__ + [livvkit.model_bundle, "verification.json"])
            livvkit.verification_model_module = importlib.import_module(
                 ".".join(["livvkit.bundles", livvkit.model_bundle, "verification"]))

            livvkit.performance_model_config = os.sep.join(
                 bundles.__path__ + [livvkit.model_bundle, "performance.json"])
            # NOTE: This isn't used right now...
            # livvkit.performance_model_module = importlib.import_module(
            #      ".".join(["livvkit.bundles", livvkit.model_bundle, "performance"]))
        else:
            # TODO: Should implement some error checking here...
            livvkit.verify = False

    if options.validate is not None:
        livvkit.validation_model_configs = options.validate

    if not (livvkit.verify or livvkit.validate):
        print("")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("                       UH OH!")
        print("----------------------------------------------------------")
        print("    No verification or validation tests found/submitted!")
        print("")
        print("    Use either one or both of the --verify and")
        print("    --validate options to run tests.  For more ")
        print("    information use the --help option, view the README")
        print("    or check https://livvkit.github.io/Docs/")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("")
        sys.exit(1)

    return options
