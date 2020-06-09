import re
import os


def file_rewriter(file_to_rewrite, path, output_name):
    filename = os.path.join(path, "{}".format(output_name))
    f = open(filename, "w+")
    for line in file_to_rewrite:
        f.write("{}".format(line))
    f.close()


def file_extract(file_path):
    return_list = []
    with open(file_path) as file:
        for line in file:
            if line[0] != "#":
                return_list.append(line)
    file.close()
    return return_list


def dup_remover(file_path, output_path):
    file = file_extract(file_path)
    file_output = []
    for line in file:
        if line not in file_output:
            file_output.append(line)

    a = "".join(re.split('/', file_path)[-1:])
    file_rewriter(file_output, output_path, "{}{}".format(a, '_no_duplicates'))


if __name__ == "__main__":
    inp = input('Inp path:\n')
    output_dir = input('Output directory and name:\n')
    dup_remover(inp, output_dir)
    print('done')
