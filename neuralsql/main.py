import os
import sys
import time
from threading import Lock

import click
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import DynamicCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.lexers import PygmentsLexer

from neuralsql import __version__
from neuralsql.cli.completer import SQLCompleter
from neuralsql.cli.lexer import CliLexer
from neuralsql.sql.executor import SQLExecutor


class NeuralSQLCli(object):
    def __init__(self):
        self.prompt_app = None
        self.sql_executor = None

        self.completer = SQLCompleter()
        self._completer_lock = Lock()

    def connect(self, host, port):
        self.sql_executor = SQLExecutor(host, port)

    def run_cli(self):
        sql_executor = self.sql_executor
        print('mongodb server version:', sql_executor.server_type())
        print('neuralsql', __version__)
        print('Goal: Make MongoDB More Intelligent.')

        history_file = os.path.expanduser(
            os.environ.get('NEURALSQL_CLI_HISTFILE', '~/.neuralsql-cli-history'))
        if os.path.exists(os.path.dirname(history_file)):
            history = FileHistory(history_file)
        else:
            history = None
            self.echo(
                'Error: Unable to open the history file "{}". '
                'Your query history will not be saved.'.format(history_file),
                err=True, fg='red')

        def one_iteration():
            try:
                text = self.prompt_app.prompt()
                if text == 'exit' or text == 'quit':
                    raise EOFError

                start = time.time()
                sql_executor.run(text)
                print('Time: ', round(time.time() - start, 3), 's')
            except KeyboardInterrupt:
                return

        self.prompt_app = PromptSession(
            lexer=PygmentsLexer(CliLexer),
            completer=DynamicCompleter(lambda: self.completer),
            message='neuralsql> ',
            history=history,
            auto_suggest=AutoSuggestFromHistory(),
            complete_while_typing=True,
        )

        try:
            while True:
                one_iteration()
        except EOFError:
            self.echo('Goodbye!')

    def echo(self, s, **kwargs):
        click.secho(s, **kwargs)

    def run_query(self, query):
        pass

    def load_sample(self, sample):
        self.sql_executor.load_sample(sample)


@click.command()
@click.option('-h', '--host', envvar='MONGODB_HOST', help='Host address of the database.')
@click.option('-P', '--port', envvar='MONGODB_TCP_PORT', type=int, help='Port number to use for connection. Honors '
                                                                        '$MONGODB_TCP_PORT.')
@click.option('-V', '--version', is_flag=True, help='Output NeuralSQL\'s version.')
@click.option('-D', '--database', help='Database to use.')
@click.option('-L', '--load-sample', 'sample',  help='Load Samples Data To MongoDB.')
def cli(host, port, version, database, sample):
    if version:
        print('Version:', __version__)
        sys.exit(0)

    neuralsql_cli = NeuralSQLCli()
    neuralsql_cli.connect(host, port)

    if sample:
        neuralsql_cli.load_sample(sample)
        sys.exit(0)

    neuralsql_cli.run_cli()


if __name__ == '__main__':
    cli()
