languages.pdf: languages.dvi
	dvipdf languages.dvi
	evince languages.pdf &

languages.dvi: languages.tex languages.bib
	latex languages
	bibtex languages
	latex languages
	latex languages

