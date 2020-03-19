# Cable_Duplicates
Program for searching duplicates in csv-file and giving new names for them

This program was created to resolve the following task.

Task:

A list of cable names is given in the form of csv-file. 
The names look as follows: "N-CODE-Number" - three portions separated by "-" where "Number" portion is a natural number that 
represents the number of a cable. The problem was that this "Number" must be unique, but in the given file some cables had the same
third portion and it had to be resolved. 

So this program makes the following: 

- Searching for duplicates by "Number" portion.
- Assigning new "Number" for each duplicate cable and for new "Number" it takes the minimum natural number that did not occur 
  as the cable "Number" in the initial list of cables and in already processed duplicates.
- Saving the full list of cables after processing and list of duplicates after processing as excel files. Resulting files contain 
  the initial order number (from initial csv-file), initial cable name, initial cable number, new number and new name (last two
  are changed in duplicates or unchanged otherwise).

Repository contains the program python file, initial list of cables (csv) and two excel files with processed list of cables and list of
duplicates.
