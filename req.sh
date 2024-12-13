#/bin/bash

host='localhost'
port='5001'

get_count=350
post_count=50
patch_count=10
delete_count=50

total_req=$((get_count + post_count))

echo $total_req

while [ $total_req -gt 0 ]; do

#((total_req--))

    ch=$(( ( RANDOM %5 ) + 1 ))

    model=$(( ( RANDOM %50 ) + 1 ))

    api=$(( ( RANDOM %2 ) + 1 ))

    if [ "$api" -eq 1 ]; then
	api="cars"
    else
	api="boats"
    fi

  case "$ch" in
  
	"1")
		if [ "$get_count" -gt 0 ]; then
                  ((get_count--))
		  ((total_req--))
		  echo get list $get_count
		  curl $host:$port/$api
		fi
	;;
 
	"2")
                if [ "$get_count" -gt 0 ]; then
                  ((get_count--))
                  ((total_req--))
                  echo get single $model model $get_count 
                  curl $host:$port/$api/$model
                fi
  ;;

	"3")
                if [ "$post_count" -gt 0 ]; then
                  ((post_count--))
                  ((total_req--))
                  echo post car $post_count
                  photo_file="file-"$(( ( RANDOM %3 ) + 1 ))".dat"
                  curl -X POST -F photo=@${photo_file} localhost:5001/$api
                fi		
	;;

  "4")
                if [ "$patch_count" -gt 0 ]; then
                  ((patch_count--))
                  ((total_req--))
                  echo patch $model car $patch_count
                  curl -X PATCH $host:$port/$api/$model
                fi
  ;;

	"5")
                if [ "$delete_count" -gt 0 ]; then
                  ((delete_count--))
                  ((total_req--))
                  echo delete $model car $patch_count
                  curl -X DELETE $host:$port/$api/$model
                fi

  ;;

  esac

  echo STEP $total_req , GET = $get_count , POST = $post_count

done
