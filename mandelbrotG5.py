#!/usr/bin/env python
from mandelproc import MandelProc
from multiprocessing import cpu_count
import numpy as np
import colors
import png
import argparse
import math
import os
import sys


def floatlist(s):
    try:
        result = map(float, s.split(','))
    except Exception as exc:
        msg = "Couldn't convert {!r} to floatlist: {}"
        raise argparse.ArgumentTypeError(msg.format(s, exc))

    if any(math.isnan(f) or math.isinf(f) for f in result):
        msg = "Invalid float types: {}"
        raise argparse.ArgumentTypeError(msg.format(s))

    return result


def bounds(s):
    s = floatlist(s)
    if len(s) != 2:
        raise argparse.ArgumentTypeError("Bounds only have two coordinates!")
    if s[0] >= s[1]:
        raise argparse.ArgumentTypeError("Left coordinate in bounds must be less than right coordinate!")
    return s


def colorlist(s):
    colors = s.split(',')
    result = []
    err_msg = "Invalid color format {!r}. Colors must be of the form RRGGBB."
    for c in colors:
        if len(c) != 6:
            raise argparse.ArgumentTypeError(err_msg.format(c))
        c_rgb = []
        for i in range(3):
            e_x = c[2*i:2*i+2]
            try:
                e_i = int(e_x, 16)
            except:
                raise argparse.ArgumentTypeError(err_msg.format(c))
            c_rgb.append(e_i)
        result.append(c_rgb)
    if len(result) == 1:
        result.append(result[0])
    result = [(c[0]/255.0, c[1]/255.0, c[2]/255.0) for c in result]
    return result


parser = argparse.ArgumentParser(description='Generates images of the Mandelbrot set.',
                                 epilog='Dedicated to my Powermac G5 Quad.')
parser.add_argument('--out_file', '-o', help='name of the png file that gets created.', default="image", type=str)
parser.add_argument('--processes', '-p', help='Number of processes to use for image generation.', default=cpu_count(), type=int)
parser.add_argument('--iterations', '-i', help='Number of iterations for \'escape time\' test.', default=100, type=int)
parser.add_argument('--real-bounds', '-r', help='Bounds for the real part of the Mandelbrot calculations.', type=bounds, default=(-2.0, 1.0))
parser.add_argument('--imaginary-bounds', '-I', help='Bounds for the imaginary part of the Mandelbrot calculations.', type=bounds, default=(-1.0, 1.0))
parser.add_argument('--color-pallete', '-c', help='Color pallete for the generated image. Must be of the form "RRGGBB,RRGGBB,RRGGBB", where R, G, and B are hex digits.', type=colorlist, default=colors.pallete)
parser.add_argument('--zoom', '-z', help='Scale factor for image bounds, e.g. the default bounds with zoom of 1000 makes an image 3000 pixels wide and 2000 tall.', type=float, default=1000.0)

# TODO:
# * add color option for inside Mandelbrot set
# * add output file name option


def synced(data, row_flags):
    l = len(data)
    for i in np.arange(l):
        while not row_flags[i]:
            pass
        yield data[i]


def main():
    args = parser.parse_args()
    width = int(args.zoom*(args.real_bounds[1] - args.real_bounds[0]))
    height = int(args.zoom*(args.imaginary_bounds[1] - args.imaginary_bounds[0]))
    MandelProc.set_info(args.iterations,
                        width,
                        height,
                        args.processes,
                        args.real_bounds,
                        args.imaginary_bounds,
                        args.color_pallete)
    procs, data, row_flags = MandelProc.begin_compute()
    #img_file = open('image-%dx%d.png'%(width,height), 'wb')
    #img_file = open('image.png', 'wb')
    img_file = open(args.out_file + ".png", 'wb')
    writer = png.Writer(width, height)
    writer.write(img_file, synced(data, row_flags))


if __name__ == '__main__':
    main()
