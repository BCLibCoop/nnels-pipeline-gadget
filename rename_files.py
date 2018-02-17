import subprocess
import data_structs as structs

def func_rename(patterns):
	# Prepare the arguments for a basic find command using regex
	args = ['find', '-E', '.', '-regex']
	
	# Build the regex expression from the patterns supplied
	exp = '(';
	for pattern in patterns:
		if pattern.startswith('.*/'):
			print 'Using original pattern: ' + pattern
			exp += pattern + '|'
		else:
			print 'Using augmented pattern: .*/' + pattern
			exp += '.*/' + pattern + '|'
	exp = exp[:len(exp) - 1] + ')'
	
	# Add the built pattern to the find command arguments
	args.append(exp)
	
	# DEBUGGING: Just to see if the command was built right
	print args
	
	# Run the find command and get the results (See subprocess documentation for more details)
	proc = subprocess.Popen(args, stdout=subprocess.PIPE)
	stdout, stderr = proc.communicate()
	
	# Get the lines of output as a list
	lines = stdout.decode('ascii').splitlines()
	
	# Loop over the lines of output
	for line in lines:
		
		# DEBUGGING: See what is being worked on
		print 'Currently processing: ' + line
		
		# If the filename is not in the current directory get rid of the directory information
		if '/' in line:
			path_parts = line.split('/')
			if len(path_parts) > 1:
				line = path_parts[len(path_parts) - 1]
		
		# If the filename contains a do we want to tokenize it by that (know what the format is otherwise eliminate dealing with .blahblah files)
		if '.' in line:
			filename_parts = line.split('.')
			
			# If the filename started with a . then the first token has no length so lets just remove it
			if len(filename_parts[0]) < 1:
				filename_parts.remove(filename_parts[0])
			
			# There should now only be two parts the name and the format
			if len(filename_parts) == 2:
				# Check that the name actually has some length (mostly a sanity check but...)
				if len(filename_parts[0]) > 0:
					name = filename_parts[0]
					
					# Check if the filename contains a underscore because this allows us to assume its either the title only or some combination of title and SCN
					if '_' in name:
						tokens = name.split('_')
						print 'Tokens: ' + str(tokens)
						# Need to check if we have to start trying to make permutations of multiple tokens or the simpler case
						if len(tokens) >  2:
							print 'Do permutation stuff'
						else:
							# Nothing is stopping people to put a underscore at the beginning or end of a filename
							if len(tokens[0]) > 0 and len(tokens[1]) > 0:
								print 'Need to implement'
								if structs.hasSCN(tokens[0]):
									print tokens[0] + ' is a SCN'
								elif structs.hasTitle(tokens[1]):
									print tokens[0] + ' is a Title'
								else:
									print tokens[0] + ' is neither a SCN or Title. Not sure what to do with this'
								
								if structs.hasSCN(tokens[1]):
									print tokens[1] + ' is a SCN'
								elif structs.hasTitle(tokens[1]):
									print tokens[1] + ' is a Title'
								else:
									print tokens[1] + ' is neither a SCN or Title. Not sure what to do with this'
								
								combined_token = tokens[0] + '_' + tokens[1]
								
								if structs.hasSCN(tokens[0] + '_' + tokens[1]):
									print tokens[0] + '_' + tokens[1] + ' is a SCN'
								elif structs.hasTitle(tokens[0] + '_' + tokens[1]):
									print tokens[0] + '_' + tokens[1] + ' is a Title'
								else:
									print tokens[0] + '_' + tokens[1] + ' is neither a SCN or Title. Not sure what to do with this'
							else:
								# Check if token 0 is a/the empty entry
								if len(tokens[0]) < 1:
									tokens.remove(tokens[0])
								
								# Check if token 1 is a/the empty entry
								if len(tokens[1]) < 1:
									tokens.remove(tokens[1])
								
								# Edge case of avoiding a file named _.format
								if len(tokens) > 0:
									if structs.hasSCN(tokens[0]):
										print tokens[0] + ' is a SCN'
									elif structs.hasTitle(tokens[0]):
										print tokens[0] + ' is a Title'
									else:
										print tokens[0] + ' is neither a SCN or Title. Not sure what to do with this'
					else:
						if structs.hasSCN(filename_parts[0]):
							print filename_parts[0] + ' is a SCN'
						elif structs.hasTitle(filename_parts[0]):
							print filename_parts[0] + ' is a Title'
						else:
							print filename_parts[0] + ' is neither a SCN or Title. Not sure what to do with this'
					format = filename_parts[1]
			#else:
			#	print 'There is something odd about ' + line + 'because broken down it changes into' + str(parts)

