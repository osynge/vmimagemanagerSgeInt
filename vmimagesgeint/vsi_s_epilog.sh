#!/bin/sh
#
# invoke the epilog script as
#    epilog path/to/epilog/script

virthost=`cat /tmp/$JOB_ID`

echo start epilog: hostname=`/bin/hostname` --- JOBID = $JOB_ID 

# shutdown the virtual machine
sudo /server/vmstore/SGE/prod_vmimage_stop.sh "$virthost" "$JOB_ID"

echo epilog script: end

exit 0