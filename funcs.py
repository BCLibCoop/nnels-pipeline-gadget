import click

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

def combine_regex(patterns, prefix=None, suffix=None, prefix_each=None, suffix_each=None):
	# Define the variable to store the final expression in
	exp = ''
	
	# Check if a prefix to the expression was specified if so prefix it
	if prefix is not None:
		exp += prefix
	
	# Either append or start with a open brace
	exp += '(';
	
	# Loop over the 'patterns' supplied on the command line
	for pattern in patterns:
		if prefix_each is not None:
			if not pattern.startswith(prefix_each):
				exp += prefix_each
		
		exp += pattern
		
		if suffix_each is not None:
			if not pattern.endswith(suffix_each):
				exp += suffix_each
		
		exp += '|'
	
	# Remove the last character because it will be an extranous | character
	exp = exp[:len(exp) - 1]
	
	# Add a close brace to end the expression
	exp += ')'
	
	if suffix is not None:
		exp += suffix
	
	# Return the result
	return exp
