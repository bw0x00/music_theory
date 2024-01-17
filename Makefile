.PHONY: doc
.PHONY: examples 


# TODO: move to site -> part of mkdoc
doc_generated := doc/generated


default: test clean prepare examples doc

prepare:
	mkdir $(doc_generated)

test:
	python3 -m unittest tests/*.py

examples: clean prepare
	python3 -m examples.standard_tuning_tet12_all_c_scales $(doc_generated)
	python3 -m examples.standard_tuning_tet12_all_c_chords $(doc_generated)
	python3 -m examples.standard_tuning_tet12_chords_intervals $(doc_generated)
	python3 -m examples.standard_tuning_tet12_chords_intervals $(doc_generated)
	python3 -m examples.guitar_fretboard_all_notes_e-standard $(doc_generated)

doc: clean prepare
	## todo: not working yet
	python3 -m docgen.guitar_6string_e-standard_all_scales_all_roots $(doc_generated)
	mkdocs build

clean:
	-rm  $(doc_generated)/*
	-rm  -d $(doc_generated)
