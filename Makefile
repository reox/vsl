### hint hint hint
# $@ is the target file
# $< is the input file
# see also here:
# http://www.gnu.org/software/make/manual/make.html#Automatic-Variables
# rules are based on target: source; receipe
#

# DIRS contains a list of src dirs, that can be compiled into pdfs
# Each dir that contains compileable stuff need to have its own makefile
DIRS =$(filter %/, $(wildcard src/*/))
LIB_DIRS  =$(DIRS:%/=%)
DIRS_CMD  =$(foreach subdir, $(LIB_DIRS), make-rule/$(subdir))

# this psuedo make rule is necessary to build everything correctly
make-rule/%:
	@echo "making rule"
	cd $* && $(MAKE)

all: ${DIRS_CMD}
