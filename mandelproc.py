from multiprocessing import Process, RawArray, Event
import numpy as np
from math import log
import colors


class MandelProcException(Exception): pass


class MandelProc(Process):

    ITERATIONS = None
    PIXWIDTH = None
    PIXHEIGHT = None
    STEP = None
    RMIN = None
    RMAX = None
    IMIN = None
    IMAX = None
    PALLETE = None

    def __init__(self, procnum, data, row_flags, x_coords, *args, **kwds):
        """A helper process for generating the Mandelbrot set."""
        Process.__init__(self, *args, **kwds)
        self.offset = procnum
        self.data = data
        self.row_flags = row_flags
        self.x_coords = x_coords

    @classmethod
    def set_info(cls, iters, width, height, num_procs, rbounds, ibounds, pallete):
        """Sets constants for the parallel computation.

        Argument:
        iters - the number of iterations to use for the escape time test.
        width - the width of the image being generated in pixels.
        height - the height of the image being generated in pixels.
        num_procs - the number of helper processes that will run."""
        cls.ITERATIONS = iters
        cls.PIXWIDTH = width
        cls.PIXHEIGHT = height
        cls.STEP = num_procs
        cls.RMIN = rbounds[0]
        cls.RMAX = rbounds[1]
        cls.IMIN = ibounds[0]
        cls.IMAX = ibounds[1]
        cls.PALLETE = pallete

    @classmethod
    def begin_compute(cls):
        """Starts the Mandelbrot set computation."""
        no_val = "No {} value set!"
        essential_values = [
            "ITERATIONS",
            "PIXWIDTH",
            "PIXHEIGHT",
            "STEP",
            "RMIN",
            "RMAX",
            "IMIN",
            "IMAX",
            "PALLETE",
        ]

        for v in essential_values:
            if getattr(cls, v, None) is None:
                raise MandelProcException(no_val.format(v))
        
        x_coords = RawArray('I', np.arange(cls.PIXWIDTH, dtype='I'))
        pixel_data = RawArray('B', 3*cls.PIXWIDTH*cls.PIXHEIGHT)
        row_flags = RawArray('B', cls.PIXHEIGHT)
        np_array = np.frombuffer(pixel_data, dtype='B')
        np_array = np_array.reshape(cls.PIXHEIGHT, 3*cls.PIXWIDTH)
        procs = [cls(i, np_array, row_flags, x_coords) for i in range(cls.STEP)]
        for p in procs:
            p.start()
        return procs, np_array, row_flags

    def run(self):
        ##### Constants #####
        PIXHEIGHT = MandelProc.PIXHEIGHT
        PIXWIDTH = MandelProc.PIXWIDTH
        ITERATIONS = MandelProc.ITERATIONS
        STEP = MandelProc.STEP
        RMIN = MandelProc.RMIN
        RMAX = MandelProc.RMAX
        IMIN = MandelProc.IMIN
        IMAX = MandelProc.IMAX
        PALLETE = MandelProc.PALLETE
        PALLETE_LEN = len(PALLETE)
        LOG2 = log(2)
        BAILRADIUS = 1 << 16
        XCOORDS = self.x_coords
        #####################

        data = self.data
        row_flags = self.row_flags

        for py in np.arange(self.offset, PIXHEIGHT, STEP):
            # scale y pixel to be between 1 and -1.
            # note: pixel y axis increases as cartesian y axis decreases,
            # which is why we subtract from IMAX instead of adding to IMIN.
            y0 = IMAX - (IMAX - IMIN)*py/PIXHEIGHT

            for px in XCOORDS:
                # scale x pixel to be between -2 and 1.
                x0 = RMIN + (RMAX - RMIN)*px/PIXWIDTH
                # cardiod test
                q = (x0 - .25)**2 + y0*y0
                if q*(q + (x0 - .25)) < .25*y0*y0:
                    continue
                    
                # period 2 bulb test
                if (x0 + 1)**2 + y0*y0 < 0.0625:
                    continue

                # escape time test
                i = 0
                x = 0.0
                y = 0.0
                while (x*x + y*y < BAILRADIUS) and (i < ITERATIONS):
                    # a simple periodicity check
                    xtemp = x*x - y*y + x0
                    ytemp = 2*x*y + y0
                    if x==xtemp and y==ytemp:
                        i = ITERATIONS
                        break
                      
                    x = xtemp
                    y = ytemp
                    i = i + 1

                # smooth iteration count
                if i < ITERATIONS:
                    log_zn = log(x*x + y*y)/2
                    nu = log(log_zn/LOG2)/LOG2
                    i = i + 1 - nu
                    # interpolate color
                    start_color = int(i%PALLETE_LEN)
                    end_color = int((start_color + 1)%PALLETE_LEN)
                    fraction = i%1.0
                    r, g, b = colors.rgb_interp(PALLETE[start_color],
                                                PALLETE[end_color],
                                                fraction)
                    data[py,3*px] = 255*r
                    data[py,3*px+1] = 255*g
                    data[py,3*px+2] = 255*b
                    
            row_flags[py] = 1
