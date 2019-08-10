#!/bin/bash
ROOT=rtl/

# If GIT_HOME is not set to the root location of your git folder globally, you can set here.
# GIT_HOME=~/git
GIT_HOME=/git/projects/personal

# Project/repo folder within your git home dir.
PROJECT_DIR=raspi-tasks

# Pre compile function for writing clean cpp file.
function pre_compile() {
    cython -a --cplus $1 --force --include-dir $GIT_HOME/$PROJECT_DIR
}

PYX_FILES=(
    "${ROOT}common/task.pyx"
    "${ROOT}tasks/openArray.pyx"
    "${ROOT}tasks/normalize.pyx"
    )

# precompile c++ modules
for i in ${PYX_FILES[@]}; do
    echo -e "Pre-compiling: $i"
    pre_compile $i
done

# general compile of project modules
echo -e "Starting full compile"
python setup.py build_ext --inplace --force
