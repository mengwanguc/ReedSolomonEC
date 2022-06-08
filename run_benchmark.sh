arguments=""

while getopts n:k:f:m: flag
do
    case "${flag}" in
        n) arguments=$arguments${OPTARG};;
        k) arguments=$arguments" "${OPTARG};;
        f) filename=${OPTARG};;
        m) mode=${OPTARG};;

    esac
done

if ["$mode" == "i"]
then
    # Run 
else
    if [ "$arguments" == "" ]
    then
        ./gradlew run > $filename
    else
        ./gradlew run --args="$arguments" > $filename
    fi
fi