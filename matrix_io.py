# Library imports
import numpy as np
import sys
import os.path

def input_matrix(filename):
    # Return array contained in filename

    input_file = open(filename,"r")

    num_cols = len(input_file.readline().split())
    input_file.seek(0)

    num_rows = sum(1 for line in input_file)
    input_file.seek(0)

    matrix = np.array([[None for i in range(num_cols)] 
                             for i in range(num_rows)])
    line_num = 0

    while True:
        line = input_file.readline()
        if not line: break
        matrix[line_num,:] = line.split()
        line_num += 1

    input_file.close()

    return matrix, num_cols, num_rows

def print_matrix(matrix):
    # Print matrix neatly to stdout

    num_cols = matrix.shape[0]
    num_rows = matrix.shape[1]

    for i in range(num_cols):
        for j in range(num_rows):
            sys.stdout.write("%6f" % matrix[i,j])
            if j != num_rows:
                sys.stdout.write(", ")
        print

def print_matrix_to_file(matrix, filename):
    # Take NumPy 2D array and print it to file for external verification/plotting

    if os.path.isfile(filename):
        response = str(raw_input("Warning, chosen output file already exists. Overwrite? "))
        if response.lower() == "yes" or response.lower() == "y":
            print "Continuing..."
        elif response.lower() == "no" or response.lower() == "n":
            print "Aborting... "
            exit(2)
        else:
            print "Unrecognised response. Aborting..."
            exit(3)

    output_file = open(filename, 'w')

    num_cols = matrix.shape[0]
    num_rows = matrix.shape[1]

    try:
        for i in range(num_cols):
            for j in range(num_rows):
                output_file.write("%6f\t" % matrix[i,j])
            output_file.write("\n")

    finally:
        output_file.close()
    # Ensure file is properly closed, even if writing to file fails
