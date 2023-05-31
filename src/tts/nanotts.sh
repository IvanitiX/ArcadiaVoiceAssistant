#!/bin/bash

DIR="/code/nanotts"
CMD="echo \"$1\" | nanotts -c -l ${DIR}/lang --voice $2 -o $3 --pitch $4 --speed $5"
echo "Ejecutando ${CMD}"
eval ${CMD}