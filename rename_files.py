import click
import subprocess

bySCN = {}
byTitle = {}

def proc_get_title():
	input = click.prompt('What is the SCN of the title your looking for?')
	try:
		title = bySCN[input]
	except:
		title = 'Unavailable (No Such Entry)'
	click.echo('The title of the book is: ' + title)

def proc_get_SCN():
	input = click.prompt('What is the title of the book your looking foer?')
	try:
		SCN = byTitle[input]
	except:
		SCN = 'Unavailable (No Such Entry)'
	click.echo('The SCN of the book is: ' + SCN)

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

def rename(pattern):
	args = ['find', '.', '-name', pattern]
	proc = subprocess.Popen(args, stdout=subprocess.PIPE)
	stdout, stderr = proc.communicate()
	lines = stdout.decode('ascii').splitlines()
	for line in lines:
		if '.' in line:
			parts = line.split('.')
			if len(parts[0]) < 1:
				parts.remove(parts[0])
			if len(parts) == 2:
				if len(parts[0]) > 0:
					name = parts[0]
					if '_' in name:
						tokens = name.split('_')
						print tokens
					else:
						print 'To be implemented...'
					format = parts[1]
			else:
				print 'There is something odd about ' + line + 'because broken down it changes into' + str(parts)

@click.command()
@click.option('--dictionary', prompt='Dictionary', help='The filename that you want to be processed')
@click.option('--pattern', prompt='File pattern', help='The file pattern to use for looking up relavent filenames')
def main(dictionary, pattern):
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
	
	rename(pattern)
	
	options = ['get', 'set']
	callbacks = {}
	for option in options:
		callbacks[option] = 'proc_' + option
	input = click.prompt('What would you like to do?', type=click.Choice(options))
	globals()[callbacks[input]]()

if __name__ == '__main__':
	main()
