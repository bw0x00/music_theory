doc_generated := doc/generated

default: test clean prepare examples 

prepare:
	mkdir $(doc_generated)

test:
	python3 -m unittest tests/*.py

examples:
	python3 -m samples.all_standard_tuning_tet12_c_scales $(doc_generated)
	python3 -m samples.all_standard_tuning_tet12_c_chords $(doc_generated)

clean:
	rm -rf $(doc_generated)
