SVG_FILES := $(wildcard *.svg)
PDF_FILES := $(SVG_FILES:.svg=.pdf)

%.pdf: %.svg
	inkscape --export-pdf=$@ $<

arrows_for_print.pdf: ${PDF_FILES} 
	pdftk ${PDF_FILES} cat output $@

all: arrows_for_print.pdf
