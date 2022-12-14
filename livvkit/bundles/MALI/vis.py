#!/usr/bin/env python
import numpy
import netCDF4
from optparse import OptionParser
import matplotlib.pyplot as plt

def plot_mali(in_file, in_var, axis=None):
    """
    Plot `in_var` of `in_file` on an axis using hexagonal points.

    Parameters
    ----------
    in_file : `netCDF4.Dataset`
        Input dataset
    in_var : string
        Variable name within netCDF file
    axis : `matplotlib.pyplot.Axis`, optional
        Axis on which to create plot. If not passed, a small figure is created

    Returns
    -------
    None

    """

    times = f.variables["xtime"]
    dcedge = f.variables["dcEdge"]
    x_cell = f.variables["xCell"]
    y_cell = f.variables["yCell"]
    x_edge = f.variables["xEdge"]
    y_edge = f.variables["yEdge"]
    angle_edge = f.variables["angleEdge"]
    # bedTopography = f.variables['bedTopography']  # not needed
    # temperature = f.variables["temperature"]
    # lowerSurface = f.variables["lowerSurface"]
    # upperSurface = f.variables["upperSurface"]
    thickness = f.variables["thickness"]
    normalVelocity = f.variables["normalVelocity"]
    # uReconstructX = f.variables["uReconstructX"]
    # uReconstructX = f.variables["uReconstructX"]
    # uReconstructY = f.variables["uReconstructY"]

    vert_levs = f.dimensions["nVertLevels"].size
    time_length = times.shape[0]
    # print("vert_levs = {};  time_length = {}".format(vert_levs, time_length))

    var_slice = thickness[time_slice, :]
    # var_slice = var_slice.reshape(time_length, ny, nx)

    # print "Global max = ", global_max, " Global min = ", global_min
    # print "Surface max = ", maxval, " Surface min = ", minval

    fig = plt.figure(1, facecolor="w")
    ax = fig.add_subplot(111, aspect="equal")
    plt.scatter(x_cell[:], y_cell[:], 80, var_slice, marker="h", edgecolors="none")
    plt.colorbar()
    plt.title("thickness at time " + str(time_slice))
    plt.draw()
    if options.saveimages:
        print("Saving figures to files.")
        plt.savefig("dome_thickness.png")

    fig = plt.figure(4)
    ax = fig.add_subplot(121, aspect="equal")
    plt.scatter(
        x_edge[:],
        y_edge[:],
        80,
        normalVelocity[time_slice, :, vert_levs - 1] * secInYr,
        marker="h",
        edgecolors="none",
    )
    plt.colorbar()
    plt.quiver(
        x_edge[:],
        y_edge[:],
        numpy.cos(angle_edge[:]) * normalVelocity[time_slice, :, vert_levs - 1] * secInYr,
        numpy.sin(angle_edge[:]) * normalVelocity[time_slice, :, vert_levs - 1] * secInYr,
    )
    plt.title("normalVelocity of bottom layer at time " + str(time_slice))
    plt.draw()
    ax = fig.add_subplot(122, aspect="equal")
    plt.scatter(
        x_edge[:],
        y_edge[:],
        80,
        normalVelocity[time_slice, :, 0] * secInYr,
        marker="h",
        edgecolors="none",
    )
    plt.colorbar()
    plt.quiver(
        x_edge[:],
        y_edge[:],
        numpy.cos(angle_edge[:]) * normalVelocity[time_slice, :, 0] * secInYr,
        numpy.sin(angle_edge[:]) * normalVelocity[time_slice, :, 0] * secInYr,
    )
    plt.title("normalVelocity of top layer at time " + str(time_slice))
    plt.draw()
    if options.saveimages:
        plt.savefig("dome_normalVelocity.png")


def main():

    parser = OptionParser()
    parser.add_option(
        "-f", "--file", dest="filename", help="file to visualize", metavar="FILE"
    )
    parser.add_option(
        "-t", "--time", dest="time", help="time step to visualize (0 based)", metavar="TIME"
    )
    parser.add_option(
        "-s",
        "--save",
        action="store_true",
        dest="saveimages",
        help="include this flag to save plots as files",
    )
    parser.add_option(
        "-n",
        "--nodisp",
        action="store_true",
        dest="hidefigs",
        help="include this flag to not display plots (usually used with -s)",
    )
    options, args = parser.parse_args()

    if not options.filename:
        print("No filename provided. Using output.nc.")
        options.filename = "output.nc"

    if not options.time:
        print("No time provided. Using time 0.")
        time_slice = 0
    else:
        time_slice = int(options.time)


    secInYr = (
        3600.0 * 24.0 * 365.0
    )  # Note: this may be slightly wrong for some calendar types!


    f = netCDF4.Dataset(options.filename, "r")

    f.close()


if __name__ == "__main__":
    main()