# coding=utf-8
# Copyright (c) 2015-2018, UT-BATTELLE, LLC
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

import os
import sys
import time
import pkgutil
import argparse
import importlib
import multiprocessing as mp

import livvkit
from livvkit import bundles


def positive_int(integer):
    """
    Argparse helper function to specify a zero or positive integer as an
    argument type
    :param integer: A zero or positive integer
    :return: integer
    """
    integer = int(integer)
    if integer < 0:
        raise argparse.ArgumentTypeError('Must be zero or a positive integer')
    return integer


def parse_args(args=None):
    """
    Handles the parsing of options for LIVVkit's command line interface

    Args:
        args: The list of arguments, typically sys.argv[1:]
    """
    parser = argparse.ArgumentParser(description='Main script to run LIVVkit.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     fromfile_prefix_chars='@')

    parser.add_argument('-o', '--out-dir',
                        default=os.path.join(os.getcwd(), 'vv_' + time.strftime('%Y-%m-%d')),
                        help='Location to output the LIVVkit webpages.'
                        )

    parser.add_argument('-v', '--verify',
                        nargs=2,
                        default=None,
                        help='Specify the locations of the test and bench bundle '
                             'to compare (respectively).'
                        )

    parser.add_argument('-V', '--validate',
                        action='store',
                        nargs='+',
                        default=None,
                        help='Specify the location of the configuration files '
                             'for validation tests.'
                        )

    # FIXME: this just short-circuits to the validation option, and should become its own module
    parser.add_argument('-e', '--extension',
                        action='store',
                        nargs='+',
                        default=None,
                        dest='validate',
                        metavar='EXTENSION',
                        help='Specify the location of the configuration files '
                             'for LIVVkit extensions.'
                        )

    parser.add_argument('-s', '--serve',
                        nargs='?',
                        type=int,
                        const=8000,
                        help='Start a simple HTTP server for the output website '
                             'specified by OUT_DIR on port SERVE.'
                        )

    parser.add_argument('-p', '--pool-size',
                        nargs='?',
                        type=int,
                        default=(mp.cpu_count() - 1 or 1),
                        help='The number of multiprocessing processes to run '
                             'analyses in. If zero, processes will run serially '
                             'outside of the multiprocessing module.')

    parser.add_argument('--version',
                        action='version',
                        version='LIVVkit {}'.format(livvkit.__version__),
                        help="Show LIVVkit's version number and exit"
                        )

    return init(parser.parse_args(args))


def init(options):
    """ Initialize some defaults """

    # Set matlplotlib's backend so LIVVkit can plot to files.
    import matplotlib
    matplotlib.use('agg')

    livvkit.output_dir = os.path.abspath(options.out_dir)
    livvkit.index_dir = livvkit.output_dir
    livvkit.verify = True if options.verify is not None else False
    livvkit.validate = True if options.validate is not None else False
    livvkit.pool_size = options.pool_size

    # Get a list of bundles that provide model specific implementations
    available_bundles = [mod for imp, mod, ispkg in pkgutil.iter_modules(bundles.__path__)]

    if options.verify is not None:
        livvkit.model_dir = os.path.normpath(options.verify[0])
        livvkit.bench_dir = os.path.normpath(options.verify[1])
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

        livvkit.model_bundle = os.path.basename(livvkit.model_dir)
        livvkit.bench_bundle = os.path.basename(livvkit.bench_dir)

        # For MPAS/COMPASS/MALI, the basename isn't MALI it's the generic "landice"
        # check if the bundle is in the available bundles, then see if an available bundle
        # is somewhere in the path, and use that bundle
        if livvkit.model_bundle not in available_bundles:
            bundle_in_path = [_bundle in livvkit.model_dir for _bundle in available_bundles]
            if any(bundle_in_path):
                # This uses the first found bundle in the path (Left-to-right) in the unlikely
                # but possible instance that multiple bundles are in the path
                livvkit.model_bundle = available_bundles[bundle_in_path.index(True)]
                livvkit.bench_bundle = livvkit.model_bundle

        if livvkit.model_bundle in available_bundles:
            livvkit.numerics_model_config = os.path.join(
                livvkit.bundle_dir, livvkit.model_bundle, "numerics.json")
            livvkit.numerics_model_module = importlib.import_module(
                ".".join(["livvkit.bundles", livvkit.model_bundle, "numerics"]))

            livvkit.verification_model_config = os.path.join(
                 livvkit.bundle_dir, livvkit.model_bundle, "verification.json")
            livvkit.verification_model_module = importlib.import_module(
                 ".".join(["livvkit.bundles", livvkit.model_bundle, "verification"]))

            livvkit.performance_model_config = os.path.join(
                 livvkit.bundle_dir, livvkit.model_bundle, "performance.json")
            # NOTE: This isn't used right now...
            # livvkit.performance_model_module = importlib.import_module(
            #      ".".join(["livvkit.bundles", livvkit.model_bundle, "performance"]))
        else:
            # TODO: Should implement some error checking here...
            livvkit.verify = False

    if options.validate is not None:
        livvkit.validation_model_configs = options.validate

    if not (livvkit.verify or livvkit.validate) and not options.serve:
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
