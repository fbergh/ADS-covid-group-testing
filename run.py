########## IMPORTS ##########

# Standard library imports
import os
import platform
import argparse


########## RUN FILE ##########

if __name__ == '__main__':
    # Parse input
    ap = argparse.ArgumentParser(description = "Run the algorithm on the full problem set for a given number of iterations")
    ap.add_argument("-n", "--iterations", help="number of iterations", type=int, default=1)
    args = vars(ap.parse_args())
    
    # Set command
    if platform.system() == "Windows":
        command = "ncat -c \"python .\main.py\" group-testing.maarse.xyz 6525"
    else:
        command = "ncat -c 'python3 ./main.py' group-testing.maarse.xyz 6525"

    # Run problem set for the given number of iterations
    for i in range(args["iterations"]):
        print(f"\nIteration {i+1} out of {args['iterations']}\n")
        os.system(command)