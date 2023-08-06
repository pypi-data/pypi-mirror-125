import inquirer
from inquirer.themes import GreenPassion
from cli.trie_nathaniel import request
import click


@click.group()
def cli():
    pass


@cli.command()
def ui():
    question = [
        inquirer.List('choice',
                      message='What operation would you like to perform',
                      choices=['Add keyword', 'Delete keyword', 'Search for keyword', 'Autocomplete by prefix',
                               'Display trie', 'Display trie fast'],
                      carousel=True)
    ]

    choice = inquirer.prompt(question, theme=GreenPassion())['choice']

    if choice != 'Display trie' and choice != 'Display trie fast':
        question2 = [
            inquirer.Text('val',
                          message='Enter a word')
        ]
        val = inquirer.prompt(question2, theme=GreenPassion())['val']
        request(choice, val)
    else:
        request(choice)

