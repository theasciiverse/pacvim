#!/bin/sh
# Builds pacvim. Linux: run inside alpine:3.22 for a fully static binary
# (ncurses and libstdc++ linked in); macOS: run on the runner with CC_ARCH
# set to x86_64 or arm64, linking the system's ncurses.
#   docker run --rm -v "$PWD":/src -w /src alpine:3.22 sh asciiverse/build.sh
# Leaves ./pacvim. The maps folder is compiled in as /usr/share/pacvim-maps
# for the system packages; av's start script points PACVIM_MAPS at the
# maps next to it instead.
set -eu
if [ -f /etc/alpine-release ]; then
  apk add --no-cache build-base pkgconf ncurses-dev ncurses-static >/dev/null
  ldflags="-static"
  ldlibs="$(pkg-config --static --libs ncursesw) -lpthread"
else
  ldflags=""
  ldlibs="-lncurses -lpthread"
fi
cxx="c++${CC_ARCH:+ -arch $CC_ARCH}"
make clean >/dev/null
make CXX="$cxx" MAPDIR=/usr/share/pacvim-maps LDFLAGS="$ldflags" LDLIBS="$ldlibs"
strip pacvim
