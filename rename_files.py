######################################################
# Purpose: Provide functionality for the rename      #
#          features within the program               #
# Author: Alan Bridgeman                             #
######################################################

import dynamic_loader as loader

loader.load_subprocess()
subprocess = loader.subprocess
#import subprocess

import itertools

loader.load_data_structs()
structs = loader.structs
#import data_structs as structs

import funcs
		
from BookFile import BookFile
from BookFileType import BookFileType, DAISY_Type, DAISY202_Type, DAISY3_Type, BookFileTypeFactory

DEBUG_MODE = False
OS = 'Mac' # Can be Mac or Linux
#----------------------------------------------------#
# Purpose: Because I use regular expressions instead #
#          of globbing (like the terminal) I thought #
#          it would make sense to try to correct if  #
#          someone tried to use globbing at least in #
#          the simplist form (ex. *.extension        #
#          becomes .*.extension)                     #
# Parameters: patterns - The patterns to evaluate    #
# Return: list/string/None - A list or value         #
#                            representing what the   #
#                            value for the           #
#                            prefix_each argument of #
#                            the combine_regex       #
#                            function should be or   #
#                            None if the prefix_each #
#                            argument should not be  #
#                            specified               #
#----------------------------------------------------#
def correct_for_globbing(patterns):
	# Fill an array of the same size as patterns with None for all values
	use_prefixs = [None for i in range(len(patterns))]
	
	# For each pattern see if it starts with a star (*) if so then check if 
	# it has a dot (.) next to it. If so we can correct with a dot (.) 
	# prefix
        for index in range(0, len(patterns)):
                if patterns[index].startswith('*'):
                        if '.' in patterns[index]:
                                tokens = patterns[index].split('.')
                                if len(tokens) == 2:
                                        if len(tokens[0]) == 1:
                                                use_prefixs[index] = '.'
	
	# Check if all prefixes are the same (None or the same value)
        all_prefixs_same = True
        for index in range(0, len(use_prefixs)):
                for index2 in range(0, len(use_prefixs)):
                        if use_prefixs[index] != use_prefixs[index2]:
                                all_prefixs_same = False
	
	# If they are all the same (arbitrarly) assign the first entry to be the
	# value of the variable. In other words change the type of the variable
        if all_prefixs_same:
                use_prefixs = use_prefixs[0]
	
	# Return the result
	return use_prefixs

#----------------------------------------------------#
# Purpose: To get all the filenames that fit the     #
#          specified patterns                        #
# Parameters: patterns - The pattern(s) to match the #
#                        filenames against           #
#             folder - The workspace directory/      #
#                      folder where all the relavent #
#                      files are kept                #
# Returns: List - A list of the applicable filenames #
#                 (including path)                   #
#----------------------------------------------------#
def get_file_names(patterns, folder):
	if DEBUG_MODE:
		print '===================================================='
		print 'Call Summary for get_file_names (rename_files.py)'
		print '----------------------------------------------------'
		print 'Patterns: ' + str(patterns)
		print 'Workspace: ' + str(folder)
		print '===================================================='
	
	# Prepare the arguments for a basic find command using regex (Extended 
	# regex)
	if OS == 'Mac':
        	args = ['find', '-E', folder, '-regex']
	elif OS == 'Linux':
		args = ['find', folder, '-regextype posix-extended', '-regex']
	
	use_prefixs = correct_for_globbing(patterns)
	
        # Build the regex expression from the patterns supplied
	if use_prefixs is not None:
        	exp = funcs.combine_regex(patterns, prefix_each=use_prefixs)
	else:
		exp = funcs.combine_regex(patterns)
	
        # Add the built pattern to the find command arguments
        args.append(exp)

        # DEBUGGING: Just to see if the command was built right
        #if DEBUG_MODE:
	print args

        # Run the find command and get the results (See subprocess documentation
	# for more details)
	if OS == 'Mac':
        	proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        elif OS == 'Linux':
		proc = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
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
	if DEBUG_MODE:
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
def get_combinations(tokens):
	if DEBUG_MODE:
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
def check_token(records, book, token):
	if DEBUG_MODE:
		print '===================================================='
        	print 'Call Summary for rename_files (rename_files.py) '
        	print '----------------------------------------------------'
        	print 'Records: ' + str(records)
		print 'Book: ' + str(book)
        	print 'Token: ' + str(token)
        	print '===================================================='
	
	# Check if the current token matches a SCN
	if structs.has_SCN(records, token):
		metadata_record = structs.get_item_with_attr(records, 'SCN', token)
		# Now that we know the token matches A SCN lets check if its 
		# the proper one if we can
		if book.title is not None:
			if metadata_record.title == book.title:
				if DEBUG_MODE:
					print 'Setting the SCN: ' + token
				# Sinc it matched set it in the book object
				book.SCN = token
			else:
				# Since it didn't match let the user know and 
				# move on
				if DEBUG_MODE:
					print 'Skipping SCN ' + token + ' because it does not match with identified title ' + book.title
		else:
			if DEBUG_MODE:
				print 'Setting the SCN: ' + token
			# Because we don't yet know the title assume this is 
			# the right SCN
			book.SCN = token
	# Check if the current token matches a title
	elif structs.has_title(records, token):
		metadata_record = structs.get_item_with_attr(records, 'title', token)
		# Now that we know the token matches A title lets check if its 
		# the propery one if we can
		if book.SCN is not None:
			if metadata_record.SCN == book.SCN:
				if DEBUG_MODE:
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
			if DEBUG_MODE:
				print 'Changed book type to ' + str(bookType)

#----------------------------------------------------#
# Purpose: 
# Parameters: 
# Return: 
#----------------------------------------------------#
def zero_length_token_fix(records, book, tokens):
	if DEBUG_MODE:
		print '===================================================='
        	print 'Call Summary for zero_length_token_fix (rename_files.py) '
        	print '----------------------------------------------------'
		print 'Records: ' + str(records)
        	print 'Book: ' + str(book)
        	print 'Tokens: ' + str(tokens)
        	print '===================================================='
	
	# Loop over each of the tokens to check their length
	for x in range(0, len(tokens)):
		# Check if token x is a/the empty entry
		if len(tokens[x]) < 1:
			tokens.remove(tokens[x])
	
        # Avoid edge case of a file named _.format and process the any/the 
	# token left
        if len(tokens) > 0:
		check_token(records, book, tokens[0])

def process_two_tokens(records, book, tokens):
	if DEBUG_MODE:
		print '===================================================='
        	print 'Call Summary for process_two_tokens (rename_files.py) '
        	print '----------------------------------------------------'
		print 'Records: ' + str(records)
        	print 'Book: ' + str(book)
        	print 'Tokens: ' + str(tokens)
        	print '===================================================='
	
	# Nothing is stopping people to put a underscore at the beginning or 
	# end of a filename
	if len(tokens[0]) > 0 and len(tokens[1]) > 0:
		check_token(records, book, tokens[0])
		check_token(records, book, tokens[1])
		check_token(records, book, tokens[0] + '_' + tokens[1])
	else:
		zero_length_token_fix(records, book, tokens)

#----------------------------------------------------#
# Purpose: To tokenize the filename by unederscore   #
#          and process the tokens appropriatley      #
# Parameters: name - The filename to be tokenized    #
# Return: N/A (To be reevaluated later)
#----------------------------------------------------#
def tokenize_by_underscore(records, book, name):
	if DEBUG_MODE:
		print '===================================================='
        	print 'Call Summary for tokenize_by_underscore (rename_files.py) '
        	print '----------------------------------------------------'
		print 'Recoreds: ' + str(records)
        	print 'Book: ' + str(book)
        	print 'Name: ' + str(name)
        	print '===================================================='
	
	tokens = name.split('_')
	
	if DEBUG_MODE:
		print 'Tokens: ' + str(tokens)
	
	# Need to check if we have to start trying to make permutations of 
	# multiple tokens or the simpler case
	if len(tokens) >  2:
		combos = get_combinations(tokens)
		for combo in combos:
			check_token(records, book, combo)
	else:
		process_two_tokens(records, book, tokens)

#----------------------------------------------------#
# Purpose: Break the filename into meaningful peices
# Parameters: 
# Return: 
#----------------------------------------------------#
def get_name_parts(records, book):
	if DEBUG_MODE:
		print '===================================================='
        	print 'Call Summary for rename_files (rename_files.py) '
        	print '----------------------------------------------------'
        	print 'Book: ' + str(book)
        	print '===================================================='
	
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
			if DEBUG_MODE:
				print bookType
		
		# Check that the name actually has some length (mostly 
		# a sanity check but...)
		if len(filename_parts[0]) > 0:
			name = filename_parts[0]
			
			# Check if the filename contains a underscore because 
			# this allows us to assume its either the title only 
			# or some combination of title and SCN
			if '_' in name:
				tokenize_by_underscore(records, book, name)
			else:
				check_token(records, book, filename_parts[0])
		else:
			print 'The filename seems to be unreadable (has no length)'
	else:
		if len(book.filename) > 0:
			if '_' in book.filename:
				tokenize_by_underscore(records, book, book.filename)
			else:
				check_token(records, book, book.filename)

#----------------------------------------------------#
# Purpose: Create a list of book objects from the    #
#          patterns provided at the command line     #
# Parameters: patterns - The patterns to use to get  #
#                        the files that will be      #
#                        represented in the book     #
#                        objects contained in the    #
#                        list                        #
#             folder - The workspace directory/      #
#                      folder where all the relavent #
#                      files are kept                #
# Return: list - A list of the book objects to be    #
#                processed                           #
#----------------------------------------------------#
def create_booklist(patterns, folder):
	if DEBUG_MODE:
		print '===================================================='
		print 'Call Summary for create_booklist (rename_files.py) '
		print '----------------------------------------------------'
		print 'Patterns: ' + str(patterns)
		print 'Workspace: ' + str(folder)
		print '===================================================='
	
	# A list variable to hold the reults
	booklist = []
	
	# Get the list of files with the given patterns
	files = get_file_names(patterns, folder)
	
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
	if DEBUG_MODE:
		print '===================================================='
        	print 'Call Summary for get_book_filename (rename_files.py) '
        	print '----------------------------------------------------'
        	print 'Book: ' + str(book)
        	print '===================================================='
	
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

#----------------------------------------------------#
# Purpose: To generate the new (desired) filename    #
# Parameters: book - The book object to generate the #
#                    new (desired) filename for      #
# Return: string - The new (desired) filename        #
#----------------------------------------------------#
def _generate_new_file_name(book):
        # Set the return variable to None initially
        return_result = None

        # Get the extension of the book file
        file_ext = book.filename.split('.')[len(book.filename.split('.')) - 1]

        # Get the length of the filename (used for extracting the folder info)
        file_name_length = len(book.filename)

        # Extract the folder information from the book's fullpath
        return_result = book.fullpath[:-file_name_length]

        # Generate that desired title_SCN format that was desired
        return_result += book.title + '_' + book.SCN

        # If its a DAISY book put the appropriate suffix at the end of the
        # filename
        if isinstance(book.type, DAISY_Type):
                if isinstance(book.type, DAISY202_Type):
                        return_result += '_DAISY202'
                elif isinstance(book.type, DAISY3_Type):
                        return_result += '_DAISY3'

        # Add the file extenstion (.type) to theend of the file name
        return_result += '.' + file_ext

        # Return the result
        return return_result

#----------------------------------------------------#
# Purpose: Trigger method for starting the renaming  #
#          of files funtionality                     #
# Parameters: patterns - A list of regular           #
#                        expression "patterns" to    #
#                        identify book files         # 
#             folder - The workspace directory/      #
#                      folder where all the relavent #
#                      files are kept                #
# Return: N/A                                        #
#----------------------------------------------------#
def rename_files(records, patterns, folder='.'):
	if DEBUG_MODE:
		print '===================================================='
		print 'Call Summary for rename_files (rename_files.py) '
		print '----------------------------------------------------'
		print 'Patterns: ' + str(patterns)
		print 'Workspace: ' + str(folder)
		print '===================================================='
	
	# Get a list of books
	books = create_booklist(patterns, folder)
	
	renames = {}
	
	# Loop over the list of books
	for book in books:
		# Set the book's filename (remove directory info)
		book.filename = get_book_filename(book)
		
		renames[book.filename] = None
		
		# 
		get_name_parts(records, book)
	
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
				print 'Result of call is: ' + str(metadata)
			else:
				print book.filename + ' seems to be a bit of a mystory'
		
		if book.SCN is not None:
			if book.title is None:
				book.title = structs.get_item_with_attr(records, 'SCN', book.SCN).title
		if book.title is not None:
			if book.SCN is None:
				book.SCN = structs.get_item_with_attr(records, 'title', book.title).SCN
		if book.SCN is not None and book.title is not None:
			renames[book.fullpath] = _generate_new_file_name(book)
	
	# Return the resulrt
	return renames
