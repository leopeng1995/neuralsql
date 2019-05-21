import sys

from pyparsing import CaselessKeyword
from pyparsing import Forward
from pyparsing import Group
from pyparsing import Literal
from pyparsing import Optional
from pyparsing import ParserElement
from pyparsing import Word
from pyparsing import ZeroOrMore
from pyparsing import alphanums
from pyparsing import alphas
from pyparsing import delimitedList
from pyparsing import infixNotation
from pyparsing import oneOf
from pyparsing import opAssoc
from pyparsing import pyparsing_common as ppc
from pyparsing import quotedString
from pyparsing import restOfLine
from pyparsing import MatchFirst


ParserElement.enablePackrat()

sys.setrecursionlimit(3000)

# define SQL tokens
selectStmt = Forward()

keywords = {
    "select",
    "from",
    "where",
    "and",
    "or",
    "in",
    "is",
    "not",
    "null",
    "trainer",
    "with",
    "into",
    'asc',
    'desc',
    'limit',
}

locs = locals()
reserved = []
for k in keywords:
    name = k.upper().replace(" ", "")
    locs[name] = value = CaselessKeyword(k).setName(k.lower())
    reserved.append(value)
RESERVED = MatchFirst(reserved)

# SELECT, FROM, WHERE, AND, OR, IN, IS, NOT, NULL, TRAINER, WITH = map(CaselessKeyword,
#                                                                      "select from where and or in is not null trainer with".split())
NOT_NULL = NOT + NULL

ident = Word(alphas, alphanums + "_$").setName("identifier")
columnName = delimitedList(ident, ".", combine=True).setName("column name")
# columnName.addParseAction(ppc.upcaseTokens)
columnNameList = Group(delimitedList(columnName))
tableName = delimitedList(ident, ".", combine=True).setName("table name")
# tableName.addParseAction(ppc.upcaseTokens)
tableNameList = Group(delimitedList(tableName))

binop = oneOf("= != < > >= <= eq ne lt le gt ge", caseless=True)
realNum = ppc.real()
intNum = ppc.signed_integer()

paramName = delimitedList(ident, ".", combine=True).setName("param name")
# paramValue = QuotedString("'") | delimitedList(ident, ".", combine=True)
# paramValue = delimitedList(ident, ".", combine=True).setName("param value")
paramValue = quotedString | columnName | realNum | intNum

columnRval = realNum | intNum | quotedString | columnName  # need to add support for alg expressions
whereCondition = Group(
    (columnName + binop + columnRval) |
    (columnName + IN + Group("(" + delimitedList(columnRval) + ")")) |
    (columnName + IN + Group("(" + selectStmt + ")")) |
    (columnName + IS + (NULL | NOT_NULL))
)

whereExpression = infixNotation(whereCondition,
                                [
                                    (NOT, 1, opAssoc.RIGHT),
                                    (AND, 2, opAssoc.LEFT),
                                    (OR, 2, opAssoc.LEFT),
                                ])

limitExpression = intNum

# loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None
withExpression = Group(
    Group(paramName + "=" + paramValue) + ZeroOrMore("," + Group(paramName + "=" + paramValue))
)

# define the grammar
selectStmt <<= (SELECT + ('*' | columnNameList)("columns") +
                FROM + tableNameList("tables") +
                Optional(Group(TRAINER + columnName + Optional(WITH + withExpression)))("trainer") +
                Optional(Group(INTO + tableName))("into") +
                Optional(Group(WHERE + whereExpression), "")("where")  +
                Optional(Group(LIMIT + limitExpression))('limit'))

NeuralSQLParser = selectStmt

# define Oracle and MySQL comment format, and ignore them
oracleSqlComment = Literal("--") + restOfLine
mySqlComment = Literal("#") + restOfLine
NeuralSQLParser.ignore(oracleSqlComment | mySqlComment)
