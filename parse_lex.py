DICT = {}

def count_lex():
    with open('g.lex') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            if '(' in line and ')' in line:
                key = line[0:line.index("(")]
                print(key)
                DICT[key] += 1

            else:
                key = line.split(" ", 1)[0]
                DICT[key] = 1
    print(DICT)


if __name__ == '__main__':
    count_lex()
