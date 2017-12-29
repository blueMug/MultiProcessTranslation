
def read_txt(filename, begin=0):
    res = list()
    with open(filename, 'rb') as f:
        for i, line in enumerate(f):
            if i < begin:
                continue
            line = line.decode('utf-8').strip()
            res.append(line)
    return res


def save_to_txt(filename, contents):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(contents) + '\n')


def add_to_txt(filename, contents):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write('\n'.join(contents) + '\n')
