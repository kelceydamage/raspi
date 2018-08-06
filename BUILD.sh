# init
PROJECT=$1
if [ -z "$1" ]; then
    echo "ERROR: Must specify a project (folder) name"
    exit 1
fi

# precompile c++ modules
echo -e "PRE_COMPILING PXD\n"
cython --annotate-coverage coverage.xml $PROJECT/drive.pyx --force --embed --cplus

# general compile of project modules
echo -e "RUNNING SETUP.PY\n"
python3 $PROJECT/setup.py build_ext --inplace --force

# postcompile c++ modules
echo -e "POST_COMPILING PXD for annotations and coverage\n"
cython --annotate-coverage coverage.xml $PROJECT/drive.pyx --force --embed --cplus

echo -e "DONE\n"
# distribute and cleanup
rm -rf $PROJECT/*.cpp
rm -rf $PROJECT/*.c
rm -rf */*/*/*/*.pyc