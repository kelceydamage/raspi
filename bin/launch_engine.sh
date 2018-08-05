echo -en "\n   +  "
for i in {0..21}; do
  printf "%2b " $i
done

printf "\n\n %3b  " 0
for i in {0..15}; do
  echo -en "\033[48;5;${i}m  \033[m "
done

#for i in 16 52 88 124 160 196 232; do
for i in {0..4}; do
  let "i = i*36 +16"
  printf "\n\n %3b  " $i
  for j in {0..21}; do
    let "val = i+j"
    echo -en "\033[48;5;${val}m  \033[m "
  done
done

echo -e "\n"
echo "         R A S P I      (c) Robot OS                         -K. Damage"

local_home=`pwd`
export PATH=$local_home:$PATH
#export RASPI_HOME=/git/projects/cython/personal
export RASPI_HOME=/opt/git
PYTHON="python3"
$PYTHON $RASPI_HOME/raspi/task_engine/start_engine.py -m
$PYTHON $RASPI_HOME/raspi/task_engine/start_engine.py ROUTER -a 0.0.0.0 &
$PYTHON $RASPI_HOME/raspi/task_engine/start_engine.py TASK -a 0.0.0.0 -p 19100 &
