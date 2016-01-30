# CCC Grader

A Python script to grade Python CCC solutions along with CCC data from 
2005 - 2015.

## Usage Example

You have written a solution to question 5 on the 2015 Junior CCC and 
have the source code of your solution stored in /home/user/junior5.py. 
To grade it, use the following command:

```python grader.py /home/user/junior5.py 2015 j5```

You should get an output similar to the following

```
j5.1.in PASS
j5.10.in TIMEOUT
j5.2.in PASS
j5.3.in PASS
j5.4.in PASS
j5.5.in PASS
j5.6.in PASS
j5.7.in PASS
j5.8.in PASS
j5.9.in TIMEOUT
```

## Data

Test data from 2005 - 2015 is in the data.tar.gz tarball.
Problem s4 from 2009 and s4 from 2013 are not included in the data
due to the size of their input and output files

The grader will by default look in ./data for test data, if you have the
test data stored in another place, use the ```--data_path``` argument
to specify the path to the files.
