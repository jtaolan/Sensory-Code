def split_string(s):
    count = 0
    label = s.split(" ", 1)[0]
    rest = s.split(" ", 1)[1]
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


content = ""
with open('lts_en_us_12.9.0_phonRules_Default.txt') as f:
    settingDict = {"optional": "opt", "rewrite": "obl"}
    countLine = 0
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        label, input, output, setting = split_string(line)
        input = input.split()
        output = output.split()


        line1 = ""
        line2 = ""
        line3 = ""
        line1 = 'regroup_' + label + str(countLine) + " = ( "
        for input_i in input:
            if input_i[0] == '{' and input_i[-1] == '}':
                input_i = input_i[1:len(input_i)-2]
            line1 = line1 +  '"' + input_i +  '".syms'
        line1 = line1 + ' : '
        for output_i in output:
            if output_i[0] == '{' and output_i[-1] == '}':
                output_i = output_i[1:len(output_i)-1]
            if output_i[0] == '$':

            line1 = line1 + output_i + '.syms"*' + str(countLine) + '".syms);'
        if setting == "ignored":
            line2 = label + '0 = CDRewrite[regroup_' + label + '0 , "".syms ,"".syms' + \
                    " , phones_star , 'ltr'];"
        else:
            line2 = label + '0 = CDRewrite[regroup_' + label + '0 , "".syms ,"".syms' + \
                    " , phones_star , 'ltr' , '" + settingDict[setting] + "' ];"

        line3 = "export _P3 = Optimize[" + label + "0];"
        content += line1 + "\n" + line2 + "\n" + line3 + "\n"

        countLine += 1


with open('convert.txt', 'w') as f:
    f.write(content)


# dict = {}
# s = "aaabbbcccc"
# for c in s:
#    if c in dict:
#        count = dict[c]
#        dict[c] = count+1
#    else:
#        dict[c] = 1
#
# from collections import defaultdict
#
#
# label = ["word", "word", "word", "word", "word", "word"]
#
# de_dict = defaultdict(int)
# for c in label:
#     count = de_dict[c]
#     print(c + str(count))
#     de_dict[c] = count+1
#
# print(de_dict)