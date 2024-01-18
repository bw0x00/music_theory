.PHONY: doc
.PHONY: examples 


# TODO: move to site -> part of mkdoc
examples_generated := examples


default: test clean prepare examples doc

prepare:
	#pass

test:
	python3 -m unittest tests/*.py

examples: clean prepare
	python3 -m examples.standard_tuning_tet12_c_scales $(examples_generated)
	python3 -m examples.standard_tuning_tet12_c_chords $(examples_generated)
	python3 -m examples.standard_tuning_tet12_chords_intervals $(examples_generated)
	python3 -m examples.standard_tuning_tet12_chords_intervals $(examples_generated)
	python3 -m examples.guitar_fretboard_all_notes_e-standard $(examples_generated)

doc: clean prepare
	## todo: not working yet
##	python3 -m docgen.guitar_6string_e-standard_all_scales_all_roots $(doc_generated)
	mkdocs build

clean:
	-rm  $(examples_generated)/*.svg
	-rm  $(examples_generated)/*.txt
