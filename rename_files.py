######################################################
# Purpose: Provide functionality for the rename      #
#          features within the program               #
# Author: Alan Bridgeman                             #
######################################################

import subprocess
import itertools
import data_structs as structs			
from BookFile import BookFile
from BookFileType import BookFileType, BookFileTypeFactory

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
	#print outputEntry
	
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
def get_combinations(tokens):
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
# Purpose: Check the provieded token for matches     #
#          with SCNs and titles                      #
# Parameters: book - The book object being processed #
#             token - The token to be checked        #
#                     against                        #
# Return: N/A                                        #
#----------------------------------------------------#
def check_token(book, token):
	# Check if the current token matches a SCN
	if structs.hasSCN(token):
		# Now that we know the token matches A SCN lets check if its 
		# the proper one if we can
		if book.title is not None:
			if token == getSCN_fromTitle(book.title):
				print 'Setting the SCN: ' + token
				# Since it matched set it in the book object
				book.SCN = token
			else:
				# Since it didn't match let the user know and move on
				print 'Skipping SCN ' + token + ' because it does not match with identified title ' + book.title
		else:
			print 'Setting the SCN: ' + token
			# Because we don't yet know the title assume this is 
			# the right SCN
			book.SCN = token
	# Check if the current token matches a title
	elif structs.hasTitle(token):
		# Now that we know the token matches A title lets check if its 
		# the propery one if we can
		if book.SCN is not None:
			if token == structs.getTitle_fromSCN(book.SCN):
				print 'Setting the title: ' + token
				# Since it matched set it in the book object
				book.title = token
			else:
				# Since it didn't match let the user know and move on
				print 'Skipping title ' + token + ' because it does not match with identified SCN ' + book.SCN
		else:
			print 'Setting the title: ' + token
			# Because we don't yet know the SCN assume this is the 
			# right title
			book.title = token
	elif book.type is None:
		factory = BookFileTypeFactory()
		bookType = factory.getStringType(token) 
		if bookType is not None:
			book.type = bookType
			print 'Changed book type to ' + str(bookType)

#----------------------------------------------------#
# Purpose: 
# Parameters: 
# Return: 
#----------------------------------------------------#
def zero_length_token_fix(book, tokens):
	# Loop over each of the tokens to check their length
	for x in range(0, len(tokens)):
		# Check if token x is a/the empty entry
		if len(tokens[x]) < 1:
			tokens.remove(tokens[x])
	
        # Avoid edge case of a file named _.format and process the any/the 
	# token left
        if len(tokens) > 0:
		check_token(book, tokens[0])

def process_two_tokens(book, tokens):
	# Nothing is stopping people to put a underscore at the beginning or 
	# end of a filename
	if len(tokens[0]) > 0 and len(tokens[1]) > 0:
		check_token(book, tokens[0])
		check_token(book, tokens[1])
		check_token(book, tokens[0] + '_' + tokens[1])
	else:
		zero_length_token_fix(book, tokens)

#----------------------------------------------------#
# Purpose: To tokenize the filename by unederscore   #
#          and process the tokens appropriatley      #
# Parameters: name - The filename to be tokenized    #
# Return: N/A (To be reevaluated later)
#----------------------------------------------------#
def tokenize_by_underscore(book, name):
	tokens = name.split('_')
	print 'Tokens: ' + str(tokens)
	
	# Need to check if we have to start trying to make permutations of 
	# multiple tokens or the simpler case
	if len(tokens) >  2:
		combos = get_combinations(tokens)
		for combo in combos:
			check_token(book, combo)
	else:
		process_two_tokens(book, tokens)

#----------------------------------------------------#
# Purpose: Break the filename into meaningful peices
# Parameters: 
# Return: 
#----------------------------------------------------#
def get_name_parts(book):
	# If the filename contains a do we want to tokenize it by that (know 
	# what the format is otherwise eliminate dealing with .blahblah files)
	if '.' in book.filename:
		filename_parts = book.filename.split('.')
		
		# If the filename started with a . then the first token has no 
		# length so lets just remove it
		if len(filename_parts[0]) < 1:
			filename_parts.remove(filename_parts[0])
		
		# If there are EXACTLY two tokens assume the second token is the
                # format/extension
		if len(filename_parts) == 2:
                        format = filename_parts[1]
                        bookType = BookFileTypeFactory.getExtensionType(format)
                        if bookType is not None:
				book.type = bookType
			print bookType
		
		# Check that the name actually has some length (mostly 
		# a sanity check but...)
		if len(filename_parts[0]) > 0:
			name = filename_parts[0]
			
			# Check if the filename contains a underscore be
			# cause this allows us to assume its either the 
			# title only or some combination of title and 
			# SCN
			if '_' in name:
				tokenize_by_underscore(book, name)
			else:
				check_token(book, filename_parts[0])
		else:
			print 'The filename seems to be unreadable'
	else:
		if len(book.filename) > 0:
			if '_' in filename:
				tokenize_by_underscore(book.filename)
			else:
				check_token(book, book.filename)

#----------------------------------------------------#
# Purpose: Create a list of book objects from the    #
#          patterns provided at the command line     #
# Parameters: patterns - The patterns to use to get  #
#                        the files that will be      #
#                        represented in the book     #
#                        objects contained in the    #
#                        list                        #
# Return: list - A list of the book objects to be    #
#                processed                           #
#----------------------------------------------------#
def create_booklist(patterns):
	# A list variable to hold the reults
	booklist = []
	
	# Get the list of files with the given patterns
	files = getFileNames(patterns)
	
	# Loop over the list of files and create a new book object for each
	for currFile in files:
		currBook = BookFile()
		currBook.fullpath = currFile
		
		# Add the newly created book object to the list
		booklist.append(currBook)
	
	# Return the result
	return booklist

#----------------------------------------------------#
# Purpose: Get the books filename (filename without  #
#          directory)                                #
# Parameters: book - The current book being          #
#                    processed                       #
# Return: string - The books filename (without       #
#                  directory information)            #
#----------------------------------------------------#
def get_book_filename(book):
	# Create a variable for the result that will be returned
	book_filename = None
	
	# Check if there is a / character in the fullpath of the book
	if '/' in book.fullpath:
		# Tokenize/split the path using the / as a delimiter
		path_parts = book.fullpath.split('/')
		
		# Check if there is more than one token/substring after the 
		# split
		if len(path_parts) > 1:
			# Set the result to be the the last token in the set 
			# (the text after the last /)
			book_filename = path_parts[len(path_parts) - 1]
	
	# Check if the result variable is still None
	if book_filename == None:
		# Because it wasn't set assume that the filename and path are 
		# the same
		book_filename = book.fullpath
	
	# Return the result
	return book_filename

def func_rename(patterns):
	# Get a list of books
	books = create_booklist(patterns)
	
	# Loop over the list of books
	for book in books:
		# Set the book's filename (remove directory info)
		book.filename = get_book_filename(book)
		
		# 
		get_name_parts(book)
	
	for book in books:
		# DEBUGGING: Print a summary of the information we have
		print '|----------------------------------------------------|'
		print '| BOOK SUMMARY'
		print '| ============'
		print '| File Path: ' + str(book.fullpath)
		print '| File Name: ' + str(book.filename)
		print '| Book SCN: ' + str(book.SCN)
		print '| Book Title: ' + str(book.title)
		print '| Book Type: ' + str(book.type)
		print '|----------------------------------------------------|'
		
		# Check if there was enough information or if further
		# investigation is required
		if book.SCN is None and book.title is None:
			# Checck if the book has a type
			if book.type is not None:
				# Get the metadata from the actual file based
				# on its type
				metadata = book.type.get_metadata(book.fullpath)
				
				# DEBUGGING: Print the result of the file 
				#            metadata extraction
				print metadata
				
				# Check if the title is specified in the 
				# metadata (which is the mostly likely 
				# consistant element across all the file types 
				# and this system)
				if metadata['title'] is not None:
					# DEBUGGING: Print statement for 
					#            getting an inital title
					#            value before any
					#            processing
					print 'Should set the title to: ' + metadata['title']
					# Assign to a secondary variable (just
					# so that we have a way to still get the
					# original if needed
					title = metadata['title']
					
					# Remove special characters (NOTE: 
					# was required addition of u'\u2019' for
					# removing single quote)
        				specialchars = [",", ":", ".", "'", u'\u2019', "?", "&", "/"]
        				for char in specialchars:
                				title = title.replace(char, "")
				
        				# Strip any extranous whitespace
        				title = title.strip()
					
        				# Underscore remaining whitespace
        				title = title.replace(" ", "_")
					
					# Capatilize the first letter only
					title = title.lower()
					title = title[:1].upper() + title[1:]
					
					# DEBUGGING: Print the resultant title 
					#            after processing
					print 'Title to use: ' + title
					
					# Set the book object's title to be the 
					# title from the metadata after
					# processing
					book.title = title
					
					# DEBUGGING: Print the book Object's 
					#            title to make sure it works
					print 'Did set the title to: ' + str(book.title)
					
					# Confirm the change took
					if book.title is not None:
						print 'Chaned the title to ' + book.title
			else:
				print book.filename + ' seems to be a bit of a mystory'
