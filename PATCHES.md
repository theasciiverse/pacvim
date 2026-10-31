# Changes from upstream

This is the Asciiverse packaging of [PacVim](https://github.com/jmoon018/PacVim)
by Jamal Moon (2014-2018), a maze game that teaches vim motions, in C++ and
ncurses. Upstream is the `upstream` remote; this build is upstream's
`master` at `ca7c883` (2018-05-16), the last commit: release 1.1.1 plus a
Makefile repair, the change of licence from GPL to LGPL-3.0-or-later
(`COPYING.LESSER`, with `COPYING` for the GPL it builds on) and a
Dockerfile. Debian packages 1.1.1 without patches of its own. The
`asciiverse` branch carries the changes below.

## Code

- **Relocatable maps.** `PACVIM_MAPS` names the maps folder, ahead of the
  one compiled in (`MAPS_LOCATION`), so av's install finds its maps.
- **No errors.log.** The game appended its messages ("YOU WIN", "GAME
  ENDED!") to `errors.log` in whatever folder it was started from. They
  now go to stderr, and only when stderr is not the terminal (it would
  draw over the game): av sends them to the title's log.

## Packaging (new files)

- `asciiverse/build.sh`: static Linux build in Alpine, macOS builds per
  architecture against the system's ncurses.
- `asciiverse/pacvim`, `asciiverse/stage.sh`: av's start script and the
  archive layout (binary in `lib/`, `maps/` beside it).
- `asciiverse/nfpm.yaml`: .deb, .rpm, .apk and Arch packages, maps in
  `/usr/share/pacvim-maps`.
- `asciiverse/record-preview.sh`, `asciiverse/drive.py`: the catalog
  preview, played by a script in a tmux pane.
- `.github/workflows/release.yml`: builds all of it on a tag.

## Not built

- Windows: PacVim runs its ghosts on POSIX threads under ncurses.
