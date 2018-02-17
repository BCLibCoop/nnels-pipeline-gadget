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


