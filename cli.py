import click
import os
import data_structs as structs
from Metadata_Parsers import Marc_XML_Parser
from funcs import func_get, func_set
from rename_files import rename_files

@click.command()
#@click.option('--dictionary', '-d', prompt='Dictionary', help='The filename that you want to be processed')
@click.option('--pattern', '-p', default=[u'.*'], help='The file pattern to use for looking up relavent filenames', multiple=True)
def main(pattern):
	parser_type = {'Marc XML':Marc_XML_Parser}
	options = []
	callbacks = {}
	for k,v in parser_type.iteritems():
		options.append(k)
		callbacks[k] = v
	
	type = click.prompt('What type of metadata to parse', type=click.Choice(options))
	dict_file_name = click.prompt('Where (filename) should the file be stored?')
	parser = callbacks[type]()
	parser.parse_to_file(dict_file_name)
	
        #click.echo('Opening %s' % file)
        #with open(dictionary) as f:
        #        lines = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the
        # end of each line
        #lines = [x.strip() for x in lines]
        #for line in lines:
        #        tokens = line.split("\t")
        #        structs.setTitle_fromSCN(tokens[0], tokens[1])
        #        structs.setSCN_fromTitle(tokens[1], tokens[0])
	#
	options = ['get', 'set', 'rename']
	with open(dict_file_name + '.json') as f:
		result = structs.json.load(f)
		records = structs.records_from_json(result)
	callback_args = {'rename':{'records':records, 'patterns':pattern}}
        callbacks = {'rename':'rename_files'}
        #for option in options:
        #        callbacks[option] = 'func_' + option
	#
        input = click.prompt('What would you like to do?', type=click.Choice(options))
	if input in callback_args:
		callback_returns = globals()[callbacks[input]](**callback_args[input])
		#if type(callback_returns) is dict:
		for k,v in callback_returns.iteritems():
			input = click.prompt('Change ' + str(k) + ' into ' + str(v) + '?', type=click.Choice(['yes','no']))
			if input == 'yes':
				os.rename(k, v)
			else:
				click.echo('Okay, I won\'t :(')
	else:
		globals()[callbacks[input]]()

if __name__ == '__main__':
        main()
