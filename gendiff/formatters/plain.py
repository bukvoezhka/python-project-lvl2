from gendiff.constants import (
    COMPLEX_VALUES,
    NEW_LINE,
    PLAIN_VIEW,
    PRIMITIVE_VALUES,
    STATUS,
)


def stringify_primitive(current_value):
    """
    Check and convert values for print view.

    Args:
        current_value: value from ast.

    Returns:
        primitive output string.
    """
    if isinstance(current_value, COMPLEX_VALUES):
        return '[complex value]'
    if isinstance(current_value, str):
        return "'{0}'".format(current_value)
    try:
        return PRIMITIVE_VALUES[current_value]
    except KeyError:
        return current_value


def check_cell_status(cell):
    """
    Check and convert value to output format.

    Args:
        cell: current cell of ast.

    Returns:
        converted value.
    """
    if cell['status'] == STATUS.equal:
        return False
    if cell['status'] == STATUS.updated:
        return stringify_primitive(cell['old_value']), stringify_primitive(
            cell['new_value'],
        )
    return stringify_primitive(cell['value'])


def make_ast_plain_view(ast, parrent_path=None):
    """
    Convert AST to pretty print plain view.

    Args:
        ast: abstract syntax tree,
        parrent_path: full path to key in nested structure.

    Returns:
        string representation.
    """
    plain_view = []
    if parrent_path is None:
        parrent_path = []
    for cell in filter(check_cell_status, ast):
        if cell['status'] == STATUS.children:
            parrent_path += [cell['key']]
            plain_view.append(make_ast_plain_view(cell['value'], parrent_path))
            parrent_path.pop()
        else:
            key_path = parrent_path + [cell['key']]
            plain_view.append('{0}'.format(
                PLAIN_VIEW[cell['status']](
                    PLAIN_VIEW['delemiter'].join(key_path),
                    check_cell_status(cell),
                ),
            ))
            key_path.clear()
    return NEW_LINE.join(plain_view)
