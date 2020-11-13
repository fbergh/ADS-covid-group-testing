########## IMPORTS ##########

# Standard library imports
import os
import platform
import argparse


########## RUN FILE ##########

if __name__ == '__main__':
    

    # Parse input
    ap = argparse.ArgumentParser(description = "Run the algorithm on the full problem set for a given number of iterations")
    ap.add_argument("iterations", help="number of iterations", type=int)
    ap.add_argument("-u", "--username", help="username for server", type=str, default="")
    ap.add_argument("-p", "--password", help="password for server", type=str, default="")
    ap.add_argument("-c", "--command", help="command to run (including username & password)", type=str, default="")
    args = vars(ap.parse_args())

    # Make sure that either a username and password or a command was provided
    assert (args["username"] and args["password"]) or args["command"], "Missing username & password or command"

    # Set default command if command is empty
    command = args["command"]
    if not command:
        if platform.system() == "Windows":
            command = f"ncat -c \"echo {args['username']} && echo {args['password']} && python .\main.py\" group-testing.maarse.xyz 6525"
        else:
            command = f"ncat -c 'echo {args['username']} && echo {args['password']} && python3 ./main.py' group-testing.maarse.xyz 6525"
    
    # Run problem set for the given number of iterations
    for i in range(args["iterations"]):
        print(f"\nIteration {i+1} out of {args['iterations']}\n")
        os.system(command)