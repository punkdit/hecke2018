
all: algebraic.pdf sketches.pdf


cusp.pdf: cusp.tex   dynkin.tex
	timeout 10s pdflatex cusp.tex
	bibtex cusp
	pdflatex cusp.tex
	pdflatex cusp.tex


algebraic.pdf: algebraic.tex   dynkin.tex
	timeout 10s pdflatex algebraic.tex
	bibtex algebraic
	pdflatex algebraic.tex
	pdflatex algebraic.tex

dolan.pdf: dolan.tex  refs2.bib
	timeout 10s pdflatex dolan.tex
	bibtex dolan
	pdflatex dolan.tex
	pdflatex dolan.tex


sketches.pdf: sketches.tex  refs2.bib
	timeout 10s pdflatex sketches.tex
	bibtex sketches
	pdflatex sketches.tex
	pdflatex sketches.tex


hecke.pdf: hecke.tex  refs.bib
	timeout 10s pdflatex hecke.tex
	bibtex hecke
	pdflatex hecke.tex
	pdflatex hecke.tex


