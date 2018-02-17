import click
import data_structs as structs
from funcs import func_get, func_set
from rename_files import func_rename

@click.command()
@click.option('--dictionary', '-d', prompt='Dictionary', help='The filename that you want to be processed')
@click.option('--pattern', '-p', default=[u'.*'], help='The file pattern to use for looking up relavent filenames', multiple=True)
def main(dictionary, pattern):
        click.echo('Opening %s' % file)
        with open(dictionary) as f:
                lines = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the
        # end of each line
        lines = [x.strip() for x in lines]
        for line in lines:
                tokens = line.split("\t")
                structs.setTitle_fromSCN(tokens[0], tokens[1])
                structs.setSCN_fromTitle(tokens[1], tokens[0])
	
	options = ['get', 'set', 'rename']
	callbackArgs = {'rename':'pattern'}
        callbacks = {}
        for option in options:
                callbacks[option] = 'func_' + option
	
        input = click.prompt('What would you like to do?', type=click.Choice(options))
	if input in callbackArgs:
		globals()[callbacks[input]](locals()[callbackArgs[input]])
	else:
		globals()[callbacks[input]]()

if __name__ == '__main__':
        main()
