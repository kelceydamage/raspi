#!/usr/bin/env python3
# ------------------------------------------------------------------------ 79->
# Author: ${name=Kelcey Damage}
# Python: 3.5+
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Doc
# ------------------------------------------------------------------------ 79->

# Imports
# ------------------------------------------------------------------------ 79->

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def main(cuda, func, a, a_doubled):
    a_gpu = cuda.mem_alloc(a.nbytes)
    cuda.memcpy_htod_async(a_gpu, a)
    func(a_gpu, block=(32, 32, 1), grid=(32, 32))
    cuda.memcpy_dtoh(a_doubled, a_gpu)
    return a_doubled

def gen_kernel(SourceModule):
    return SourceModule("""
        __global__ void double_it(float *a)
        {
                int idx = threadIdx.x + blockDim.x * blockIdx.x;
                a[idx] *= 2;
        }
        """)

def compile_kernel(SourceModule):
    mod = gen_kernel(SourceModule)
    func = mod.get_function("double_it")
    return func

def gen_objects(numpy, WIDTH, DEPTH):
    a = numpy.random.randn(WIDTH, DEPTH)
    a = a.astype(numpy.float32)
    a_doubled = numpy.empty_like(a)
    return a, a_doubled

def task_double_cuda_matrix(*args, **kwargs):
    import pycuda.driver as cuda
    import pycuda.autoinit
    from pycuda.compiler import SourceModule
    import numpy
    import time
    a, a_doubled = gen_objects(numpy, 32, 32)
    try:
        func  = compile_kernel(SourceModule)
    except Exception as e:
        return str(e)
    results = []
    for i in xrange(4):
        start = time.time()
        try:
            a_doubled = main(cuda, func, a, a_doubled)
        except Exception as e:
            return str(e)
        else:
            end = time.time() - start
            results.append((len(a_doubled), end))
    return results

# Main
# ------------------------------------------------------------------------ 79->
