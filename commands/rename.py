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
@click.option('--pattern', '-p', default=[u'.*'], help='The file pattern to use for looking up relevent filenames', multiple=True)
@click.option('--scn-index', '-s', default=-1, help='The position of the SCN instance')
@click.option('--folder', '-f', default='.', help='The folder to find the files for renaming in')
@click.option('--sweep', '-s', is_flag=True, default=True, help="Sweep through all filenames after first prompt")
@click.pass_context
def cli(ctx, pattern, scn_index, folder, sweep):
       	# DEBUGGING: See what is passed along
	if ctx.obj['cfg'].DEBUG_MODE == 'status':
		print 'Context Object: ' + str(ctx.obj)

	# Create a variable to hold the callback arguments
	callback_args = {
		'records':ctx.obj['records'],
		'cfg':ctx.obj['cfg']
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
	if scn_index != -1:
		callback_args['scn_index'] = scn

	# If the folder value is specified by the command line via Click add it
	# to the callback arguments
	if folder != '.':
		callback_args['folder'] = folder

        # Invoke the callback with appropriate arguments
        callback_return = rename_files(**callback_args)

	# Setup a progress bar so that the user knows how many more files there
	# are to consider renaming
	with click.progressbar(callback_return, show_eta=False, width=0) as bar:

		if callback_args['sweep'] is not True:
			for key in bar:
				if click.confirm('Rename ' + str(key) + ' into ' + str(callback_return[key][scn_index]) + '?', abort=True):
					#####KILL
					print index
					print scn_index
					exit()

					# Rename the actual file
					click.echo('Renaming...')
					os.rename(key, callback_return[key][scn_index])
				else:
					click.echo('Skipping...')
		# Sweep is active
		else:
			click.echo('Set to rename: ')
			for k,v in callback_return.iteritems():
				click.echo( str(key) + ' into ' + str(callback_return[key][scn_index])

			if click.confirm("Proceed?", abort=True):
				for k,v in callback_return.iteritems():
					os.rename(key, callback_return[key][scn_index])

				click.echo("Renamed " + count(callback_return) + ' items')

			# Check if the current value is a list or not as we'll
			# need to treat these differently. The list arises when
			# there are multiple SCNs for a file but no specific
			# index was given
			if isinstance(callback_return[key], list):
				prompt_text = "There was no --scn-index value provided and there are multiple candidate SCNs to use. Please choice one"
				input = click.prompt(prompt_text, type=int)


