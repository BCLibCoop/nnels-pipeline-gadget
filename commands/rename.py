import click
from rename_files import rename_files

@click.command()
@click.option('--pattern', '-p', default=[u'.*'], help='The file pattern to use for looking up relavent filenames', multiple=True)
@click.pass_context
def cli(ctx, pattern):
       	# DEBUGGING: See what is passed along
	print 'Context Object: ' + str(ctx.obj)
	
	# Create a variable to hold the callback arguments
	callback_args = {
		'records':ctx.obj['records'],
	}
	
	if 'patterns' in ctx.obj:
		callback_args['patterns'] = ctx.obj['patterns']
	else:
		# Add the pattern parameter in the extra callback parameters
        	callback_args['patterns'] = pattern
	
        # Invoke the callback
        callback_return = rename_files(**callback_args)
	
	# Iterate over the values returned
	for k,v in callback_return.iteritems(): 
		# Prompt the user to see if they want to go ahead with the 
		# name change
		input = click.confirm('Change ' + str(k) + ' into ' + str(v) + '?')
		
		if input:
			# Rename the file
			os.rename(k, v)
			
			# Let the user know what has happend
			click.echo('Done! I\'ve renamed the file :)')
		else:
			# Let the user know we've acknowledge the input
			click.echo('Okay, I won\'t :(')
