import click
import os
from rename_files import rename_files

#----------------------------------------------------#
# Purpose: To provide the Command Line Interface     #
#          (CLI) for the rename operation            #
#          specifically                              #
# Parameters: ctx (Click) - The context object as    #
#                           provided by the Click    #
#                           framework                #
#             pattern (Optional by Click) - The      #
#                                           pattern( #
#                                           s) to    #
#                                           use to   #
#                                           identify #
#                                           the      #
#                                           files to #
#                                           attempt  #
#                                           to       #
#                                           rename   #
#             scn (Optional by Click) - The index of #
#                                       the SCN to   #
#                                       use          #
#             folder (Optional by Click) - The       #
#                                          folder to #
#                                          search    #
#                                          for the   #
#                                          desired   #
#                                          files in  #
# Return: N/A                                        #
#----------------------------------------------------#
@click.command()
@click.option('--pattern', '-p', default=[u'.*'], help='The file pattern to use for looking up relavent filenames', multiple=True)
@click.option('--scn', '-s', default=-1, help='The SCN index to use for the names')
@click.option('--folder', '-f', default='.', help='The folder to find the files for renamening in')
@click.pass_context
def cli(ctx, pattern, scn, folder):
       	# DEBUGGING: See what is passed along
	if ctx.obj['configs'].DEBUG_MODE == 'status':
		print 'Context Object: ' + str(ctx.obj)
	
	# Create a variable to hold the callback arguments
	callback_args = {
		'records':ctx.obj['records'],
		'configs':ctx.obj['configs']
	}
	
	# If the pattern(s) are specified in context object use thos if not use
	# the command line arguments via Click
	if 'patterns' in ctx.obj:
		callback_args['patterns'] = ctx.obj['patterns']
	else:
		# Add the pattern parameter in the extra callback parameters
        	callback_args['patterns'] = pattern
	
	# If the SCN index value is specified by the command line via Click add
	# it to the callback arguments
	if scn != -1:
		callback_args['SCN_index'] = scn
	
	# If the folder value is specified by the command line via Click add it
	# to the callback arguments
	if folder != '.':
		callback_args['folder'] = folder
	
        # Invoke the callback with appropriate arguments
        callback_return = rename_files(**callback_args)
	
	# Setup a progress bar so that the user knows how many more files there
	# are to consider renaming
	with click.progressbar(callback_return, show_eta=False, width=0) as bar:
		# The actual loop control
		for key in bar:
			# Check if the current value is a list or not as we'll 
			# need to treat these differently. The list arises when
			# there are multiple SCNs for a file but no specific
			# index was given
			if isinstance(callback_return[key], list):
				# Preface the user with what they will see
				prompt_text = 'Do you want to change ' + str(key) + ' to any of the following:\n'
				
				# Generate the indexed list for printing
				for index in range(len(callback_return[key])):
					prompt_text += str(index) + '. ' + callback_return[key][index] + '\n'
				
				# Ask the actual questions (stating unintuitive
				# controls)
				prompt_text += 'Enter the number you wish to use or -1 for none'
				# Set the input variable to a value that will 
				# fail our loop constrainto
				input = -2
				
				# Have a loop to make sure the user provides 
				# valid input otherwise is reasked
				while input < -1 or input > len(callback_return[key]) - 1:
					input = click.prompt(prompt_text, type=int)
					# Check if invalid input was given and 
					# if so notify the user
					if input < -1 or input > len(callback_return[key]) - 1:
						click.echo(str(input) + ' is an invalid index. Please try again')
				
				# If the input is -1 that means they just want 
				# to skip this entry
				if input != -1:
					# Confirm with the user this is what 
					# they want to do
					input = click.confirm('Change ' + str(key) + ' into ' + str(callback_return[key][input]) + '?')
					
					if input:
						# Rename the actual file
						os.rename(key, callback_return[key][index])
						# Let the user know the result
						click.echo('Done! I\'ve renamed the file :)')
					else:
						# Let the user know whats
						# happening
						click.echo('Okay, I won\'t :(')
			else:
				# Confirm with the user this is what they want 
				# to do
				input = click.confirm('Change ' + str(key) + ' into ' + str(callback_return[key]) + '?')
				
				if input:
					# Rename the actual file
					os.rename(key, callback_return[key])
					
					# Let the user know the result
					click.echo('Done! I\'ve renamed the file :)')
				else:
					# Let the user know whats happening
					click.echo('Okay, I won\'t :(')
