#!/bin/sh
# Lays out the av archive in stage/: the start script at the top, the
# binary in lib/, and the maps beside them.
set -eu
rm -rf stage && mkdir -p stage/lib stage/maps
cp pacvim stage/lib/pacvim
cp asciiverse/pacvim stage/pacvim
cp maps/map*.txt stage/maps/
cp COPYING COPYING.LESSER README.md PATCHES.md stage/
