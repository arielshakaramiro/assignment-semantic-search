#!/usr/bin/env bash
# Setup environment lalu jalankan notebook dari awal sampai akhir (hasil tersimpan di notebook).
set -e
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=600 \
  notebook/starter_notebook_semantic_search.ipynb
echo "SELESAI - notebook berhasil dijalankan."
