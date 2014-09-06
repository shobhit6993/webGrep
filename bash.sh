for i in {13..15}
do
  one=1
  ten=10
  x=$(($i * $ten))
  t=$(($i + $one))
  y=$(($t * $ten))
  echo $x
  echo $y
    timeout 1500 pypy createIndex.py $x $y
    rc=$?
    if [[ $rc != 0 ]] ; then
            echo $x >> kharab
    fi

done
