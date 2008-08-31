#!/bin/sh
#
# invoke the prolog script as
#     prolog=/path/to/prolog/script $job_id

JOBID=$1

echo "prolog: start. hostname="`/bin/hostname` --- JOBID = $JOBID
echo "prolog:        user="$USER

echo "prolog:        start loading VM   = "`/bin/date`
echo sge_queue=$QUEUE
sudo /server/vmstore/SGE/prod_vmimage_start.sh "$QUEUE" "$JOBID"
vmimagemanagerc=$?
echo "prolog:        end   loading VM rc=$vmimagemanagerc  = "`/bin/date`

# synchronization
sleep 30                       
echo "prolog:        end synchronization= "`/bin/date`

echo "prolog: stop."

exit 0