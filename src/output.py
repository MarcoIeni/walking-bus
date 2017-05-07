import os


def generate_output(edges, filename):
    # out_file = open("solutions/output_" + alg + "_" + filename + ".sol", "w")

    SOLUTIONS_PATH = ".." + os.path.sep + "solutions"

    if not os.path.exists(SOLUTIONS_PATH):
        os.makedirs(SOLUTIONS_PATH)
        out_file = open(SOLUTIONS_PATH + os.path.sep + filename + ".sol", "w")
        for e in edges:
            out_file.write(str(e[1]) + " " + str(e[0]) + "\n")
        out_file.close()
