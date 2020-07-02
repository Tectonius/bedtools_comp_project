import os
from shutil import copyfile
import re
import matplotlib.pyplot as plt


# splits lines into columns and compares the first six of the full list and matched list
# returns a list of the items in full_list
def filter_list(full_list, match_list):
    split_full = []
    split_match = []
    filtered_split = []
    filtered_full = []
    for item_a in full_list:
        split_full.append(re.split(r'\t+', item_a))
    for item_a in match_list:
        split_match.append(re.split(r'\t+', item_a))
    for item_a in split_full:
        for match_item in split_match:
            if item_a[0].strip() == match_item[0].strip()\
                    and item_a[1].strip() == match_item[1].strip()\
                    and item_a[2].strip() == match_item[2].strip()\
                    and item_a[3].strip() == match_item[3].strip()\
                    and item_a[4].strip() == match_item[4].strip()\
                    and item_a[5].strip() == match_item[5].strip():
                break
        else:
            filtered_split.append(item_a)
    for item_a in filtered_split:
        filtered_full.append("\t".join(item_a))
    return filtered_full


# appends a python list extracted via file_extract() to given file directory and name
# args are file_to_append, (the name of the python list to be appended), path to the file, and output_name (name of output)
def file_appender(file_to_append, output_path, output_name):
    output_file = open(os.path.join(output_path, "temp_append"), "w+")
    output_file.close()
    file_rewriter(file_to_append, output_path, "temp_append")
    os.system("cat {} >> {}".format(os.path.join(output_path, "temp_append"), os.path.join(output_path, output_name)))
    os.system("rm {}".format(os.path.join(output_path, "temp_append")))


# writes file back to OS
def file_rewriter(file_to_rewrite, path, output_name):
    filename = os.path.join(path, "{}".format(output_name))
    f = open(filename, "w+")
    for line in file_to_rewrite:
        f.write("{}".format(line))
    f.close()


# extracts the data from a bedpe file into a list of strings
def file_extract(file_path):
    return_list = []
    with open(file_path) as file:
        for line in file:
            if line[0] != "#":
                return_list.append(line)
    return return_list


# replaces a file with a cut version containing only the columns one through six
def cut_temp(file_path):
    os.system("cut -f1,2,3,4,5,6 {} > {}_cut".format(file_path, file_path))
    os.system("mv {}_cut {}".format(file_path, file_path))


def dup_remover(file):
    output_list = []
    for point in file:
        if point not in output_list:
            output_list.append(point)
    return output_list


# appends the data cut from a file by cut_temp back to the appropriate lines
def uncut_output(cut_final, full_inp):
    return_array = []
    for item_a in cut_final:
        for line in full_inp:
            item_a = item_a.strip('\n')
            line = line.strip('\n')
            item_split = re.split(r'\t+', item_a)
            line_split = re.split(r'\t+', line)
            if item_split[0] == line_split[0] and item_split[1] == line_split[1] and item_split[2] == line_split[2] and item_split[3] == line_split[3] and item_split[4] == line_split[4] and item_split[5] == line_split[5]:
                return_array.append(item_a + '\t' + '\t'.join(re.split(r'\t+', line)[6:]) + '\n')
    return return_array


# iteratively uses bedtools pairtopair to apply slops from starting slop, incrementing by slop_increment until the stop_slop
# args are file_a, file_b, bedtools_path, start_slop, slop_increment, stop_slop, output directory, & an optional output name
def iterative_slop(inp_file_a, inp_file_b, bedtools_path, start_slop, slop_increment, stop_slop, output_directory, name):
    int_start_slop = int(start_slop)
    int_slop_increment = int(slop_increment)
    int_stop_slop = int(stop_slop)
    rname = name
    name = os.path.join(output_directory, name)
    open(name, "w+")
    int_current_slop = int_start_slop
    copyfile(inp_file_a, "{}/temp_file_a".format(output_directory))
    copyfile(inp_file_b, "{}/temp_file_b".format(output_directory))
    file_a = "{}/temp_file_a".format(output_directory)
    file_b = "{}/temp_file_b".format(output_directory)
    full_inp_a = file_extract(file_a)
    full_inp_b = file_extract(file_b)
    cut_temp(file_a)
    cut_temp(file_b)
    x = [0]
    y = [0]
    name_len = 0
    while int_current_slop <= int_stop_slop:
        ex_file_a = file_extract(file_a)
        ex_file_b = file_extract(file_b)
        a_input = "{} -slop {} -a {} -b {} > {}/temp_a_{}".format(bedtools_path, int_current_slop, file_a, file_b, output_directory, int_current_slop)
        b_input = "{} -slop {} -a {} -b {} > {}/temp_b_{}".format(bedtools_path, int_current_slop, file_b, file_a, output_directory, int_current_slop)
        os.system(a_input)
        os.system(b_input)
        dup_temp_a = file_extract('{}/temp_a_{}'.format(output_directory, int_current_slop))
        dup_temp_b = file_extract('{}/temp_b_{}'.format(output_directory, int_current_slop))
        dup_temp_a = dup_remover(dup_temp_a)
        dup_temp_b = dup_remover(dup_temp_b)
        file_rewriter(dup_temp_a, output_directory, '{}/temp_a_{}'.format(output_directory, int_current_slop))
        file_rewriter(dup_temp_b, output_directory, '{}/temp_b_{}'.format(output_directory, int_current_slop))
        intersected_temp_a = file_extract("{}/temp_a_{}".format(output_directory, int_current_slop))
        intersected_temp_b = file_extract("{}/temp_b_{}".format(output_directory, int_current_slop))
        name_len += len(intersected_temp_a)

        # filters out bedtools outputs from future pairtopairs
        ex_file_a = filter_list(ex_file_a, intersected_temp_a)
        ex_file_b = filter_list(ex_file_b, intersected_temp_b)

        # writes filtered breakpoint sets back onto files

        file_rewriter(ex_file_a, output_directory, "temp_file_a")
        file_rewriter(ex_file_b, output_directory, "temp_file_b")

        file_appender(intersected_temp_a, output_directory, name)
        int_current_slop = int_current_slop + int_slop_increment
        x.append(int_current_slop)
        y.append(name_len)
    cut_output = file_extract(name)
    final_output = uncut_output(cut_output, full_inp_a)
    print(str(len(final_output)) + " is the length of the final output")
    file_rewriter(final_output, output_directory, name)
    plt.plot(x, y)
    plt.ylabel("Cumulative number of hits")
    plt.xlabel("Slop")
    plt.savefig(fname="temp.png")
    os.system("mv temp.png {}/{}.png".format(output_directory, rname))
    os.system("rm {}/temp*".format(output_directory))
    plt.clf()


# takes inputs and runs iterative slop on them
if __name__ == "__main__":
    a = input('iterative slop args (Path to input file a, Path to input file b, Path to bedtools pairtopair, Starting slop, Slop increment, Slop cap, Output directory, Name of output file). Separate inputs with a ", ". \n')
    sep_output = a.split(", ")
    for item in sep_output:
        b = item.split(" ")
        iterative_slop(b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7])
        print(f"Done with {b[7]}")
