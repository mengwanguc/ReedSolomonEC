#!/bin/bash

# Set environment variables for erasure coding enumerations
export ISA_L=0
export JAVA_RS=1
export SLEC=0
export MLEC=1
export MLEC_SPLIT=2
export LRC=3
export DEC_SLEC=4

arguments=""

while getopts a:b:n:k:c:m:f:e:l:r:p:t: flag
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
        t) type=${OPTARG};;
    esac
done

if [ "$mode" = "$ISA_L" ];
then
    if [ "$ec" = "$SLEC" ];
    then
        echo "Running ISA-L SLEC Encoding Process"
        ./isa-l/erasure_code/erasure_code_perf_from_file $loc_data $loc_parity $chunksize > $filename
    elif [ "$ec" = "$MLEC" ];
    then
        echo "Running ISA-L Serial MLEC Encoding Process"
        ./isa-l/erasure_code/erasure_code_perf_mlec $net_data $net_parity $loc_data $loc_parity $chunksize > $filename
    elif [ "$ec" = "$MLEC_SPLIT" ];
    then
        echo "Running ISA-L Parallel MLEC Encoding Process"
        ./isa-l/erasure_code/erasure_code_perf_mlec_split $net_data $net_parity $loc_data $loc_parity $chunksize > $filename
    elif [ "$ec" = "$LRC" ];
    then
        echo "Running ISA-L LRC Encoding Process"
        ./isa-l/erasure_code/erasure_code_perf_lrc $loc_parity $local_groups $global_parity $local_parity $chunksize $type > $filename
    elif [ "$ec" = "$DEC_SLEC" ];
    then
        echo "Running ISA-L SLEC Decoding Process"
        ./isa-l/erasure_code/erasure_decode_slec $loc_data $loc_parity $chunksize > $filename
    else
        echo "Error: Invalid EC method specified."
    fi
elif [ "$mode" = "$JAVA_RS" ];
then
    if [ "$ec" = "$SLEC" ];
    then
        echo "Running JAVA RS SLEC Encoding Process"
        arguments=$arguments$loc_data" "$loc_parity" "$chunksize
        ./JavaReedSolomon/gradlew -PmainClass=com.backblaze.erasure.ReedSolomonBenchmark run --args="$arguments" > $filename
    elif [ "$ec" = "$MLEC" ];
    then
        echo "Running JAVA RS MLEC Encoding Process"
        arguments=$arguments$net_data" "$net_parity" "$loc_data" "$loc_parity" "$chunksize
        ./JavaReedSolomon/gradlew -PmainClass=com.backblaze.erasure.ReedSolomonBenchmarkMLEC run --args="$arguments" > $filename
    elif [ "$ec" = "$LRC" ];
    then
        echo "Running JAVA RS LRC Encoding Process"
        arguments=$arguments$loc_parity" "$local_groups" "$global_parity" "$local_parity" "$chunksize
        ./JavaReedSolomon/gradlew -PmainClass=com.backblaze.erasure.ReedSolomonBenchmarkLRC run --args="$arguments" > $filename
    else
        echo "Error: Invalid EC method specified."
    fi
else
    echo "Error: Invalid mode specified."
fi
