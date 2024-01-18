.PHONY: doc
.PHONY: examples 


# TODO: move to site -> part of mkdoc
examples_generated := examples
img_doc := docs/img

default: test clean prepare examples

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
	python3 -m examples.guitar_fretboard_chord_Cmaj_pitchclasses $(img_doc)
	python3 -m examples.guitar_fretboard_scale_major_pentatonic_c $(img_doc)
	mkdocs serve 

clean:
	-rm  $(img_doc)/*.svg
	-rm  $(examples_generated)/*.svg
	-rm  $(examples_generated)/*.txt
