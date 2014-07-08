### hint hint hint
# $@ is the target file
# $< is the input file
# see also here:
# http://www.gnu.org/software/make/manual/make.html#Automatic-Variables
# rules are based on target: source; receipe
#

# DIRS contains a list of src dirs, that can be compiled into pdfs
# Each dir that contains compileable stuff need to have its own makefile
SUB_MAKEFILES = $(wildcard src/*/Makefile)
DIRS = $(SUB_MAKEFILES:%/Makefile=%)
DIRS_CMD  =$(foreach subdir, $(DIRS), make-rule/$(subdir))
DIRS_CMD_CLEAN  =$(foreach subdir, $(DIRS), make-rule-clean/$(subdir))

# this psuedo make rule is necessary to build everything correctly
make-rule/%:
	cd $* && $(MAKE)

make-rule-clean/%:
	cd $* && $(MAKE) clean

ROOMS_TEX = $(wildcard rooms/*.tex)
ROOMS_TEX_NAMES = $(ROOMS_TEX:rooms/%=%)
ROOMS_PDF = $(foreach outdir, $(ROOMS_TEX_NAMES:.tex=.pdf), out_rooms/$(outdir))

all_rooms.pdf: ${ROOMS_PDF}
	pdftk $(sort $^) cat output $@

out_rooms/%.pdf: rooms/%.tex
	latexmk -pdflatex=lualatex -pdf -output-directory=$(@D) $<

all: ${DIRS_CMD}

clean: ${DIRS_CMD_CLEAN}
	rm all_rooms.pdf
	rm out_rooms/*

test.pdf: all
	pdftk $(wildcard src/*/out/*/*.pdf) cat output $@
