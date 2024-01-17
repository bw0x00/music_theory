.PHONY: doc

doc_generated := doc/generated
pydoc_generated := $(doc_generated)/pydoc

default: test clean prepare examples gendoc

prepare:
	mkdir $(doc_generated)
	mkdir $(pydoc_generated)

test:
	python3 -m unittest tests/*.py

examples: clean prepare
	python3 -m samples.standard_tuning_tet12_all_c_scales $(doc_generated)
	python3 -m samples.standard_tuning_tet12_all_c_chords $(doc_generated)
	python3 -m samples.standard_tuning_tet12_chords_intervals $(doc_generated)
	python3 -m samples.standard_tuning_tet12_chords_intervals $(doc_generated)
	python3 -m samples.guitar_fretboard_all_notes_e-standard $(doc_generated)

doc: clean prepare
	## todo: not working yet
	cd $(pydoc_generated)
	echo pydoc3 -w `find ../../pymusictheory -name *.py`
	cd ../..
#	python3 -m docgen.guitar_6string_e-standard_all_scales_all_roots $(doc_generated)

clean:
	-rm $(pydoc_generated)/*
	-rm -d $(pydoc_generated)
	-rm  $(doc_generated)/*
	-rm  -d $(doc_generated)
