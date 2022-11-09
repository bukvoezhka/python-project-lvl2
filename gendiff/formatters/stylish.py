from gendiff.constants import (
    BRACKETS,
    NEW_LINE,
    PRIMITIVE_VALUES,
    SPACE_INDENT,
    STATUS,
    STYLISH_VIEW,
)


def add_space_indent(current_indent):
    """
    Add space for indent print.

    Args:
        current_indent: current amount of indent.

    Returns:
        string for tab.
    """
    current_indent += SPACE_INDENT
    return STYLISH_VIEW['indent'] * current_indent


def del_space_indent(current_indent):
    """
    Delete space for indent print.

    Args:
        current_indent: current amount of indent.

    Returns:
        string for tab.
    """
    current_indent -= SPACE_INDENT
    return STYLISH_VIEW['indent'] * current_indent


def stringify_primitive(current_value):
    """
    Check and convert boolean value for print view.

    Args:
        current_value: value from ast.

    Returns:
        primitive output string.
    """
    if isinstance(current_value, dict):
        return convert_dict_value(current_value)
    if isinstance(current_value, bool):
        return PRIMITIVE_VALUES[current_value]
    if current_value is None:
        return PRIMITIVE_VALUES[current_value]
    return current_value


def is_false_children(node_value):
    """
    Check attribute of value on used a convert_dict_value function.

    Args:
        node_value: value of current cell from AST.

    Returns:
        boolean result.

    Raise:
        AttributeError: if value has not been converted.
    """
    if isinstance(node_value, list):
        try:
            return node_value[0]['false_children']
        except AttributeError:
            return False
    return False


def convert_dict_value(node_value):
    """
    Check and convert value if AST cell value is python dict.

    Args:
        node_value: value of current cell from AST.

    Returns:
        list of new value of AST representation.
    """
    if not isinstance(node_value, dict):
        return node_value
    false_children = []
    for child_key, child_value in node_value.items():
        if isinstance(child_value, dict):
            false_children.append({
                'key': child_key,
                'status': 'children',
                'value': convert_dict_value(child_value),
                'false_children': True,
            })
        else:
            false_children.append({
                'key': child_key,
                'status': 'equal',
                'value': child_value,
                'false_children': True,
            })
    return false_children


def check_cell_status(cell):
    """
    Check status of current cell from AST.

    Args:
        cell: node from AST.

    Returns:
        list of converted value based on its status.
    """
    status = cell['status']
    if status == STATUS.updated:
        return [{
            'key': cell['key'],
            'status': 'deleted',
            'value': stringify_primitive(cell['old_value']),
        }, {
            'key': cell['key'],
            'status': 'added',
            'value': stringify_primitive(cell['new_value']),
        }]
    if status != STATUS.children:
        return [{
            'key': cell['key'],
            'status': status,
            'value': stringify_primitive(cell['value']),
        }]
    return [cell]


def add_ast_tree_line(cell, indent):
    """
    Make a line of current cell for tree view representation.

    Args:
        cell: current node of AST,
        indent: space indent to display.

    Returns:
        formatted line list for common tree view.
    """
    tree_line = []
    for node in check_cell_status(cell):
        node_status = node['status']
        node_value = node['value']
        if node_status == STATUS.children or is_false_children(node_value):
            tree_line.append('{0}{1}{2}'.format(
                NEW_LINE,
                indent,
                STYLISH_VIEW[node_status](
                    node['key'], make_ast_tree_view(
                        node_value, len(indent) + SPACE_INDENT,
                    ),
                ),
            ))
        else:
            tree_line.append('{0}{1}{2}'.format(
                NEW_LINE,
                indent,
                STYLISH_VIEW[node_status](
                    node['key'], stringify_primitive(node_value),
                ),
            ))
    return tree_line


def make_ast_tree_view(ast, indent=0):
    """
    Convert AST to pretty print tree view.

    Args:
        ast: abstract syntax tree,
        indent: amount of indent for output view.

    Returns:
        string representation.
    """
    tree_view = [BRACKETS['open']]
    space_indent = add_space_indent(indent)
    for cell in ast:
        tree_view.extend(add_ast_tree_line(cell, space_indent))
    tree_view.append(('{0}{1}{2}').format(
        NEW_LINE,
        del_space_indent(len(space_indent)),
        BRACKETS['close'],
    ))
    return ''.join(tree_view)
