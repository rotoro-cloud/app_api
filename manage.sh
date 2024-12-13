#/bin/bash
[ ! -f file-1.dat ] && dd if=/dev/zero of=file-1.dat bs=7500 count=1
[ ! -f file-2.dat ] && dd if=/dev/zero of=file-2.dat bs=13500 count=1
[ ! -f file-3.dat ] && dd if=/dev/zero of=file-3.dat bs=19000 count=1
[ ! -f file-4.dat ] && dd if=/dev/zero of=file-4.dat bs=21000 count=1

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
