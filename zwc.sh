#! /bin/bash --
for F in "$@"; do
  echo "$(zcat -f <"$F" | wc -l) $F"
done

