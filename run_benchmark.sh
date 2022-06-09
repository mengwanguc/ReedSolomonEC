arguments=""

while getopts n:k:m:f: flag
do
    case "${flag}" in
        n) data=${OPTARG};;
        k) parity=${OPTARG};;
        m) mode=${OPTARG};;
        f) filename=${OPTARG};;

    esac
done

arguments=$arguments$data" "$parity

if [ "$mode" == "i" ]
then
    ./erasure_code/erasure_code_perf_from_file $data $parity 128 > $filename
else
    ./gradlew run --args="$arguments" > $filename
fi