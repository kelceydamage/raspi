#! /usr/bin/env python3

from distutils.core import setup
from distutils.extension import Extension
import platform

USE_CYTHON = True

ext = '.pyx' if USE_CYTHON else '.c'

extentions = [
    Extension(
        "python_src.b_processor.lib.timer", 
        sources=["python_src/b_processor/lib/timer{0}".format(ext)],
        extra_compile_args=['-Wno-strict-prototypes'],
        language="c++"
        ),
    Extension(
        "python_src.b_processor.driver.haruspex", 
        sources=["python_src/b_processor/driver/haruspex{0}".format(ext)],
        extra_compile_args=['-Wno-strict-prototypes'],
        language="c++"
        ),
    Extension(
        "python_src.b_processor.task_engine.task", 
        sources=["python_src/b_processor/task_engine/task{0}".format(ext)],
        extra_compile_args=['-Wno-strict-prototypes'],
        language="c++"
        ),
    Extension(
        "python_src.b_processor.task_engine.engine", 
        sources=["python_src/b_processor/task_engine/engine{0}".format(ext)],
        extra_compile_args=['-Wno-strict-prototypes'],
        language="c++"
        ),
    Extension(
        "python_src.b_processor.transforms.transforms", 
        sources=["python_src/b_processor/transforms/transforms{0}".format(ext)],
        extra_compile_args=['-Wno-strict-prototypes'],
        language="c++"
        ),
    Extension(
        "python_src.b_processor.lib.parser", 
        sources=["python_src/b_processor/lib/parser{0}".format(ext)],
        extra_compile_args=['-Wno-strict-prototypes'],
        language="c++"
        ),
    Extension(
        "python_src.b_processor.config.configuration", 
        sources=["python_src/b_processor/config/configuration{0}".format(ext)],
        extra_compile_args=['-Wno-strict-prototypes'],
        language="c++"
        ),
    Extension(
        "test", 
        sources=["test{0}".format(ext)],
        extra_compile_args=['-Wno-strict-prototypes'],
        language="c++"
        )
    ]

if USE_CYTHON:
    from Cython.Build import cythonize
    extentions = cythonize(extentions)

setup(
    ext_modules = extentions
)
