sphinx-apidoc -A "Martin Moxon" -P -H "Martin's Huffman Encoder" -M -e -f -F -o docs src/
python modify_conf.py
cd docs
make clean
make html
touch $null >> _build/html/.nojekyll
cd ..
git add *
git commit -m "Updated Documentation"
git subtree push --prefix docs/_build/html origin gh-pages
