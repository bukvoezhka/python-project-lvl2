import json
from collections import namedtuple

import yaml

NEW_LINE = '\n'

FILE_HANDLER = {
    'JSON': {
        'extns': ('.json'),
        'converter': json.load,
    },
    'YAML': {
        'extns': ('.yaml', '.yml'),
        'converter': yaml.safe_load,
    },
}

AST_STATUSES = namedtuple(
    'status', ['added', 'deleted', 'equal', 'children', 'updated'],
)
STATUS = AST_STATUSES('added', 'deleted', 'equal', 'children', 'updated')

AST_STRUCTURE = {
    STATUS.added: lambda key, value:
        {
            'key': key,
            'status': 'added',
            'value': value[1],
        },
    STATUS.deleted: lambda key, value:
        {
            'key': key,
            'status': 'deleted',
            'value': value[0],
        },
    STATUS.equal: lambda key, value:
        {
            'key': key,
            'status': 'equal',
            'value': value[0],
        },
    STATUS.children: lambda key, value:
        {
            'key': key,
            'status': 'children',
            'value': value,
        },
    STATUS.updated: lambda key, value:
        {
            'key': key,
            'status': 'updated',
            'old_value': value[0],
            'new_value': value[1],
        },
}

PRIMITIVE_VALUES = {
    True: 'true',
    False: 'false',
    None: 'null',
}
COMPLEX_VALUES = (list, dict, tuple, set)

STYLISH_VIEW = {
    STATUS.added: lambda key, value: '+ {0}: {1}'.format(
        key, value,
    ),
    STATUS.deleted: lambda key, value: '- {0}: {1}'.format(
        key, value,
    ),
    STATUS.equal: lambda key, value: '  {0}: {1}'.format(
        key, value,
    ),
    STATUS.children: lambda key, value: '  {0}: {1}'.format(
        key, value,
    ),
    'indent': ' ',
}
SPACE_INDENT = 2
BRACKETS = {
    'open': '{',
    'close': '}',
}

PLAIN_VIEW = {
    STATUS.added: lambda key, value:
        "Property '{0}' was added with value: {1}".format(key, value),
    STATUS.deleted: lambda key, _:
        "Property '{0}' was removed".format(key),
    STATUS.updated: lambda key, value:
        "Property '{0}' was updated. From {1} to {2}".format(
            key, value[0], value[1],
        ),
    'delemiter': '.',
}
