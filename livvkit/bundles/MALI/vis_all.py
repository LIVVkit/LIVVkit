#!/usr/bin/env python
import numpy
import netCDF4
from optparse import OptionParser
import matplotlib.pyplot as plt
from pathlib import Path
import multiprocessing as mp
from functools import partial
import xarray as xr

def __plot_mali(in_file, in_var, title, axis=None):
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
    # normalVelocity = f.variables["normalVelocity"]
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


def plot_mali(in_file, in_var, axis=None):
    """Plot MALI."""
    title = " ".join(in_file.parts[-5:])[:-3]
    # print(title)
    data = xr.open_dataset(in_file)
    # Plot the model output
    plt.xlabel("Model Data")
    plt.ylabel(in_var)
    # plt.xticks([])
    # plt.yticks([])
    # plt.imshow(model_data, vmin=_min, vmax=_max, interpolation='nearest', cmap=colormaps.viridis)
    x_data_m = data.xCell
    y_data_m = data.yCell
    try:
        model_data = data[in_var][-1] - data[in_var][0]
    except KeyError:
        model_data = numpy.zeros(x_data_m.shape)
        # print(f"   {in_var} not in {in_file}")

    vabsmax = numpy.max(numpy.abs(model_data)) * 0.98
    if vabsmax == 0:
        vabsmax = 0.001

    plt.scatter(
        x_data_m,
        y_data_m,
        10,
        model_data,
        vmin=-vabsmax,
        vmax=vabsmax,
        marker="h",
        edgecolors="black",
        linewidths=0.05,
        cmap="RdBu_r"
    )
    plt.title(title)
    plt.colorbar()
    plt.savefig(f"plots/plt_{'_'.join(title.split())}")
    plt.close()


def main():

    in_dir = Path("/Users/25k/Data/MPAS/MALI_2020-12-21/landice")
    in_files = in_dir.rglob("*output*.nc")

    with mp.Pool(10) as pool:
        test_results = pool.map_async(partial(plot_mali, in_var="thickness"), in_files)
        results = test_results.get()
        # plot_mali(_file, "thickness", title)

if __name__ == "__main__":
    main()