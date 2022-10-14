NESTED_AST = [
    {
        'key': 'common',
        'value': None,
        'status': 'upd',
        'children': [
            {
                'key': 'follow',
                'value': False,
                'status': 'add',
                'children': None,
            },
            {
                'key': 'setting1',
                'value': 'Value 1',
                'status': 'eql',
                'children': None,
            },
            {
                'key': 'setting2',
                'value': 200,
                'status': 'del',
                'children': None,
            },
            {
                'key': 'setting3',
                'value': {
                    'old': True,
                    'new': None,
                },
                'status': 'upd',
                'children': None,
            },
            {
                'key': 'setting4',
                'value': 'blah blah',
                'status': 'add',
                'children': None,
            },
            {
                'key': 'setting5',
                'value': {'key5': 'value5'},
                'status': 'add',
                'children': None,
            },
            {
                'key': 'setting6',
                'value': None,
                'status': 'upd',
                'children': [
                    {
                        'key': 'doge',
                        'value': None,
                        'status': 'upd',
                        'children': [
                            {
                                'key': 'wow',
                                'value': {
                                    'old': '',
                                    'new': 'so much',
                                },
                                'status': 'upd',
                                'children': None,
                            },
                        ],
                    },
                    {
                        'key': 'key',
                        'value': 'value',
                        'status': 'eql',
                        'children': None,
                    },
                    {
                        'key': 'ops',
                        'value': 'vops',
                        'status': 'add',
                        'children': None,
                    },
                ],
            },
        ],
    },
    {
        'key': 'group1',
        'value': None,
        'status': 'upd',
        'children': [
            {
                'key': 'baz',
                'value': {
                    'old': 'bas',
                    'new': 'bars',
                },
                'status': 'upd',
                'children': None,
            },
            {
                'key': 'foo',
                'value': 'bar',
                'status': 'eql',
                'children': None,
            },
            {
                'key': 'nest',
                'value': {
                    'old': {'key': 'value'},
                    'new': 'str',
                },
                'status': 'upd',
                'children': None,
            },
        ],
    },
    {
        'key': 'group2',
        'value': {
            'abc': 12345,
            'deep': {
                'id': 45,
            },
        },
        'status': 'del',
        'children': None,
    },
    {
        'key': 'group3',
        'value': {
            'deep': {
                'id': {
                    'number': 45,
                },
            },
            'fee': 100500,
        },
        'status': 'add',
        'children': None,
    },
]
