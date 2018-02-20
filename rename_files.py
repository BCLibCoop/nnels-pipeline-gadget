import subprocess
import itertools
import data_structs as structs			
from BookFile import BookFile
from BookFileType import BookFileType

#----------------------------------------------------#
# Purpose: Create a filename regex based on the      #
#          patterns supplied at runtime with --files #
#          flag(s). Because the find command line    #
#          utility can only use one regex (in the    #
#          way I want) at once. So, I logical OR all #
#          the supplied 'patterns' together. I also  #
#          add a .*/ at the beginning if it doesn't  #
#          have it as my assumption is that the find #
#          utility is looking for filenames rather   #
#          than file paths consequently I prepend a  #
#          "ignore" expression for directories. I    #
#          may put some kind of mode parameter       #
#          to control this later but for now I think #
#          it works this way                         #
# Parameters: patterns - The patterns used to within #
#                        the regex                   #
# Return: string - The Regex that will be used in    #
#                  the find command                  #
#----------------------------------------------------#
def create_filename_regex(patterns):
	# Define the variable to store the final expression and start with a 
	# left a open brace
        exp = '(';
	
	# Loop over the 'patterns' supplied on the command line
        for pattern in patterns:
		# Check if it starts with the "ignore directories" expression
                if pattern.startswith('.*/'):
			# Because it has the "ignore directories" expression 
			# use as is
                        print 'Using original pattern: ' + pattern
                        exp += pattern + '|'
                else:
			# Because it doesn't have the "ignore directories" 
			# expression prepend that to the beginning
                        print 'Using augmented pattern: .*/' + pattern
                        exp += '.*/' + pattern + '|'
        
	# Remove the last character because it will be an extranous | character
	exp = exp[:len(exp) - 1]
	
	# Add a close brace to end the expression
	exp += ')'
	
	# Return the result
	return exp

#----------------------------------------------------#
# Purpose: To get all the filenames that fit the     #
#          specified patterns                        #
# Parameters: patterns - The pattern(s) to match the #
#                        filenames against           #
# Returns: List - A list of the applicable filenames #
#                 (including path)                   #
#----------------------------------------------------#
def getFileNames(patterns):
	# Prepare the arguments for a basic find command using regex (Extended 
	# regex)
        args = ['find', '-E', '.', '-regex']

        # Build the regex expression from the patterns supplied
        exp = create_filename_regex(patterns)

        # Add the built pattern to the find command arguments
        args.append(exp)

        # DEBUGGING: Just to see if the command was built right
        print args

        # Run the find command and get the results (See subprocess documentation
	# for more details)
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        # Get the lines of output as a list
        lines = stdout.decode('ascii').splitlines()
	
	# return the results
	return lines

#----------------------------------------------------#
# Purpose: Create a "combination token" which is     #
#          purely a combination of some subset (     #
#          including potentially the entire superset #
#          ) of tokens within a filename that should #
#          be recombined with seperating underscores #
#          (_)                                       #
# Parameters: set - A set of "tokens" (strings) that #
#                   should be recombined to form a   #
#                   "combination token"              #
# Return: String - the "combination token"           #
#----------------------------------------------------#
def createCombinationToken(set):
	# Create and initialize a variable for the "combination token"
	outputEntry = ''
	
	# Loop over list of entries/tokens in the set I need an index whih is 
	# why I'm using the 'in range' syntax rather than the purely 'in' syntax
        for x in range(0, len(set)):
		# Add the current entry to the "combination token'
        	outputEntry += set[x]
		
		# If this isn't the last token we're looking at add a underscore
                if x < len(set) - 1:
			outputEntry += '_'
	
        # DEBUGGING: See what the value of the "combination token" is
	print outputEntry
	
	# Return the value
	return outputEntry

#----------------------------------------------------#
# Purpose: Generate a list of all the possible       #
#          combinations that need to be checked if   #
#          they could be the SCN or the title        #
# Parameters: tokens - The tokens (strings)          #
#                      generated by seperating the   #
#                      filename by underscores (_)   #
# Return: List - All potential "combination tokens"  #
#                that need to be varified as a SCN   #
#                or title                            #
#----------------------------------------------------#
def do_combinations(tokens):
	print 'Do permutation stuff'
	
	# Generate all possible combinations using the itertools moduole
	superset = []
	for x in range(0, len(tokens)):
		superset.extend(list(itertools.combinations(tokens, x + 1)))
	
	# Previous step generates a list of lists rather than a list of strings
	# so need to recombine to put it back into the list of strings format
	outputSet = []
	for set in superset:
		outputSet.append(createCombinationToken(set))
	
	# Return the result
	return outputSet

#----------------------------------------------------#
# Purpose: Check if the potentially identified       #
#          title matches with the expected title as  #
#          queryed using the SCN as a key            #
# Parameters: scn - The scn that HAS been identified #
#             potential_title - The token you think  #
#                               is the title         #
# Return: N/A (To be reevaluated later)              #
#----------------------------------------------------#
def check_by_SCN(scn, potential_title):
	# DEBUGGING: Display that we've identified this as a SCN
	print scn + ' is a SCN'
	
	# Query the data structure to get the expected title for the SCN
	expectedTitle = structs.getTitle_fromSCN(scn)
	
	# Perform the check and respond appropriatly
	if expectedTitle == potential_title:
		print 'The filename matched the format SCN_title'
	else:
		print 'The filename is a format of SCN_ something (that is not the title because the title is ' + expectedTitle + ')'

#----------------------------------------------------#
# Purpose: Check if the potentially identified SCN   #
#          matches with the expected SCN as queryed  #
#          using the title as a key                  #
# Parameters: title - The title that HAS been        #
#                     identified                     #
#             potential_SCN - The token you think is #
#                             the SCN                #
# Return: N/A (To be reevaluated later)              #
#----------------------------------------------------#
def check_by_Title(title, potential_SCN):
	# DEBUGGING: Display that we've identified this as a title
	print title + ' is a Title'
	
	# Query the data structures to get the expected SCN for the title
	expectedSCN = structs.getSCN_fromTitle(title)
	
	# Perform the check and respond appropriately
	if expectedSCN == potential_SCN:
		print 'The filename match the format title_SCN'
	else:
		print 'The filename is a format of title_ something that is not the SCN'

#----------------------------------------------------#
# Purpose: 
# Parameters: 
# Return: 
#----------------------------------------------------#
def check_two_tokens(tokens, index1, index2 = None):
	if structs.hasSCN(tokens[index1]):
		if index2 is not None:
			check_by_SCN(tokens[index1], tokens[index2])
		else:
			print tokens[index1] + ' is a SCN'
	elif structs.hasTitle(tokens[index1]):
		if index2 is not None:
			check_by_title(tokens[index1], tokens[index2])
		else:
			print tokens[index1] + ' is a Title'
	else:
		print tokens[index1] + ' is neither a SCN or Title. Not sure what to do with this'

#-----------------------------------------------------#
# Purpose: 
# Parameter: 
# Return: 
#-----------------------------------------------------#
def check_combined_token(str1, str2):
	combined_token = str1 + '_' + str2
	
	if structs.hasSCN(str1 + '_' + str2):
		print str1 + '_' + str2 + ' is a SCN'
	elif structs.hasTitle(str1 + '_' + str2):
		print str1 + '_' + str2 + ' is a Title'
        else:
		print str1 + '_' + str2 + ' is neither a SCN or Title. Not sure what to do with this'

#----------------------------------------------------#
# Purpose: 
# Parameters: 
# Return: 
#----------------------------------------------------#
def zero_length_token_fix(tokens):
	
	for x in range(0, len(tokens)):
		# Check if token x is a/the empty entry
		if len(tokens[x]) < 1:
			tokens.remove(tokens[x])
	
        # Avoid edge case of a file named _.format and process the any/the 
	# token left
        if len(tokens) > 0:
		check_two_tokens(tokens, 0)

def process_two_tokens(tokens):
	# Nothing is stopping people to put a underscore at the beginning or 
	# end of a filename
	if len(tokens[0]) > 0 and len(tokens[1]) > 0:
		check_two_tokens(tokens, 0, 1)
		check_two_tokens(tokens, 1, 0)
		check_combined_token(tokens[0], tokens[1])
	else:
		zero_length_token_fix(tokens)

#----------------------------------------------------#
# Purpose: To tokenize the filename by unederscore   #
#          and process the tokens appropriatley      #
# Parameters: name - The filename to be tokenized    #
# Return: N/A (To be reevaluated later)
#----------------------------------------------------#
def tokenize_by_underscore(name):
	tokens = name.split('_')
	print 'Tokens: ' + str(tokens)
	# Need to check if we have to start trying to make permutations of 
	# multiple tokens or the simpler case
	if len(tokens) >  2:
		do_combinations(tokens)
	else:
		process_two_tokens(tokens)

#----------------------------------------------------#
# Purpose: Break the filename into meaningful peices
# Parameters: 
# Return: 
#----------------------------------------------------#
def get_name_parts(filename):
	# If the filename contains a do we want to tokenize it by that (know 
	# what the format is otherwise eliminate dealing with .blahblah files)
	if '.' in filename:
		filename_parts = filename.split('.')
		
		# If the filename started with a . then the first token has no 
		# length so lets just remove it
		if len(filename_parts[0]) < 1:
			filename_parts.remove(filename_parts[0])
		
		# There should now only be two parts the name and the format
		if len(filename_parts) == 2:
			# Check that the name actually has some length (mostly 
			# a sanity check but...)
			if len(filename_parts[0]) > 0:
				name = filename_parts[0]
				
				# Check if the filename contains a underscore be
				# cause this allows us to assume its either the 
				# title only or some combination of title and 
				# SCN
				if '_' in name:
					tokenize_by_underscore(name)
				else:
					check_two_tokens(filename_parts, 0)
				
				format = filename_parts[1]
                        #else:
                        #       print 'There is something odd about ' + line + 'because broken down it changes into' + str(parts)
	else:
		if len(filename) > 0:
			if '_' in filename:
				tokenize_by_underscore(filename)
			else:
				check_two_tokens([filename], 0)

def func_rename(patterns):
	# Get the applicable filenames
	lines = getFileNames(patterns)
	
	# Loop over the lines of output
	for line in lines:
		currBookType = BookFileType()
		currBook = BookFile(currBookType)
		
		# DEBUGGING: See what is being worked on
		print 'Currently processing: ' + line
		
		# If the filename is not in the current directory get rid of the directory information
		if '/' in line:
			path_parts = line.split('/')
			if len(path_parts) > 1:
				line = path_parts[len(path_parts) - 1]
		
		get_name_parts(line)

