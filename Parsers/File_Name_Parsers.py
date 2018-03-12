#=====================================================# 
# Purpose:
# Properties: records - The records to compare        #
#                       against                       #
#             file_list - The list of files to parse  #
#                         the filename of             #
# Method: 
#=====================================================#
class File_Name_Parser(object):
	
	#----------------------------------------------------#
	# PUrpose: 
	# Parameters: 
	# Return: 
	#----------------------------------------------------#
	def __init__(self, records, file_list):
		self.records = records
		self.files = file_list
	
	#----------------------------------------------------#
	# Purpose: Check the provieded token for matches     #
	#          with SCNs and titles                      #
	# Parameters: book - The book object being processed #
	#             token - The token to be checked        #
	#                     against                        #
	# Return: N/A                                        #
	#----------------------------------------------------#
	def parse_token(has_type, token):
		if DEBUG_MODE:
			print '===================================================='
			print 'Call Summary for rename_files (rename_files.py) '
			print '----------------------------------------------------'
			print 'Records: ' + str(records)
			print 'Book: ' + str(book)
			print 'Token: ' + str(token)
			print '===================================================='
		
		return_result = {}
		
		# Check if the current token matches a SCN
		if structs.has_SCN(records, token):
			call_return = check_SCN(self.ecords, book, token)
			if isinstance(call_return, dict)
				for k,v in call_return.iteritems():
					return_result[k] = v
		# Check if the current token matches a title
        	elif structs.has_title(records, token):
                	metadata_record = structs.get_item_with_attr(self.records, 'title', token)
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
                        return_result['type'] = bookType
                        if DEBUG_MODE:
                                print 'Changed book type to ' + str(bookType)
		
		return return_result
	
	#----------------------------------------------------#
	# Purpose: Parse the filename into meaningful peices
	# Parameters:
	# Return:
	#----------------------------------------------------#
	def parse(filename):
		if DEBUG_MODE:
			print '===================================================='
			print 'Call Summary for rename_files (rename_files.py) '
			print '----------------------------------------------------'
			print 'Book: ' + str(book
			print '===================================================='
		
		return_result = {}
		
		# If the filename contains a dot we want to tokenize it by that
		# (know what the format is otherwise eliminate dealing with 
		# .blahblah files)
		if '.' in filename:
			filename_parts = book.filename.split('.')
		
		# If the filename started with a . then the first token has no
		# length so lets just remove it
		if not filename_parts and len(filename_parts[0]) < 1:
			filename_parts.remove(filename_parts[0])
		
		# If there are EXACTLY two tokens assume the second token is 
		# the format/extension
		if len(filename_parts) == 2:
			format = filename_parts[1]
			bookType = BookFileTypeFactory.getExtensionType(format)
			if bookType is not None:
				return_result['type'] = bookType
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
				call_return = parse_token(book, filename_parts[0])
				if isinstance(call_return, dict):
					for k,v in call_return.iteritems():
						return_result[k] = v
		else:
			print 'The filename seems to be unreadable (has no length)'
	else:
		if len(book.filename) > 0:
                        if '_' in book.filename:
                                tokenize_by_underscore(records, book, book.filename)
                        else:
                                call_return = parse_token(book, book.filename)
				if isinstance(call_return, dict):
					for k,v in call_return.iteritems():
						return_result[k] = v
		
		return return_result
