#!/usr/bin/env python
#-------------------------------------------------------------------------------- <-80
# Author: Kelcey Damage
# Python: 2.7

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Doc
#-------------------------------------------------------------------------------- <-80
"""
SUMMARY:                Starter script for storing registered functions
"""

# Imports
#-------------------------------------------------------------------------------- <-80
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy
import time
import math

# Globals
#-------------------------------------------------------------------------------- <-80
WIDTH = 32
DEPTH = 32
TOTAL = WIDTH * DEPTH
BLOCK = 32
GRID = int(math.ceil(math.sqrt((TOTAL / BLOCK)) / 8))
GRID = GRID - (GRID % 32)
if GRID == 0:
        GRID = 1

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80
def main(func, a, a_doubled):
    t0 = time.time()
    t1 = time.time()
    a_gpu = cuda.mem_alloc(a.nbytes)
    mem_allocate = time.time() - t1
    #print('Allocate to CUDA memory: {0}s'.format(mem_allocate))

    t11 = time.time()
    cuda.memcpy_htod_async(a_gpu, a)
    mem_cp_time = time.time() - t11
    #print('Copy object to CUDA memory: {0}s'.format(mem_cp_time))

    t = time.time()
    func(a_gpu, block=(BLOCK, BLOCK, 1), grid=(100, 100))
    total_time = time.time() - t
    #print('Call CUDA Kernel: {0}'.format(total_time))

    t3 = time.time()
    cuda.memcpy_dtoh(a_doubled, a_gpu)
    recv_mem = time.time() - t3
    #print('Retrieve object from CUDA memory: {0}'.format(recv_mem))

    return total_time, recv_mem, mem_cp_time, t0
    

def print_out(total_time, recv_mem, mem_cp_time, t0):
    t_time = total_time + recv_mem + mem_cp_time
    print('--------------------------------------------------------')
    print('Took: {0}s'.format(t_time))
    print('Rate: {0:f} / s'.format(round(TOTAL / t_time, 2)))
    print('End to end: {0}s'.format(time.time() - t0))
    print('--------------------------------------------------------')

def gen_kernel():
    return SourceModule("""
        __global__ void double_it(float *a)
        {
                int idx = threadIdx.x + blockDim.x * blockIdx.x;
                a[idx] *= 2;
        }
        """)

def compile_kernel():
    t2 = time.time()
    mod = gen_kernel()
    func = mod.get_function("double_it")
    setup_kern = time.time() - t2
    print('Compile CUDA Kernel: {0}'.format(setup_kern))
    return func

def gen_objects():
    t0 = time.time()
    a = numpy.random.randn(WIDTH, DEPTH)
    a = a.astype(numpy.float32)
    a_doubled = numpy.empty_like(a)
    init_time = time.time() - t0
    print('Generate numpy object time: {0}'.format(init_time))
    return a, a_doubled

def task_get_cuda_test(*args, **kwargs):
    print('--------------------------------------------------------')
    print('Doubling float matrix of {0} x {1} [{2}]'.format(WIDTH, DEPTH, TOTAL))
    print('Grid: ({0},{0}), Block: ({1},{1},1)'.format(100, BLOCK))
    a, a_doubled = gen_objects()
    func  = compile_kernel()
    for i in xrange(4):
        total_time, recv_mem, mem_cp_time, t0 = main(func, a, a_doubled)
        print_out(total_time, recv_mem, mem_cp_time, t0)

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
    print('--------------------------------------------------------')
    
    
    func = compile_kernel()
    matrices = []
    times = []
    rates = []
    for i in xrange(10):
        print(WIDTH, DEPTH)
        print('Doubling float matrix of {0} x {1} [{2}]'.format(WIDTH, DEPTH, TOTAL))
        print('Grid: ({0},{0}), Block: ({1},{1},1)'.format(100, BLOCK))
        a, a_doubled = gen_objects()
        total_time, recv_mem, mem_cp_time, t0 = main(func, a, a_doubled)
        t_time = total_time + recv_mem + mem_cp_time
        print_out(total_time, recv_mem, mem_cp_time, t0)
        matrices.append(str(TOTAL))
        times.append(str(t_time))
        rates.append(str(round(TOTAL / t_time, 2)))
        WIDTH = WIDTH << 1
        DEPTH = DEPTH << 1
        TOTAL = WIDTH * DEPTH

    print(','.join(matrices))
    print(','.join(times))
    print(','.join(rates))