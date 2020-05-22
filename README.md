# User Manual
## Authors
- Jessica Cunha, 2016239495, jessicac@student.uc.pt
- Ricardo Paiva, 2016253100, rjpaiva@student.uc.pt

## Requirements
- python3
    - necessary libraries: random, copy, math, json, os, pandas, numpy, matplotlib, scipy, 
- R

# FAQ

### 1 - How to run the code

1 - Choose the parameters in the file <parameters.py> that you want to test

2 - Run the file <main.py> (see 2.1 if help is needed), and you'll see the best individual of each generation printed in the terminal. If you didn't changed the code, a folder will be created with the best individual of each generation and inside, a *log* folder with the fitness of all individuals of each generation. To avoid this folder of being generated see **section 4**


2.1 - You can run the code by using an IDE (suggestion: PyCharm) or, if you're using Linux or MacOS, the terminal, by running:
<python3 main.py>

### 2 - How to generate the plots

For this you need to have R installed on your computer or the IDE RStudio.
1 - Open the file <plot_generators.r>

2 - Change the directory, to the folder where you have the files <best.txt> (this will be generated when running the code in **1**)

3 - Run the file by using RStudio or in the terminal:

<Rscript plot_generator.r>

### 3 - How to do the statistical tests

1 - Open the file <stat_alunos.py>

2 - Change the code to load the data from the folder where your tests are. Note: The step **2** needs to be done first.

3 - Run the file by using an IDE or running in the terminal:

<python3 stat_alunos.py>

### 4 - I don't want to have the log folder with the fitness with all individuals
1 - Comment the lines 297 and 300-301 of the file <main.py>