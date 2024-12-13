#/bin/bash

now=$(date +%s)
end=$((now + 7200))

while [ $((end - now)) -gt 0 ]; do
  echo no
  sleep 10
  now=$(date +%s)
  echo $now

  api=$(( ( RANDOM %3 ) + 1 ))
  if [ "$api" -eq 1 ]; then
    ./req.sh
  else
    sleep 5
  fi

done
