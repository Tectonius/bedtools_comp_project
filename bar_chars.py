import matplotlib.pyplot as plt
import os

TenX = [['10X'], ['DEL', 'INS', 'TRA', 'INV', 'UNK'],
        ['BioNano', 'Illumina', 'PacBio', 'PacBio_chr6', 'Original_BEDPE'],
        [47, 0, 182, 22, 174],
        [22, 0, 799, 8, 788],
        [44, 0, 762, 15, 753],
        [6, 0, 700, 3, 684],
        [1693, 0, 992, 2684, 1437]]

BioNano = [['BioNano'], ['DEL', 'INS', 'TRA', 'INV', 'DUP'],
           ['10X', 'Illumina', 'PacBio', 'PacBio_chr6', 'Original_BEDPE'],
           [71, 16, 199, 40, 37],
           [34, 8, 177, 14, 29],
           [1048, 1917, 160, 52, 30],
           [95, 193, 150, 8, 1],
           [1702, 4082, 229, 214, 140]]

Illumina = [['Illumina'], ['inv', 'del', 'tandem-dup', 'transloc'],
            ['10X', 'BioNano', 'PacBio', 'PacBio_chr6', 'Original_BEDPE'],
            [396, 233, 214, 16],
            [73, 70, 71, 0],
            [404, 257, 227, 43],
            [360, 215, 179, 5],
            [504, 307, 270, 192]]

PacBio = [['PacBio'], ['TRA', 'DUP', 'DEL', 'INS', 'INV', 'INVDUP', 'DUP/INS'],
          ['10X', 'BioNano', 'Illumina', 'Original_BEDPE'],
          [24, 208, 247, 0, 380, 0, 0],
          [0, 522, 769, 622, 83, 0, 3],
          [43, 235, 261, 1, 389, 3, 0],
          [352, 1777, 4547, 4901, 573, 3, 13]]

PacBio_chr6 = [['PacBio_chr6'], ['<TRA>', '<DUP>', '<DEL>', '<INS>', '<INV>', '<INVDUP>', '<DUP/INS>'],
               ['10X', 'BioNano', 'Illumina', 'Original_BEDPE'],
               [2, 171, 200, 0, 344, 0, 0],
               [0, 81, 88, 50, 54, 0, 0],
               [5, 186, 217, 0, 351, 0, 0],
               [12, 285, 481, 337, 381, 0, 1]]

plt.style.use('ggplot')


def x_plot(array):
    for i in range(len(array[2])):
        x_pos = [a for a, _ in enumerate(array[1])]
        plt.tight_layout()
        plt.gcf().subplots_adjust(bottom=0.15)
        plt.bar(x_pos, array[i+3], color='blue')
        plt.xlabel('SV Type')
        plt.ylabel('# of SVs')
        plt.title(f'{array[0][0]}_{array[2][i]}_SV_plot_June_9')
        plt.xticks(x_pos, array[1], rotation='vertical')
        plt.savefig(fname='temp.png')
        os.system(f'mv /Users/ae10/PycharmProjects/barchart_VCFS/temp.png /Users/ae10/Desktop/tests/SV_Type_plots/{array[0][0]}_{array[2][i]}_SV_plot_June_9')


x_plot(TenX)
x_plot(BioNano)
x_plot(Illumina)
x_plot(PacBio)
x_plot(PacBio_chr6)
