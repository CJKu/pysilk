#!/bin/bash
# A tool to parse gecko log and retrieve silk log
#

SCRIPT="$0"
SCRIPTPATH="$(dirname $SCRIPT)"
cd ${SCRIPTPATH}

if [ -z $1 ]; then
  echo "Input filename missed."
  exit 1
fi

# The name of source log file
IN=$1
# The name of output field file
# default output filename is "output.txt"
OUT=${2:-output_log.tsv}

echo "Generate and put field data into \"${OUT}\""

# sample name
LOG_NAME="Silk input resample"
SILK_LOG_PATTERN="s/.*${LOG_NAME} *, *\([0-9]*\) *, *\([.0-9]*\).*/\1	\2/"

# Convert log string into two fields: "frame number" "distance"
# For example, if the source log looks like
# "I/Gecko   ( 6418): Silk input resample , 196827, 0.030"
# This script tunrs it into
# "196827 0.030"
# The format of this output file is tab-delilited text. So that
# we can use AppleScript to import these records into a table
# in Numbers
sed -n "/${LOG_NAME}/p" "${IN}" | sed "${SILK_LOG_PATTERN}" > ${OUT}

echo "Done..."
