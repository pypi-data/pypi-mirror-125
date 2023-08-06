import inquirer
from inquirer.themes import GreenPassion
from cli.trie_nathaniel import request
import click


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument('val', required=1)
def add(val: str) -> None:
    """Adds the given word to trie and displays the status of the operation

    Args:
        val (str): The word you wish to add to the trie
    """
    request('Add keyword', val)


@cli.command()
@click.argument('val', required=1)
def delete(val: str) -> None:
    """Deletes a word from the trie if it exists and displays the status of the operation

    Args:
        val (str): The word you wish to delete from the trie
    """
    request('Delete keyword', val)


@cli.command()
@click.argument('val', required=1)
def search(val: str) -> None:
    """Searches the trie for the given word and will display whether or not it was found

    Args:
        val (str): The word you want to check exists in the trie
    """
    request('Search for keyword', val)


@cli.command()
@click.argument('val', required=1)
def complete(val: str) -> None:
    """Displays all possible completions of words from the given prefix according to existing words in the trie

    Args:
        val (str): The prefix you wish to search the trie for auto-completions of
    """
    request('Autocomplete by prefix', val)


@cli.command()
def view() -> None:
    """Displays all the elements in the trie in a slower manner than could be done. Since this retrieves the elements
    of the trie using recursion it is slower but it tests the implementation of the recursive method
    """
    request('Display trie')


@cli.command()
def viewfast() -> None:
    """Displays all the elements in the trie in the fastest way possible. This is done through a separate array that
    holds all values in the trie
    """
    request('Display trie fast')


@cli.command()
def ui() -> None:
    """Initiates the CLI UI with beautiful controls and easy to navigate options
    """
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


if __name__ == '__main__':
    ui()

