# PacVim (Asciiverse packaging)

Jamal Moon's PacVim (C++, ncurses, LGPL-3.0-or-later), packaged for the
Asciiverse catalog (id `pacvim`, kind `game`) the way Typespeed is: static
Linux build, macOS build, a start script, system packages. Not our code:
keep changes small and list every one in PATCHES.md.

- `upstream` is github.com/jmoon018/PacVim (branch `master`, last commit
  2018); ours is branch `asciiverse`, `origin` github.com/theasciiverse/pacvim.
- Release: tag `v1.1.1+20180516-av.<n>` and push it;
  `.github/workflows/release.yml` builds Linux (Alpine, static), macOS and
  .deb/.rpm/.apk/Arch packages. No Windows build.
- Local build: `sh asciiverse/build.sh` (or in alpine:3.22 for the static
  one) leaves `./pacvim`; run it with `PACVIM_MAPS=maps ./pacvim`.
- Preview: `asciiverse/record-preview.sh` (asciinema 3, tmux); ghosts are
  random, so re-run until the take clears level 0 (about 40 s).
