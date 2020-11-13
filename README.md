# Algorighms and Data Structures
## Practical Assignment 1
### Group Testing for Covid-19
##### Submission group 88: Freek van den Bergh (s4801709) and Max Driessen (s4789628)

This repository contains our code for the Group Testing for Covid-19 assignment of Algorithms and Data Structures. The files in the root folder contain generic code for running the algorithm, a graph data structure, server communication and logging. The files in the `algorithm` folder contain code specific to our algorithm.
In order to run our code, you can use either of the following commands:<br>
``ncat -c 'echo 'USERNAME' && echo 'PASSWORD' && python3 ./main.py' group-testing.maarse.xyz 6525``<br>
``python3 run.py <iterations> -u 'USERNAME' -p 'PASSWORD'``<br>
``python3 run.py <iterations> -c 'COMMAND'``<br>
where `USERNAME` and `PASSWORD` are the server credentials, `<iterations>` is the number of times you want to run the full test on the server, and `COMMAND` is the full command you want to run (inclusing `USERNAME` and `PASSWORD`).
