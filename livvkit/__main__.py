#!/usr/bin/env python
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
Executable script to start a verification and validation test suite.
Management of the tests to be run is handled by the scheduler in livvkit.util
"""

import os
import sys
import http.server as server
import socketserver as socket
from pathlib import Path
import shutil

import livvkit
from livvkit.util import options
from loguru import logger

log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS Z}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<magenta>{process.name}.{process.id}</magenta> | "
    "<level>{message}</level>"
)
logger.remove(0)  # Don't log to sys.stderr

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")

LOGO = r"""-------------------------------------------------------------------
                   __   _____   ___   ____    _ __
                  / /  /  _/ | / / | / / /__ (_) /_
                 / /___/ / | |/ /| |/ /  '_// / __/
                /____/___/ |___/ |___/_/\_\/_/\__/

                Land Ice Verification & Validation
-------------------------------------------------------------------
"""


@logger.catch
def main(cl_args=None):
    """Direct execution."""
    if cl_args is None and len(sys.argv) > 1:
        cl_args = sys.argv[1:]
    args = options.parse_args(cl_args)
    out_name = Path(livvkit.output_dir).parts[-1]
    log_file = Path(f"livv_log_{out_name}.log")
    if log_file.exists():
        # Backup the log file
        _filetime = str(os.stat(log_file).st_ctime).replace(".", "_")
        _newname = f"{log_file.stem}_bkd_{_filetime}.log"
        shutil.move(log_file, _newname)
    logger.add(log_file, format=log_format, enqueue=True)

    print(LOGO)
    print("")
    print("  Current run: " + livvkit.timestamp)
    print("  User: " + livvkit.user)
    print("  OS Type: " + livvkit.os_type)
    print("  Machine: " + livvkit.machine)

    from livvkit.components import numerics
    from livvkit.components import verification
    from livvkit.components import performance
    from livvkit.components import validation
    from livvkit import elements
    from livvkit import scheduler
    from livvkit.util import functions

    summary_elements = []

    if livvkit.verify or livvkit.validate:
        logger.info("SETUP OUTPUT")
        functions.setup_output()

    if livvkit.verify:
        summary_elements.append(
            scheduler.run(
                "numerics", numerics, functions.read_json(livvkit.numerics_model_config)
            )
        )
        summary_elements.append(
            scheduler.run(
                "verification",
                verification,
                functions.read_json(livvkit.verification_model_config),
            )
        )
        summary_elements.append(
            scheduler.run(
                "performance",
                performance,
                functions.read_json(livvkit.performance_model_config),
            )
        )
    if livvkit.validate:
        print(" -----------------------------------------------------------------")
        print("   Beginning the validation test suite ")
        print(" -----------------------------------------------------------------")
        print("")
        validation_config = {}
        for conf in livvkit.validation_model_configs:
            logger.info(f"ADDING {conf} config")
            if "yml" in conf or "yaml" in conf:
                validation_config = functions.merge_dicts(
                    validation_config, functions.read_yaml(conf)
                )
            else:
                validation_config = functions.merge_dicts(
                    validation_config, functions.read_json(conf)
                )

        logger.info(
            f"WRITE MERGED VALIDATION CONFIG TO {livvkit.output_dir}/livvkit.yml"
        )
        functions.write_yaml(validation_config, livvkit.output_dir, "livvkit.yml")

        logger.info("BEGIN RUNNING VALIDATION SUITE")
        summary_elements.extend(
            scheduler.run_quiet(
                "validation", validation, validation_config, group=False
            )
        )
        logger.info("DONE - RUNNING VALIDATION SUITE")
        print(" -----------------------------------------------------------------")
        print("   Validation test suite complete ")
        print(" -----------------------------------------------------------------")
        print("")

    if livvkit.verify or livvkit.validate:
        result = elements.Page("Summary", "", summary_elements)
        with open(os.path.join(livvkit.output_dir, "index.json"), "w") as index_data:
            index_data.write(result._repr_json())

        if "/global/cfs/projectdirs" in livvkit.output_dir:
            webaddress = livvkit.output_dir.replace(
                "/global/cfs/projectdirs", "https://portal.nersc.gov/project"
            ).replace("/www", "")
        else:
            webaddress = ""

        print("-------------------------------------------------------------------")
        print(" Done!  Results can be seen in a web browser at:")
        print("  " + os.path.join(livvkit.output_dir, "index.html"))
        if webaddress:
            print("    or")
            print("  " + webaddress)
        print("-------------------------------------------------------------------")

    # Make webpage output directory have 0755 permissions
    # functions.webdir_chmod(livvkit.output_dir)

    if args.serve:
        httpd = socket.TCPServer(("", args.serve), server.SimpleHTTPRequestHandler)

        sa = httpd.socket.getsockname()
        print(
            "\nServing HTTP on {host} port {port} (http://{host}:{port}/)".format(
                host=sa[0], port=sa[1]
            )
        )
        print("\nView the generated website by navigating to:")
        print(
            "\n    http://{host}:{port}/{path}/index.html".format(
                host=sa[0], port=sa[1], path=os.path.relpath(livvkit.output_dir)
            )
        )
        print("\nExit by pressing `ctrl+c` to send a keyboard interrupt.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
