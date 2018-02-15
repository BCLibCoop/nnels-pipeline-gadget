import click

bySCN = {}
byTitle = {}

def proc_get_title():
	input = click.prompt('What is the SCN of the title your looking for?')
	title = bySCN[input]
	click.echo('The title of the book is: ' + title)

def proc_get_SCN():
	click.echo('Getting SCN')

def proc_get():
	options = ['title', 'SCN']
	callbacks = {}
	for option in options:
		callbacks[option] = 'proc_get_' + option
	
	input = click.prompt('What would you like to get?', type=click.Choice(options))
	globals()[callbacks[input]]()

def proc_set_title():
	click.echo('Setting the title')

def proc_set_SCN():
	click.echo('Setting the SCN')

def proc_set():
	options = ['title', 'SCN']
        callbacks = {}
        for option in options:
                callbacks[option] = 'proc_set_' + option

        input = click.prompt('What would you like to get?', type=click.Choice(options))
        globals()[callbacks[input]]()

@click.command()
@click.option('--dictionary', prompt='Dictionary', help='The filename that you want to be processed')
def main(dictionary):
	click.echo('Opening %s' % file)
	with open(dictionary) as f:
		lines = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the 
	# end of each line
	lines = [x.strip() for x in lines]
	for line in lines:
		tokens = line.split("\t")
		bySCN[tokens[0]] = tokens[1]
		byTitle[tokens[1]] = tokens[0]
	
	options = ['get', 'set']
	callbacks = {}
	for option in options:
		callbacks[option] = 'proc_' + option
	input = click.prompt('What would you like to do?', type=click.Choice(options))
	globals()[callbacks[input]]()
if __name__ == '__main__':
	main()
