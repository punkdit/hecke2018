
all: hecke.pdf


hecke.pdf: hecke.tex  refs.bib
	pdflatex hecke.tex
	bibtex hecke
	pdflatex hecke.tex
	pdflatex hecke.tex


