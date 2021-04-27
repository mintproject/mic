

We use IPython2CWL for a tool for converting [IPython](https://ipython.org/) Jupyter Notebooks to
[CWL (Common Workflow Language)](https://www.commonwl.org/) Command Line Tools by simply providing typing annotation.

## Supported Types

### Basic Data Types

Each variable can be an input or an output. The basic data types are:

- Inputs:
    - CWLFilePathInput
    - CWLBooleanInput
    - CWLStringInput
    - CWLIntInput

- Outputs:
    - CWLFilePathOutput
    - CWLDumpableFile
    - CWLDumpableBinaryFile

## Example

In our example, we have parameters (variables: a, b, c), a input file (variable: input_file) and a output file (variable: output_file)

```python
a = 5
b = 4
c = 6
input_file = "./x.csv"
output_file = "./y.csv"
```


You should annotate them using CWL typing annotation and the result will be:


```python
a : 'CWLIntInput' = 5
b : 'CWLIntInput' = 4
c : 'CWLIntInput' = 6
input_file : 'CWLFilePathInput' = "./x.csv"
output_file : 'CWLFilePathOutput' = "./y.csv"
```

You can check the final notebook at

```
https://github.com/mosoriob/simpleModel-1/blob/master/simpleModelAnnotated.ipynb
```



## Before to continue

Go to [mybinder.org](mybinder.org) and run the whole notebook without errors. If it works, continue
