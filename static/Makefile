

#
# Compile javascript using
# google closure compiler
# https://developers.google.com/closure/compiler/docs/gettingstarted_app
#


COMPILER_JAR='/usr/local/closure-compiler/build/compiler.jar'

all:	common.js login.js get_beef.js new_user.js create_beef.js	
	 java -jar ${COMPILER_JAR} --js $@ --js_output_file beef-compiled.js	
	

$(CC) -c $(CPPFLAGS) $(CFLAGS)