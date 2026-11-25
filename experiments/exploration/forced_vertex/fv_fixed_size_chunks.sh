#!/bin/bash
# usage: runchunks.sh FIRST LAST ; chunk w handles first labels a with a%40==w; skips completed chunks
cd "$(dirname "$0")"
seq $1 $2 | xargs -P4 -I{} sh -c 'f=c157/chunk_{}.txt; grep -q "^p=" $f 2>/dev/null || ./fvw 157 8 40 {} > $f.tmp && mv $f.tmp $f'
