
#
# Compile javascript using
# google closure compiler
# https://developers.google.com/closure/compiler/docs/gettingstarted_app
#

# Location of closure jar
COMPILER_JAR='/usr/local/closure-compiler/build/compiler.jar'
COMPILER_LIB='/usr/local/closure-library/'
CALC_DEPS=${COMPILER_LIB}/closure/bin/calcdeps.py

# List the sources
SRCS = common.js login.js new_user.js create_beef.js get_beef.js

# Create the list of targets by
# doing a simple string suffix replace
TARGETS = $(SRCS:.js=-compiled.js)


all: $(TARGETS)

# 	${CALCDEPS} -i get_beef.js -p /usr/local/closure-library -o script > get_beef-calc.js	

# A single example
common-compiled: common.js
	cat $< | sed -E 's/console.(log|debug|info|count)\((.*)\);?//g' >common_temp.js	
	java -jar ${COMPILER_JAR} --js  common_temp.js --js_output_file $@.js
	rm common_temp.js

# Compile using a rule:
# Create %-compiled.js, 
# which depends on %.js
# Recall: 
#   % represents the matched string
#   $@ is the target (ie common-compiled.js)
#   $< is the dependency (ie common.js)
%-compiled.js: %.js
	cat $< | sed -E 's/console.(log|debug|info|count)\((.*)\);?//g' >%_temp.js	
	java -jar ${COMPILER_JAR} --js %_temp.js --js_output_file $@
	rm %_temp.js

.PHONY: clean

clean:
	rm -f *_temp.js
	rm -f $(TARGETS)




#production: common-compiled.js
