for i in {0..1}
do
  one=1
  ten=10
  x=$(($i * $ten))
  t=$(($i + $one))
  y=$(($t * $ten))
  echo $x
  echo $y
    timeout 1200 pypy createIndex.py $x $y
done
