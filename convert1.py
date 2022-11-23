def split_string(s):
    count = 0
    label = s.split(" ", 1)[0]  # label
    rest = s.split(" ", 1)[1]  # input
    input = ""
    output = ""
    setting = ""
    temp = ""
    index = 0
    for c in rest:
        if count != 0:
            temp = temp + c

        if c == "{":
            count = count + 1
        elif c == "}":
            count = count - 1
            if count == 0:
                temp = temp[:-1]
                if index == 0:
                    input = temp
                elif index == 1:
                    output = temp
                else:
                    setting = temp
                temp = ""
                index += 1

    if index != 3:
        raise EOFError

    return label, input, output, setting


DICT = {}
SETTING_DICT = {"optional": "opt", "rewrite": "obl"}


def process_str(s):
    s1 = s
    s2 = s1.replace("{", "")
    s3 = s2.replace("}", "")
    s_list = s3.split(" ")
    return s_list


def process_output(input, output):
    input_list = process_str(input)
    out_list = process_str(output)
    result = []
    for v in out_list:
        if v.startswith("$"):
            index = v[1:]
            # print("add index {} in input".format(index))
            result.append(input_list[int(index)])
        else:
            result.append(v)
    # print("input is {}".format(input_list))
    # print("output is {}".format(result))
    return result


def gen_line0(input, output, label):
    input_list = process_str(input)
    out_list = process_output(input, output)
    line0 = "regroup_{}{} = ( ".format(label, str(DICT[label]))
    for i in input_list:
        line0 += "\"{}\".syms".format(i)
    line0 += " : "
    for o in out_list:
        line0 += "\"{}\".syms".format(o)
    line0 += "\"*{}\".syms )".format(str(DICT[label]))
    return line0 + "\n"


def gen_line1(label, setting):
    line1 = "{}{} = CDRewrite[regroup_{}{} , \"\".syms , \"\".syms , phones_star , 'ltr'".format(label,
                                                                                                 str(DICT[label]),
                                                                                                 label,
                                                                                                 str(DICT[label]))
    if SETTING_DICT.__contains__(setting):
        line1 += " , '{}' ]".format(SETTING_DICT[setting])
    return line1 + "\n"


def gen_line2(label):
    line2 = "export _P3 = Optmize[{}{}]".format(label, str(DICT[label]))
    return line2 + "\n"


if __name__ == '__main__':
    content = ""
    with open('lts_en_us_12.9.0_phonRules_Default.txt') as f:
        countLine = 0
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            label, input, output, setting = split_string(line)
            if DICT.__contains__(label):
                DICT[label] += 1
            else:
                DICT[label] = 0
            content += gen_line0(input, output, label)
            content += gen_line1(label, setting)
            content += gen_line2(label)

    with open('convert.txt', 'w') as f:
        f.write(content)


