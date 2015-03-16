#!/bin/bash
#
# This script will install the LIVV dependencies on debian systems such as
# ubuntu. These are IN ADDITION to the Community Ice Sheet Model (CISM)
# dependencies.

# NOTE: Make sure to read over this script as it will use sudo to install
# packages on your system!

# UDUNITS
sudo apt-get install -y libudunits2-dev

# NCL
sudo apt-get install -y ncl-ncarg
#sudo ln -s /usr/share/ncarg /usr/lib/ncarg
    # this fixes a bug in NCL which may be present in Ubuntu 14.04 LTS
    # but as been fixed in package NCL-6.2.0.1ubuntu1
    # test first with:
    # ng4ex gsun01n -clean
