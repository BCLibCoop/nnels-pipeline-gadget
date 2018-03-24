import click

from config import Config
cfg = Config()

def func_get_title():
        input = click.prompt('What is the SCN of the title your looking for?')
        try:
                title = bySCN[input]
        except:
                title = 'Unavailable (No Such Entry)'
        click.echo('The title of the book is: ' + title)

def func_get_SCN():
        input = click.prompt('What is the title of the book your looking foer?')
        try:
                SCN = byTitle[input]
        except:
                SCN = 'Unavailable (No Such Entry)'
        click.echo('The SCN of the book is: ' + SCN)

def func_get():
        options = ['title', 'SCN']
        callbacks = {}
        for option in options:
                callbacks[option] = 'func_get_' + option

        input = click.prompt('What would you like to get?', type=click.Choice(options))
        globals()[callbacks[input]]()

def func_set():
        options = ['title', 'SCN']
        callbacks = {}
        for option in options:
                callbacks[option] = 'proc_set_' + option

        input = click.prompt('What would you like to get?', type=click.Choice(options))
        globals()[callbacks[input]]()

#----------------------------------------------------#
# Purpose: Combine patterns to form single regex     #
# Parameters: patterns - The patterns to combine     #
#             prefix (optional) - Any text or        #
#                                 pattern to         #
#                                 "prefix" to the    #
#                                 entire combined    #
#                                 pattern            #
#             suffix (optional) - Any text or        #
#                                 pattern to         #
#                                 "suffix"/append to #
#                                 the entire         #
#                                 combined pattern   #
#             prefix_each (optional) - Any text or   #
#                                      pattern to    #
#                                      "prefix" to   #
#                                      each of the   #
#                                      patterns      #
#                                      before        #
#                                      combination   #
#             suffix_each (optional) - Any text or   #
#                                      pattern to    #
#                                      "suffix"/     #
#                                      append to     #
#                                      each of the   #
#                                      patterns      #
#                                      before        #
#                                      combination   #
# Return: string - The resultant combined regex      #
#                  expression                        #
#----------------------------------------------------#
def combine_regex(patterns, prefix=None, suffix=None, prefix_each=None, suffix_each=None):
	if cfg.DEBUG_MODE:
		print '===================================================='
        	print 'Call Summary for combine_regex (funcs.py)'
        	print '----------------------------------------------------'
        	print 'Patterns: ' + str(patterns)
        	print 'Prefix (Whole): ' + str(prefix)
		print 'Suffix (Whole): ' + str(suffix)
		print 'Prefix (Each): ' + str(prefix_each)
		print 'Suffix (Each): ' + str(suffix_each)
        	print '===================|================================'
	
	# Define the variable to store the final expression in
	exp = ''
	
	# Check if a prefix to the expression was specified if so prefix it
	if prefix is not None:
		exp += prefix
	
	# Either append or start with a open brace
	if cfg.HOST_OS == 'Mac':
		exp += '('
	elif cfg.HOST_OS == 'Linux':
		exp += "'"
	
	# Loop over the 'patterns' supplied on the command line
	for index in range(0, len(patterns)):
		if prefix_each is not None:
			if type(prefix_each) != list:
				if not patterns[index].startswith(prefix_each):
					exp += prefix_each
			else:
				if prefix_each[index] is not None:
					if not patterns[index].startswith(prefix_each[index]):
						exp += prefix_each[index]
		
		exp += patterns[index]
		
		if suffix_each is not None:
			if type(suffix_each) != list:
				if not patterns[index].endswith(suffix_each):
					exp += suffix_each
			else:
				if suffix_each[index] is not None:
					if not patterns[index].endswith(suffix_each[index]):
						exp += suffix_each[index]
		
		exp += '|'
	
	# Remove the last character because it will be an extranous | character
	exp = exp[:len(exp) - 1]
	
  # Add a close brace/single-quote to end the expression
	if cfg.HOST_OS == 'Mac':
		exp += ")"
	elif cfg.HOST_OS == 'Linux':
		exp += "'"

	
	if suffix is not None:
		exp += suffix
	
	# Return the result
	return exp
