# This is a very generic Makefile to build all tex files in a subdirectory

TEX_SOURCES=$(wildcard */*.tex)
PDF_TARGETS=$(addprefix out/, $(TEX_SOURCES:.tex=.pdf))

out/%.pdf: %.tex
	latexmk -pdflatex=lualatex -pdf -output-directory=$(@D) $<

out/combined-%.pdf: out 
	pdftk $(sort $(wildcard $(addprefix out/, $(subst .pdf, ,$(subst combined-, ,$(@F))))/*.pdf)) cat output $@

all: ${PDF_TARGETS}


.PHONY: clean
clean:
	rm out/ -rf
