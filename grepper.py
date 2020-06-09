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


def grepper(file_path):
    file = file_extract(file_path)
    breakpoints = []
    for line in file:
        split_line = re.split(r'\t', line)
        if len(split_line) > 5:
            breakpoints.append(f"{split_line[0]} {split_line[1]} {split_line[2]} {split_line[3]} {split_line[4]} {split_line[5]} {split_line[6]} {os.linesep}")
    # file_rewriter(breakpoints, '/Users/ae10/Desktop', 'bionano_test')
    return [len(set(breakpoints)), len(breakpoints)]


if __name__ == "__main__":
    inp = input('Grepper paths, separate with ", "\n')
    sep_output = inp.split(", ")
    for item in sep_output:
        a = grepper(item)
        print('Grepper for {}'.format(item))
        print("{} number of breakpoints in output file".format(a[1]))
        print("{} number of breakpoints with duplicates removed".format(a[0]))
        print('\n')
