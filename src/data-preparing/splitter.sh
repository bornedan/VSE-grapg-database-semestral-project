#!/bin/bash

# Vstupní soubor
INPUT_FILE="dblp.v12.json"

# Velikost každé části (1G = 1 GB)
PART_SIZE="1G"

# Výstupní prefix a přípona
OUTPUT_PREFIX="file"
OUTPUT_SUFFIX=".json"

# Čítač pro názvy souborů
n=1

# Rozdělení souboru na části s dočasným názvem
split -b "$PART_SIZE" "$INPUT_FILE" temp_part_

# Přejmenování výsledných souborů
for f in temp_part_*; do
  mv "$f" "${OUTPUT_PREFIX}${n}${OUTPUT_SUFFIX}"
  n=$((n+1))
done

echo "Rozdělení dokončeno. Výsledné soubory: ${OUTPUT_PREFIX}1${OUTPUT_SUFFIX}, ${OUTPUT_PREFIX}2${OUTPUT_SUFFIX}, ..."
