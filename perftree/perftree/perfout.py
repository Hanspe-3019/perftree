' - '
def print_it(root):
    'Print Tree, ist fummelig'
    indent = ''
    max_elaps = max(child.elaps for child in root.children.values())
    time_to_str = make_seconds_str(max_elaps)
    header_line = ' '*35 + (
            'count '
            '     elaps '
            '      /call   '
            '   cpu   '
            'busy'
    )
    print(header_line)

    sum_elaps_inside = 0

    def walk(node):
        nonlocal indent
        nonlocal sum_elaps_inside
        elaps_inside = node.elaps -  sum(
            child.elaps for child in node.children.values()
        )
        sum_elaps_inside += elaps_inside
        cpu_inside = node.cpu - sum(
            child.cpu for child in node.children.values()
        )
        busy = min(
            cpu_inside / elaps_inside if elaps_inside > 0 else 1.,
            1.
        )
        print(
            f'{indent + node.name:30s}:'
            f'{int_to_str(node.count)} '
            f'{"*" if node.exceptions > 0 else ' '} '
            f'{time_to_str(elaps_inside)} '
            f'{secs_to_str(elaps_inside/node.count) if node.count > 1 else ' '*10}'
            f'{time_to_str(cpu_inside)} '
            f' {busy:4.0%} '
        )

        indent += ' '*4
        for child in node.children.values():
            walk(child)
        indent = indent[4:]

    for child in root.children.values():
        walk(child)
    print(f'{"*"*30}: {" "*10}{secs_to_str(sum_elaps_inside)}')

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

def secs_to_str(secs):
    ' - '
    return make_seconds_str(secs)(secs)
def int_to_str(i):
    ' format int to str'
    if i < 10**6:
        return f'{i:8d}'
    if i < 10**9:
        return f'{i/10**6:7.2f}M'
    return f'{i/10**9:7.2f}G'
