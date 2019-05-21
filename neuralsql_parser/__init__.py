from threading import Lock
from neuralsql_parser.parser import NeuralSQLParser


parserLocker = Lock()


def preprocess(result):
    parsed_result = dict()

    parsed_result['trainable'] = False
    if 'trainer' in result:
        parsed_result['trainable'] = True
        parsed_result['trainer'] = result['trainer'][0][1]

    table = result['tables'][0]
    parsed_result['database'] = table.split('.')[0]
    parsed_result['table'] = table.split('.')[1]

    parsed_result['columns'] = result['columns'][0]
    if 'where' in result:
        if type(result['where'][0]) != str:
            parsed_result['where'] = result['where'][0][1]

    if 'limit' in result:
        parsed_result['limit'] = result['limit'][0][1]

    return parsed_result


def parse(sql):
    with parserLocker:
        sql = sql.rstrip().rstrip(";")
        result = NeuralSQLParser.parseString(sql, parseAll=True).asDict()
        return preprocess(result)


__all__ = [
    'parse'
]
