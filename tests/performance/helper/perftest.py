import time
import numpy

from datetime import date
from mpi4py import MPI

def perftest(f):
    def _inner(*args, **kwargs):

        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()

        t_start  = time.time()
        test_out = f(*args, **kwargs)
        t_end    = time.time()
        dt       = numpy.array([t_end - t_start])

        dt_min = numpy.zeros(1)
        dt_max = numpy.zeros(1)
        dt_sum = numpy.zeros(1)
        comm.Reduce([dt, MPI.DOUBLE], [dt_min, MPI.DOUBLE], op=MPI.MIN, root=0)
        comm.Reduce([dt, MPI.DOUBLE], [dt_max, MPI.DOUBLE], op=MPI.MAX, root=0)
        comm.Reduce([dt, MPI.DOUBLE], [dt_sum, MPI.DOUBLE], op=MPI.SUM, root=0)

        if rank is 0:
            average = dt_sum[0] / size
            print "%s took (%s / %s / %s)s" % (getattr(f, "__name__", "<unnamed>"), dt_min[0], average, dt_max[0])

            filename = "%s_%s" % (getattr(f, "__name__", "<unnamed>"), date.today())
            measurements = "%s %s %s %s\n" % (size, dt_min[0], average, dt_max[0])
            with open(filename, "a") as out:
                out.write(measurements)

    return _inner