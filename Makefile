OBJECTS=sign_text.pdf sign_door.pdf

all: ${OBJECTS}

%.pdf: %.tex
	xelatex $<

show: all
	evince sign_text.pdf

.PHONY : clean
clean:
	rm ${OBJECTS}
