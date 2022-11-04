NESTED_AST = [
    {
        'key': 'common',
        'status': 'children',
        'value': [
            {
                'key': 'follow',
                'status': 'added',
                'value': False,
            },
            {
                'key': 'setting1',
                'status': 'equal',
                'value': 'Value 1',
            },
            {
                'key': 'setting2',
                'status': 'deleted',
                'value': 200,
            },
            {
                'key': 'setting3',
                'status': 'updated',
                'old_value': True,
                'new_value': None,
            },
            {
                'key': 'setting4',
                'status': 'added',
                'value': 'blah blah',
            },
            {
                'key': 'setting5',
                'status': 'added',
                'value': {'key5': 'value5'},
            },
            {
                'key': 'setting6',
                'status': 'children',
                'value': [
                    {
                        'key': 'doge',
                        'status': 'children',
                        'value': [
                            {
                                'key': 'wow',
                                'status': 'updated',
                                'old_value': '',
                                'new_value': 'so much',
                            },
                        ],
                    },
                    {
                        'key': 'key',
                        'status': 'equal',
                        'value': 'value',
                    },
                    {
                        'key': 'ops',
                        'status': 'added',
                        'value': 'vops',
                    },
                ],
            },
        ],
    },
    {
        'key': 'group1',
        'status': 'children',
        'value': [
            {
                'key': 'baz',
                'status': 'updated',
                'old_value': 'bas',
                'new_value': 'bars',
            },
            {
                'key': 'foo',
                'status': 'equal',
                'value': 'bar',
            },
            {
                'key': 'nest',
                'status': 'updated',
                'old_value': {'key': 'value'},
                'new_value': 'str',
            },
        ],
    },
    {
        'key': 'group2',
        'status': 'deleted',
        'value': {
            'abc': 12345,
            'deep': {
                'id': 45,
            },
        },
    },
    {
        'key': 'group3',
        'status': 'added',
        'value': {
            'deep': {
                'id': {
                    'number': 45,
                },
            },
            'fee': 100500,
        },
    },
]
