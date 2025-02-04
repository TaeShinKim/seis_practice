#!/bin/bash



# Preprocess
cd /home/cc/amatrice/preprocess/runs || exit 1
./runpreprocess.chasZ > outZ 2>&1 &
./runpreprocess.chasH > outH 2>&1 &

# Correl
cd /home/cc/amatrice/correl/runs || exit 1
./runcorrel9.chasZ > outZ 2>&1 &
./runcorrel9.chasN > outN 2>&1 &
./runcorrel9.chasE > outE 2>&1 &

# Select
./runselect5 > select.out 2>&1 &

