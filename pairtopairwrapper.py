import os
from shutil import copyfile
import re
import pandas as pd


# splits lines into columns and compares the first six of the full list and matched list
# returns a list of the items in full_list
# return list(set(full_list) - set(match_list))
def filter_list(full_list, match_list):
    # split_full = []
    # split_match = []
    # filtered_split = []
    # filtered_full = []
    # for item in full_list:
    #     split_full.append(re.split(r'\t+', item))
    # for item in match_list:
    #     split_match.append(re.split(r'\t+', item))
    # for item in split_full:
    #     for match_item in split_match:
    #         if item[0] == match_item[0]\
    #                 and item[1] == match_item[1]\
    #                 and item[2] == match_item[2]\
    #                 and item[3] == match_item[3]\
    #                 and item[4] == match_item[4]\
    #                 and item[5] == match_item[5]:
    #             break
    #     else:
    #         filtered_split.append(item)
    # for item in filtered_split:
    #     filtered_full.append("\t".join(item))
    # return filtered_full
    filtered_list = pd.DataFrame([])

    return 0


# appends a python list extracted via file_extract() to given file directory and name
# args are file_to_append, (the name of the python list to be appended), path to the file, and output_name (name of output)
def file_appender(file_to_append, path, output_name):
    filename = os.path.join(path, "{}".format(output_name))
    with open(filename) as file:
        file_to_append.to_csv(path_or_buf=file, sep="\t", mode="a", index=False)
    # filename = os.path.join(path, "{}".format(output_name))
    # f = open(filename, "a")
    # for line in file_to_append:
    #     f.write("{}".format(line))
    # f.close()


# writes file back to OS
def file_rewriter(file_to_rewrite, path, output_name):
    # filename = os.path.join(path, "{}".format(output_name))
    # f = open(filename, "w+")
    # for line in file_to_rewrite:
    #     f.write("{}".format(line))
    # f.close()
    file_to_rewrite.to_csv(path_or_buf="{}/{}".format(path, output_name), sep="\t", mode="w+")


# extracts the data from a bedpe file into a list of strings
def file_extract(file_path):
    # return_list = []
    # with open(file_path) as file:
    #     for line in file:
    #         return_list.append(line)
    # file.close()
    # return return_list
    e = 0
    with open(file_path) as file:
        for line in file:
            if line[0] == "#":
                e = e + 1

    return_list = pd.read_csv(file, sep="\t", skiprows=e)
    return return_list


# iteratively uses bedtools pairtopair to apply slops from starting slop, incrementing by slop_increment until the stop_slop
# args are file_a, file_b, bedtools_path, start_slop, slop_increment, stop_slop, output directory, & an optional output name
def iterative_slop(inp_file_a, inp_file_b, bedtools_path, start_slop, slop_increment, stop_slop, output_directory, name):  # strip split and compare first six entries in each list, remove last
    int_start_slop = int(start_slop)
    int_slop_increment = int(slop_increment)
    int_stop_slop = int(stop_slop)
    name = os.path.join(output_directory, name)
    output_file = open(name, "w+")
    output_file.close()
    int_current_slop = int_start_slop
    copyfile(inp_file_a, "{}/temp_file_a".format(output_directory))
    copyfile(inp_file_b, "{}/temp_file_b".format(output_directory))
    file_a = "{}/temp_file_a".format(output_directory)
    file_b = "{}/temp_file_b".format(output_directory)
    while int_current_slop <= int_stop_slop:
        ex_file_a = file_extract(file_a)
        ex_file_b = file_extract(file_b)
        os.system("{} pairtopair -slop {} -a {} -b {} > {}/temp_a_{}".format(bedtools_path, int_current_slop, file_a, file_b, output_directory, int_current_slop))
        os.system("{} pairtopair -slop {} -a {} -b {} > {}/temp_b_{}".format(bedtools_path, int_current_slop, file_b, file_a, output_directory, int_current_slop))
        intersected_temp_a = file_extract("{}/temp_a_{}".format(output_directory, int_current_slop))
        intersected_temp_b = file_extract("{}/temp_b_{}".format(output_directory, int_current_slop))
        ex_file_a = filter_list(ex_file_a, intersected_temp_a)
        ex_file_b = filter_list(ex_file_b, intersected_temp_b)
        file_rewriter(ex_file_a, output_directory, "temp_file_a")
        file_rewriter(ex_file_b, output_directory, "temp_file_b")
        file_appender(intersected_temp_a, output_directory, name)
        int_current_slop = int_current_slop + int_slop_increment
    os.system("rm {}/temp*".format(output_directory))


if __name__ == "__main__":
    iterative_slop(input("Path to input file a: "),
                   input("Path to input file b: "),
                   input("Path to bedtools: "),
                   input("Starting slop: "),
                   input("Slop increment: "),
                   input("Slop cap: "),
                   input("Output directory: "),
                   input("Name of output file: "))
    print("Done")
