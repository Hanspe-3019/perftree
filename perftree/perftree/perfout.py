' - '

def print_it(root):
    '-'
    indent = ''
    max_elaps = max(child.elaps for child in root.children.values())
    time_to_str = make_seconds_str(max_elaps)

    def walk(node):
        nonlocal indent
        elaps_inside = node.elaps -  sum(
            child.elaps for child in node.children.values()
        )
        cpu_inside = node.cpu - sum(
            child.cpu for child in node.children.values()
        )
        busy = cpu_inside / elaps_inside
        print(
            f'{indent + node.name:30s}:'
            f'{int_to_str(node.count)} '
            f'{int_to_str(node.exceptions)} '
            f'{time_to_str(elaps_inside)} '
            f'{time_to_str(cpu_inside)} '
            f' {busy:4.0%} '
        )

        indent += ' '*4
        for child in node.children.values():
            walk(child)
        indent = indent[4:]

    for child in root.children.values():
        walk(child)

def make_seconds_str(max_secs):
    '- '
    if max_secs < 10**-2:
        div_by = 10**-6
        unit = 'µs'
    elif max_secs < 10:
        div_by = 10**-3
        unit = 'ms'
    elif max_secs < 3600:
        div_by = 1
        unit = 's'
    else:
        div_by = 60
        unit = 'm'
    def sec_to_str(secs):
        return f'{secs/div_by:7.1f} {unit}'

    return sec_to_str

def int_to_str(i):
    ' format int to str'
    if i < 10**6:
        return f'{i:8d}'
    if i < 10**9:
        return f'{i/10**6:5.1f}M'
    return f'{i/10**9:5.1f}G'
