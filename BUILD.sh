# precompile c++ modules
echo -e "PRE_COMPILING PXD\n"
cython --cplus motors/drive.pyx --force

# general compile of project modules
echo -e "RUNNING SETUP.PY\n"
python3.6 setup.py build_ext --inplace --force

echo -e "DONE\n"
# distribute and cleanup

