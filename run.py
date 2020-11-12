########## IMPORTS ##########

# Standard library imports
import os
import platform
import argparse


########## RUN FILE ##########

if __name__ == '__main__':
    # Set default command
    if platform.system() == "Windows":
        command = "ncat -c \"python .\main.py\" group-testing.maarse.xyz 6525"
    else:
        command = "ncat -c 'python3 ./main.py' group-testing.maarse.xyz 6525"

    # Parse input
    ap = argparse.ArgumentParser(description = "Run the algorithm on the full problem set for a given number of iterations")
    ap.add_argument("iterations", help="number of iterations", type=int)
    ap.add_argument("-c", "--command", help="command to run", type=str, default=command)
    args = vars(ap.parse_args())
    
    # Run problem set for the given number of iterations
    for i in range(args["iterations"]):
        print(f"\nIteration {i+1} out of {args['iterations']}\n")
        os.system(args['command'])