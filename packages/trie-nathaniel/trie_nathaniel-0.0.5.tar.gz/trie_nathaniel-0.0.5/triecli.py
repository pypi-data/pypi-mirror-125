import inquirer
from inquirer.themes import GreenPassion
from cli.trie_nathaniel import request
import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument(type=str, help='Adds the given word to the trie')
def add(val:str):
    request('Add keyword', val)


@cli.command()
@click.argument(type=str, help='Deletes the given word from the trie')
def delete(val:str):
    request('Delete keyword', val)


@cli.command()
@click.argument(type=str, help='Searches the trie to see if the given word exists')
def search(val:str):
    request('Search for keyword', val)


@cli.command()
@click.argument(type=str, help='Autocompletes the prefix from the known values in the trie')
def complete(val:str):
    request('Autocomplete by prefix', val)


@cli.command(help='Displays the trie using recursion (slower)')
def view():
    request('Display trie')


@cli.command(help='Displays the trie from the pre-stored array values (faster)')
def viewfast():
    request('Display trie fast')


@cli.command(help='Runs the CLI with a nice user interface')
def ui():
    question = [
        inquirer.List('choice',
                      message='What operation would you like to perform',
                      choices=['Add keyword', 'Delete keyword', 'Search for keyword', 'Autocomplete by prefix',
                               'Display trie', 'Display trie fast', 'Exit'],
                      carousel=True)
    ]
    question2 = [
        inquirer.Text('val',
                      message='Enter a word')
    ]
    while True:
        choice = inquirer.prompt(question, theme=GreenPassion())['choice']

        if choice == 'Exit':
            quit()

        if choice != 'Display trie' and choice != 'Display trie fast':
            val = inquirer.prompt(question2, theme=GreenPassion())['val']
            request(choice, val)
        else:
            request(choice)

