all: sign_text.pdf

%.pdf: %.tex
	xelatex $<

show: all
	evince sign_text.pdf
