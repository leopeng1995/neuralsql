from pygments.lexer import inherit
from pygments.lexers.sql import MySqlLexer
from pygments.token import Keyword


class CliLexer(MySqlLexer):
    """Extends MySQL lexer to add keywords."""

    tokens = {
        'root': [(r'\brepair\b', Keyword),
                 (r'\boffset\b', Keyword),
                 (r'\btrainer\b', Keyword),
                 inherit],
    }
