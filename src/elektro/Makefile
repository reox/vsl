# This is a very generic Makefile to build all tex files in a subdirectory
.PHONY: clean combine all

TEX_SOURCES=$(wildcard */*.tex)
PDF_TARGETS=$(addprefix out/, $(TEX_SOURCES:.tex=.pdf))

all: ${PDF_TARGETS}
	$(MAKE) combine

out/%.pdf: %.tex
	latexmk -pdflatex=lualatex -pdf -output-directory=$(@D) $<

out/combined-%.pdf: out 
	pdftk $(sort $(wildcard $(addprefix out/, $(subst .pdf, ,$(subst combined-, ,$(@F))))/*.pdf)) cat output $@

combine: $(addsuffix .pdf, $(patsubst %/, %, $(subst out/, out/combined-,$(wildcard out/*/))))


clean:
	rm out/ -rf
