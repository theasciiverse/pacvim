#!/bin/sh
# Records the 100x30 catalog preview, asciiverse/pacvim.cast
# (hub/RECORDING.md): normal mode from level 0, played by
# asciiverse/drive.py for 50 s. asciinema records a tmux pane (own socket,
# no status line, no user config) that drive.py reads and plays in. The
# ghosts move at random: run it again until the take clears level 0.
# Needs asciinema 3 and tmux; run asciiverse/build.sh first.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
root=$(dirname "$here")
out=$here/pacvim.cast
home=$(mktemp -d)
trap 'tmux -L avrec kill-server 2>/dev/null; rm -rf "$home"' EXIT
mkdir -p "$home/bin/lib" "$home/bin/maps"
cp "$root/pacvim" "$home/bin/lib/pacvim"
cp "$here/pacvim" "$home/bin/pacvim"
cp "$root"/maps/map*.txt "$home/bin/maps/"
cd "$home"  # nothing in the recording names a local path
export HOME="$home" PATH="$home/bin:$PATH" TERM=xterm-256color COLORTERM=truecolor LANG=C.UTF-8
tmux -L avrec -f /dev/null new-session -d -s rec -x 100 -y 30 "pacvim n" \; set -g status off
python3 -I "$here/drive.py" avrec rec 50 &
asciinema rec --headless --overwrite -q \
  --window-size 100x30 --idle-time-limit 2 \
  --capture-env "TERM,COLORTERM,LANG" --title "PacVim" \
  --command "tmux -L avrec attach -t rec" "$out"
wait
