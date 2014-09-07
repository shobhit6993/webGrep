for i in {0..15} # iterating over the 15 batches
do
  one=1
  ten=10
  x=$(($i * $ten))
  t=$(($i + $one))
  y=$(($t * $ten)) # I am a noob in bash :(
  echo $x
  echo $y
    timeout 1500 pypy createIndex.py $x $y # Specifying a maximum timeout to process a batch. It is assumed to no other process is taking the cpu and hard-disk
    rc=$?
    if [[ $rc != 0 ]] ; then
            echo $x >> fault # echoing the batch no. which either timedout or exited with some non-zero exit code
    fi

done
