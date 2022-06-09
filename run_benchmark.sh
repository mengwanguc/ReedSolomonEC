arguments=""

while getopts n:k:c:m:f: flag
do
    case "${flag}" in
        n) data=${OPTARG};;
        k) parity=${OPTARG};;
        c) chunksize=${OPTARG};;
        m) mode=${OPTARG};;
        f) filename=${OPTARG};;

    esac
done

arguments=$arguments$data" "$parity" "$chunksize

if [ "$mode" == "i" ]
then
    ./erasure_code/erasure_code_perf_from_file $data $parity $chunksize > $filename
else
    ./gradlew run --args="$arguments" > $filename
fi