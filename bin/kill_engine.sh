PIDS=(`ps aux|grep start_engine|awk '{print $2}'`)
unset 'PIDS[${#PIDS[@]}-1]'
if [ ${#PIDS[@]} -eq 0 ]; then
	echo "------------------------------------------------------------------------"
	echo "Failed to find any running instances"
	echo "------------------------------------------------------------------------" 
	exit 1
else
	echo "------------------------------------------------------------------------"
	echo "Found the following processes, beginning kill..."
	echo "------------------------------------------------------------------------"
	ps aux|grep start_engine|awk '{print $1,$2,$11,$12}'|grep -v grep
	for pid in ${PIDS[@]}; do kill -9 $pid; done
	echo "------------------------------------------------------------------------"
	echo "Kill complete"
	echo "------------------------------------------------------------------------"
	ps aux|grep start_engine|grep -v grep
fi