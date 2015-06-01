sphinx-apidoc -A "Martin Moxon" -P -H "Martin's Huffman Encoder" -M -e -f -F -o docs src/
python modify_conf.py
cd docs
make clean
make html
exit
