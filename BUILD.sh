# init
#PROJECT=$1
#if [ -z "$1" ]; then
#    echo "ERROR: Must specify a project (folder) name"
#    exit 1
#fi

# precompile c++ modules
echo -e "PRE_COMPILING PXD\n"
echo -e "compiling: datatypes.pxd\n"
cython --annotate-coverage coverage.xml common/datatypes.pyx --force --cplus -I . 
echo -e "compiling: marshalling.pxd\n"
cython --annotate-coverage coverage.xml common/marshalling.pyx --force --cplus -I .
echo -e "compiling: client.pxd\n"
cython --annotate-coverage coverage.xml task_engine/client/client.pyx --force --cplus -I .
echo -e "compiling: routers.pxd\n"
cython --annotate-coverage coverage.xml task_engine/engine/routers.pyx --force --cplus -I .

# general compile of project modules
echo -e "RUNNING SETUP.PY\n"
python3 setup.py build_ext --inplace --force

echo -e "DONE\n" 
# distribute and cleanup
rm -rf $PROJECT*.cpp
rm -rf $PROJECT*.c
rm -rf */*/*/*/*.pyc