
#
# Compile javascript using
# google closure compiler
# https://developers.google.com/closure/compiler/docs/gettingstarted_app
#

COMPILE_DIR=compiled/

# Location of closure jar
COMPILER_JAR=/usr/local/closure-compiler/build/compiler.jar

# List the sources
SRCS = common.js login.js new_user.js create_beef.js get_beef.js

# Create the list of targets by
# doing a simple string suffix replace
#TARGET_NAMES = $(SRCS:.js=-compiled.js)
TARGETS=$(addprefix ${COMPILE_DIR},${SRCS})

all: $(TARGETS)

# Compile using a rule:
# Create %-compiled.js, 
# which depends on %.js
# Recall: 
#   % represents the matched string
#   $@ is the target (ie common-compiled.js)
#   $< is the dependency (ie common.js)
${COMPILE_DIR}%.js: %.js
	cat $< | sed -E 's/console.(log|debug|info|count)\((.*)\);?//g' >${COMPILE_DIR}$*_temp.js
	java -jar ${COMPILER_JAR} --js ${COMPILE_DIR}$*_temp.js --js_output_file $@
	rm ${COMPILE_DIR}$*_temp.js	

.PHONY: clean

clean:
	rm -f *_temp.js
	rm -f $(TARGETS)


# A single example
#common-compiled: common.js
#	cat $< | sed -E 's/console.(log|debug|info|count)\((.*)\);?//g' >common_temp.js	
#	java -jar ${COMPILER_JAR} --js  common_temp.js --js_output_file $@.js
#	rm common_temp.js


#CLOSURE_LIB='/usr/local/closure-library/'
#CALC_DEPS=${CLOSURE_LIB}/closure/bin/calcdeps.py
#
#%-compiled-deps.js: %.js
#	cat $< | sed -E 's/console.(log|debug|info|count)\((.*)\);?//g' >temp.js
#	${CALC_DEPS} -i temp.js -p ${CLOSURE_LIB} -c ${COMPILER_JAR} -o compiled > $@
#	java -jar ${COMPILER_JAR} --js temp.js --js_output_file $@
#	rm %_temp.js

#production: common-compiled.js
