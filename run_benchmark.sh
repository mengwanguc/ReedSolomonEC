arguments=""

while getopts a:b:n:k:c:m:f:e:l:r:p: flag
do
    case "${flag}" in
        a) net_data=${OPTARG};;
        b) net_parity=${OPTARG};;
        n) loc_data=${OPTARG};;
        k) loc_parity=${OPTARG};;
        c) chunksize=${OPTARG};;
        m) mode=${OPTARG};;
        f) filename=${OPTARG};;
        e) ec=${OPTARG};;
        l) local_groups=${OPTARG};;
        r) global_parity=${OPTARG};;
        p) local_parity=${OPTARG};;
    esac
done

if [ "$mode" == "i" ]
then
    if [ "$ec" == "s" ]
    then
        ./erasure_code/erasure_code_perf_from_file $loc_data $loc_parity $chunksize > $filename
    elif [ "$ec" == "m" ]
    then
        ./erasure_code/erasure_code_perf_mlec_split $net_data $net_parity $loc_data $loc_parity $chunksize > $filename
    elif [ "$ec" == "l" ]
    then
        ./erasure_code/erasure_code_perf_lrc $loc_parity $local_groups $global_parity $local_parity $chunksize > $filename
    else
        echo "Error: Invalid EC method specified."
    fi
elif [ "$mode" == "j" ]
then
    if [ "$ec" == "s" ]
    then
        arguments=$arguments$loc_data" "$loc_parity" "$chunksize
        ./gradlew -PmainClass=com.backblaze.erasure.ReedSolomonBenchmark run --args="$arguments" > $filename
    elif [ "$ec" == "m" ]
    then
        arguments=$arguments$net_data" "$net_parity" "$loc_data" "$loc_parity" "$chunksize
        ./gradlew -PmainClass=com.backblaze.erasure.ReedSolomonBenchmarkMLEC run --args="$arguments" > $filename
    elif [ "$ec" == "l" ]
    then
        arguments=$arguments$loc_parity" "$local_groups" "$global_parity" "$local_parity" "$chunksize
        ./gradlew -PmainClass=com.backblaze.erasure.ReedSolomonBenchmarkLRC run --args="$arguments" > $filename
    else
        echo "Error: Invalid EC method specified."
    fi
else
    echo "Error: Invalid mode specified."
fi