arguments=""

while getopts a:b:n:k:c:m:f:e: flag
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

    esac
done

if [ "$mode" == "i" ]
then
    if [ "$ec" == "s" ]
    then
        ./erasure_code/erasure_code_perf_from_file $loc_data $loc_parity $chunksize > $filename

    else
        ./erasure_code/erasure_code_perf_mlec_split $net_data $net_parity $chunksize $loc_data $loc_parity > $filename
    fi
else
    if [ "$ec" == "s" ]
    then
        arguments=$arguments$loc_data" "$loc_parity" "$chunksize
        ./gradlew -PmainClass=com.backblaze.erasure.ReedSolomonBenchmark run --args="$arguments" > $filename
    else
        arguments=$arguments$net_data" "$net_parity" "$loc_data" "$loc_parity" "$chunksize
        ./gradlew -PmainClass=com.backblaze.erasure.ReedSolomonBenchmarkMLEC run --args="$arguments" > $filename
    fi
fi