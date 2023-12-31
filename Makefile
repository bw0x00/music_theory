doc_generated := doc/generated

default: clean prepare test examples 

prepare:
	mkdir $(doc_generated)

test:
	python3 -m unittest tests/*.py

examples:
	python3 -m samples.all_scales $(doc_generated)

clean:
	rm -rf $(doc_generated)
