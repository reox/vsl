OUTPUT_DIR_ROOMS=out_rooms

TEX_FILES_ROOMS := $(wildcard rooms/*.tex)
PDF_FILES_ROOMS := $(addprefix ${OUTPUT_DIR_ROOMS}/,$(notdir $(TEX_FILES_ROOMS:.tex=.pdf)))

all: gen_rooms ${PDF_FILES_ROOMS} merge_pdf

check_dirs:
	[ -d ${OUTPUT_DIR_ROOMS} ] ||  mkdir ${OUTPUT_DIR_ROOMS}

gen_rooms:
	./room_gen.sh

merge_pdf:
	pdftk ${PDF_FILES_ROOMS} cat output all_rooms.pdf

${OUTPUT_DIR_ROOMS}/%.pdf: rooms/%.tex
	xelatex -output-directory=${OUTPUT_DIR_ROOMS} $<

.PHONY : clean check_dirs rem_auxlog
clean:
	rm ${PDF_FILES_ROOMS}
