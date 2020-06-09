import os
import re


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


gene_indexes = [['chr11', 7668402, 7687550, 'p53'], ['chr5', 112707498, 112849239, 'APC'],
                ['chr9', 136494433, 136545786, 'NOTCH1'], ['chr17', 85311244, 85347066]]


def range_comparison(input_file):
    py_inp = file_extract(input_file)
    output_matches = []
    for point in py_inp:
        split = re.split(r'\t+', point)
        for index in gene_indexes:
            if (split[0] == index[0] and ((index[1] < int(split[1]) < index[2]) or (index[1] < int(split[2]) < index[2])))\
                    or (split[3] == index[0] and ((int(split[4]) > index[1] and int(split[5]) < index[2]) or\
                                                  (int(split[4]) > index[1] and int(split[6]) < index[2]))):
                output_matches.append(f"{input_file} contains breakpoints overlapping {index[3]}")
    return output_matches


# takes inputs and runs iterative slop on them
if __name__ == "__main__":
    a = input('Input files to compare, separate inputs with ", ". \n')
    sep_output = a.split(", ")
    for item in sep_output:
        b = item.split(" ")
        print(range_comparison(item))
    print("Done with comparisons")
