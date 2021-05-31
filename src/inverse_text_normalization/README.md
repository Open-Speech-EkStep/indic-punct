Text denormalization system for Indic Languages, e.g. `चार सौ आट्ठारह` -> `418` <br>
Currently supports Hindi.

Installation:
1. pip install -r requirements.txt
2. conda install -c conda-forge pynini==2.1.4


Example prediction run:
python run_predict.py  --input=`INPUT_FILE` [--inverse_normalizer nemo]
