

sketches.pdf: sketches.tex  refs2.bib
	pdflatex sketches.tex
	bibtex sketches
	pdflatex sketches.tex
	pdflatex sketches.tex


hecke.pdf: hecke.tex  refs.bib
	pdflatex hecke.tex
	bibtex hecke
	pdflatex hecke.tex
	pdflatex hecke.tex


