import re

from prompt_toolkit.completion import Completer, Completion

cleanup_regex = {
    # This matches only alphanumerics and underscores.
    'alphanum_underscore': re.compile(r'(\w+)$'),
    # This matches everything except spaces, parens, colon, and comma
    'many_punctuations': re.compile(r'([^():,\s]+)$'),
    # This matches everything except spaces, parens, colon, comma, and period
    'most_punctuations': re.compile(r'([^\.():,\s]+)$'),
    # This matches everything except a space.
    'all_punctuations': re.compile('([^\s]+)$'),
}


def last_word(text, include='alphanum_underscore'):
    """
    Find the last word in a sentence.

    >>> last_word('abc')
    'abc'
    >>> last_word(' abc')
    'abc'
    >>> last_word('')
    ''
    >>> last_word(' ')
    ''
    >>> last_word('abc ')
    ''
    >>> last_word('abc def')
    'def'
    >>> last_word('abc def ')
    ''
    >>> last_word('abc def;')
    ''
    >>> last_word('bac $def')
    'def'
    >>> last_word('bac $def', include='most_punctuations')
    '$def'
    >>> last_word('bac \def', include='most_punctuations')
    '\\\\def'
    >>> last_word('bac \def;', include='most_punctuations')
    '\\\\def;'
    >>> last_word('bac::def', include='most_punctuations')
    'def'
    """

    if not text:  # Empty string
        return ''

    if text[-1].isspace():
        return ''
    else:
        regex = cleanup_regex[include]
        matches = regex.search(text)
        if matches:
            return matches.group(0)
        else:
            return ''


class SQLCompleter(Completer):
    keywords = ['ACCESS', 'ADD', 'ALL', 'ALTER TABLE', 'AND', 'ANY', 'AS',
                'ASC', 'AUTO_INCREMENT', 'BEFORE', 'BEGIN', 'BETWEEN', 'BINARY', 'BY',
                'CASE', 'CHAR', 'CHECK', 'COLUMN', 'COMMENT', 'COMMIT', 'CONSTRAINT',
                'CHANGE MASTER TO', 'CHARACTER SET', 'COLLATE', 'CREATE', 'CURRENT', 'CURRENT_TIMESTAMP', 'DATABASE',
                'DATE',
                'DECIMAL', 'DEFAULT', 'DELETE FROM', 'DELIMITER', 'DESC',
                'DESCRIBE', 'DROP', 'ELSE', 'END', 'ENGINE', 'ESCAPE', 'EXISTS',
                'FILE', 'FLOAT', 'FOR', 'FOREIGN KEY', 'FORMAT', 'FROM', 'FULL', 'FUNCTION', 'GRANT',
                'GROUP BY', 'HAVING', 'HOST', 'IDENTIFIED', 'IN', 'INCREMENT', 'INDEX',
                'INSERT INTO', 'INTEGER', 'INTO', 'INTERVAL', 'IS', 'JOIN', 'KEY', 'LEFT',
                'LEVEL', 'LIKE', 'LIMIT', 'LOCK', 'LOGS', 'LONG', 'MASTER', 'MODE',
                'MODIFY', 'NOT', 'NULL', 'NUMBER', 'OFFSET', 'ON', 'OPTION', 'OR',
                'ORDER BY', 'OUTER', 'OWNER', 'PASSWORD', 'PORT', 'PRIMARY',
                'PRIVILEGES', 'PROCESSLIST', 'PURGE', 'REFERENCES', 'REGEXP', 'RENAME', 'REPAIR', 'RESET',
                'REVOKE', 'RIGHT', 'ROLLBACK', 'ROW', 'ROWS', 'ROW_FORMAT', 'SELECT', 'SESSION', 'SET',
                'SAVEPOINT', 'SHARE', 'SHOW', 'SLAVE', 'SMALLINT', 'START', 'STOP', 'TABLE', 'THEN',
                'TO', 'TRANSACTION', 'TRIGGER', 'TRUNCATE', 'UNION', 'UNIQUE', 'UNSIGNED', 'UPDATE',
                'USE', 'USER', 'USING', 'VALUES', 'VARCHAR', 'VIEW', 'WHEN', 'WHERE',
                'WITH', 'TINYINT', 'SMALLINT', 'MEDIUMINT', 'INT', 'BIGINT']

    neuralsql_keywords = ['TRAINER', 'WORD2VEC', 'WORDCOUNT']

    functions = ['AVG', 'CONCAT', 'COUNT', 'DISTINCT', 'FIRST', 'FORMAT', 'LAST',
                 'LCASE', 'LEN', 'MAX', 'MIN', 'MID', 'NOW', 'ROUND', 'SUM',
                 'TOP', 'UCASE', 'FROM_UNIXTIME', 'UNIX_TIMESTAMP']

    def __init__(self):
        self.all_completions = set(self.keywords + self.functions + self.neuralsql_keywords)

    @staticmethod
    def find_matches(text, collection, start_only=False, fuzzy=True, casing=None):
        """Find completion matches for the given text.

        Given the user's input text and a collection of available
        completions, find completions matching the last word of the
        text.

        If `start_only` is True, the text will match an available
        completion only at the beginning. Otherwise, a completion is
        considered a match if the text appears anywhere within it.

        yields prompt_toolkit Completion instances for any matches found
        in the collection of available completions.
        """
        last = last_word(text, include='most_punctuations')
        text = last.lower()

        completions = []

        if fuzzy:
            regex = '.*?'.join(map(re.escape, text))
            pat = re.compile('(%s)' % regex)
            for item in sorted(collection):
                r = pat.search(item.lower())
                if r:
                    completions.append((len(r.group()), r.start(), item))
        else:
            match_end_limit = len(text) if start_only else None
            for item in sorted(collection):
                match_point = item.lower().find(text, 0, match_end_limit)
                if match_point >= 0:
                    completions.append((len(text), match_point, item))

        if casing == 'auto':
            casing = 'lower' if last and last[-1].islower() else 'upper'

        def apply_case(kw):
            if casing == 'upper':
                return kw.upper()
            return kw.lower()

        return (Completion(z if casing is None else apply_case(z), -len(text))
                for x, y, z in sorted(completions))

    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        return self.find_matches(word_before_cursor, self.all_completions,
                                 start_only=True, fuzzy=False)
