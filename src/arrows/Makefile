SVG_FILES := $(wildcard *.svg)
PDF_FILES := $(SVG_FILES:.svg=.pdf)

PDF_NUP_FILES := $(PDF_FILES:.pdf=-quad-nup.pdf)
PDF_QUAD_FILES := $(PDF_FILES:.pdf=-quad.pdf)

PDF_NUP_NINE_FILES := $(PDF_FILES:.pdf=-nine-nup.pdf)
PDF_NINE_FILES := $(PDF_FILES:.pdf=-nine.pdf)

%.pdf: %.svg
	inkscape --export-pdf=$@ $<

%-quad.pdf: %.pdf
	pdftk $< $< $< $< cat output $@

%-quad-nup.pdf: %-quad.pdf
	pdfnup --nup 2x2 --no-landscape $<

%-nine.pdf: %.pdf
	pdftk $< $< $< $< $< $< $< $< $< cat output $@

%-nine-nup.pdf: %-nine.pdf
	pdfnup --nup 3x3 --no-landscape $<

arrows_for_print.pdf: ${PDF_FILES} ${PDF_NUP_FILES} ${PDF_NUP_NINE_FILES} 
	pdftk $^ cat output $@

all: arrows_for_print.pdf

.PHONY: clean
clean:
	rm ${PDF_FILES} arrows_for_print.pdf ${PDF_NUP_FILES} ${PDF_QUAD_FILES} ${PDF_NUP_NINE_FILES} ${PDF_NINE_FILES} || exit 0
