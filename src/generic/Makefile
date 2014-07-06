# This is a very generic Makefile to build all tex files in a subdirectory

TEX_SOURCES=$(wildcard */*.tex)
PDF_TARGETS=$(addprefix out/, $(TEX_SOURCES:.tex=.pdf))

out/%.pdf: %.tex
	latexmk -pdflatex=lualatex -pdf -output-directory=$(@D) $<

all: ${PDF_TARGETS}

.PHONY: clean
clean:
	rm out/ -rf
