#!/usr/bin/env python3
"""drive.py SOCKET SESSION SECONDS: plays PacVim in a tmux pane.

Each tick it reads the pane with its colours: walls are yellow, tildes
cyan, ghosts red G, letters still to visit white, visited ones green; the
player is the terminal cursor. It walks (h j k l) the shortest path to the
nearest white letter that keeps clear of the ghosts, ten steps a
second, and presses Enter at each level's start screen. After SECONDS it
quits with q. Ghosts move at random, so runs differ. Run by record-preview.sh under asciinema."""
import collections, random, re, subprocess, sys, time

SOCK, S, SECONDS = sys.argv[1], sys.argv[2], float(sys.argv[3])
rng = random.Random(3)
SGR = re.compile(r"\x1b\[([0-9;]*)m")

def tmux(*a): return subprocess.run(["tmux", "-L", SOCK, *a], capture_output=True, text=True).stdout
def key(k): tmux("send-keys", "-t", S, k)

def grid():
    """(char, colour) per cell, from capture-pane -e."""
    rows = []
    for line in tmux("capture-pane", "-p", "-e", "-t", S).split("\n"):
        row, color, i = [], 37, 0
        while i < len(line):
            m = SGR.match(line, i)
            if m:
                for p in (m.group(1) or "0").split(";"):
                    if p.isdigit() and 30 <= int(p) <= 37:
                        color = int(p)
                    elif p in ("", "0", "39"):
                        color = 37
                i = m.end()
                continue
            if line[i] not in "\x0e\x0f":
                row.append((line[i], color))
            i += 1
        rows.append(row)
    return rows

def cursor():
    x, y = tmux("display", "-p", "-t", S, "#{cursor_x} #{cursor_y}").split()
    return int(y), int(x)

def cell(g, y, x):
    return g[y][x] if 0 <= y < len(g) and 0 <= x < len(g[y]) else (" ", 0)

def step(g, me):
    ghosts = [(y, x) for y, r in enumerate(g) for x, (c, col) in enumerate(r) if c == "G" and col == 31]
    danger = {(gy + dy, gx + dx) for gy, gx in ghosts for dy in range(-2, 3) for dx in range(-2, 3)}
    moves = {(0, -1): "h", (1, 0): "j", (-1, 0): "k", (0, 1): "l"}
    prev, todo = {me: None}, collections.deque([me])
    while todo:
        c = todo.popleft()
        ch, col = cell(g, *c)
        if c != me and col == 37 and ch.strip() and ch != "G":
            while prev[c] != me:
                c = prev[c]
            return moves[(c[0] - me[0], c[1] - me[1])]
        for d in moves:
            n = (c[0] + d[0], c[1] + d[1])
            nch, ncol = cell(g, *n)
            if n in prev or ncol in (33, 36) or n in danger or n[0] > 26:
                continue
            if not nch.strip() and ncol == 0:
                continue  # off the map
            prev[n] = c
            todo.append(n)
    # boxed in: step away from the nearest ghost
    if ghosts:
        gy, gx = min(ghosts, key=lambda p: abs(p[0] - me[0]) + abs(p[1] - me[1]))
        for d, k in moves.items():
            n = (me[0] + d[0], me[1] + d[1])
            if cell(g, *n)[1] not in (33, 36) and abs(n[0] - gy) + abs(n[1] - gx) > abs(me[0] - gy) + abs(me[1] - gx):
                return k
    return None

start = time.time()
time.sleep(2.5)
key("Enter")
time.sleep(1.0)
while time.time() - start < SECONDS:
    g = grid()
    if any("PRESS ENTER" in "".join(c for c, _ in r) for r in g):
        time.sleep(1.5)
        key("Enter")
        time.sleep(1.0)
        continue
    k = step(g, cursor())
    if k:
        key(k)
    time.sleep(0.1)
for r in grid():
    t = "".join(c for c, _ in r)
    if "Points" in t or "Lives" in t or "LEVEL" in t:
        print(t.strip(), file=sys.stderr)
key("q")
time.sleep(3)
