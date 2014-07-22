# This is a very generic Makefile to build all tex files in a subdirectory
.PHONY: clean combine all

TEX_SOURCES=$(wildcard */*.tex)
PDF_TARGETS=$(addprefix out/, $(TEX_SOURCES:.tex=.pdf))

all: ${PDF_TARGETS}
	rm out/combined-* || exit 0
	$(MAKE) combine

out/%.pdf: %.tex
	latexmk -pdflatex=lualatex -pdf -output-directory=$(@D) $<

out/combined-%.pdf: out 
	pdftk $(sort $(filter-out out/combined-*.pdf, $(wildcard $(addprefix out/, $(subst .pdf, ,$(subst combined-, ,$(@F))))/*.pdf))) cat output $@

combine: $(addsuffix .pdf, $(patsubst %/, %, $(subst out/, out/combined-,$(filter-out *.pdf, $(wildcard out/*/)))))

clean:
	rm out/ -rf
