VISUAL_INDENT = {
    'add': '+ ',
    'del': '- ',
    'eql': '  ',
    'upd': {
        'old': '- ',
        'new': '+ ',
    },
    'tab': ' ',
}
SPACE_INDENT = 2


def add_space_indent(current_indent):
    """
    Add space for indent print.

    Args:
        current_indent: current amount of indent.

    Returns:
        string for tab.
    """
    current_indent += SPACE_INDENT
    return VISUAL_INDENT['tab'] * current_indent


def del_space_indent(current_indent):
    """
    Delete space for indent print.

    Args:
        current_indent: current amount of indent.

    Returns:
        string for tab.
    """
    current_indent -= SPACE_INDENT
    return VISUAL_INDENT['tab'] * current_indent


def stringify_primitive(ast_value, indent):
    """
    Check and convert boolean value for print view or start recursion for dict.

    Args:
        ast_value: value from ast,
        indent: current amount of indent.

    Returns:
        primitive output string or recursion for nested dict.
    """
    if ast_value is True:
        return 'true'
    if ast_value is False:
        return 'false'
    if ast_value is None:
        return 'null'
    if isinstance(ast_value, dict):
        return pretty_print_dict_value(ast_value, indent=indent + SPACE_INDENT)
    return ast_value


def pretty_print_dict_value(ast_dict_value, indent):
    """
    Add print view for nested dict in AST.

    Args:
        ast_dict_value: dict object,
        indent: current space indent for print view.

    Returns:
        string view for output.
    """
    pp_dict_value = []
    space_indent = add_space_indent(indent)
    current_indent = len(space_indent)
    for ast_key, ast_value in ast_dict_value.items():
        if not pp_dict_value:
            pp_dict_value.append('{')
        pp_dict_value.append(('\n{0}{1}{2}: {3}').format(
            space_indent,
            VISUAL_INDENT['eql'],
            ast_key,
            stringify_primitive(ast_value, indent=indent + SPACE_INDENT),
        ))
    pp_dict_value.append(('\n{0}{1}').format(
        del_space_indent(current_indent),
        '}',
    ))
    return ''.join(pp_dict_value)


def pretty_print_ast(ast, indent=0):
    """
    Convert AST to pretty print view.

    Args:
        ast: abstract syntax tree,
        indent: amount of indent for output view.

    Returns:
        string representation.
    """
    pp_ast = []
    space_indent = add_space_indent(indent)
    current_indent = len(space_indent)
    for cell in ast:
        if not pp_ast:
            pp_ast.append('{')
        status = cell['status']
        if cell['children']:
            pp_ast.append(('\n{0}{1}{2}: {3}').format(
                space_indent,
                VISUAL_INDENT['eql'],
                cell['key'],
                pretty_print_ast(
                    cell['children'],
                    indent=current_indent + SPACE_INDENT,
                ),
            ))
        elif status == 'upd' and cell['children'] is None:
            old_value = cell['value']['old']
            new_value = cell['value']['new']
            pp_ast.append(('\n{0}{1}{2}: {3}').format(
                space_indent,
                VISUAL_INDENT['del'],
                cell['key'],
                stringify_primitive(old_value, current_indent),
            ))
            pp_ast.append(('\n{0}{1}{2}: {3}').format(
                space_indent,
                VISUAL_INDENT['add'],
                cell['key'],
                stringify_primitive(new_value, current_indent),
            ))
        else:
            pp_ast.append(('\n{0}{1}{2}: {3}').format(
                space_indent,
                VISUAL_INDENT[status],
                cell['key'],
                stringify_primitive(cell['value'], current_indent),
            ))
    pp_ast.append(('\n{0}{1}').format(
        del_space_indent(current_indent),
        '}',
    ))
    return ''.join(pp_ast)
