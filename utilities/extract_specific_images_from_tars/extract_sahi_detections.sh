#!/usr/bin/env bash
filelist="$1" 
tarfile="$2"
neigh=10
outdir="extracted/${tarfile%.tar}"

mkdir -p "$outdir"

mapfile -t contents < <(tar -tf "$tarfile")

while read -r target; do
    [[ -z "$target" ]] && continue

    idx=$(printf "%s\n" "${contents[@]}" | grep -n -x "$target" | cut -d: -f1)
    if [[ -n "$idx" ]]; then
        start=$(( idx - neigh ))
        end=$(( idx + neigh ))
        (( start < 1 )) && start=1
        (( end > ${#contents[@]} )) && end=${#contents[@]}

        files_to_extract=( "${contents[@]:start-1:end-start+1}" )

        echo "[$tarfile] extracting ${#files_to_extract[@]} around $target"
        tar -xf "$tarfile" -C "$outdir" "${files_to_extract[@]}"
    fi
done < "$filelist"
