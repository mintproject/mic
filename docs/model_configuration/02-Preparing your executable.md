## Preparing your executable

Ultimately, a user will want to run your code with whatever data is available. However, for the purpose of encapsulating your software, think of the MIC process as a test run. Therefore, we strongly advise that you are prepared to run with the minimum amount of data needed for an execution test. For instance, if your software is used to model hydrologic processes, can you test the software with just 3 hours worth of hourly data or do you really need to run the entire day? Remember that at this stage, you are testing whether the component is encapsulated successfully not that it will work for all data, regardless of whether they have been preprocessed successfully nor that the results are scientifically correct.

Once you are ready to proceed, we offer two options for encapsulation:

* Using a Jupyter Notebook and MIC
* Using the MIC command line

## What do we mean by input files and parameters?

Any variables in a model can be represented either as an input file or a parameter. The distinction here is purely practical. If the variable value is contained in a file, then it is an input file. If the value is represented as a single number, then it is considered a parameter.

Let's take a simple example of a model that fits a line through data: `y=ax+b`. The command line invocation looks like:

```bash
$ python linearregression.py x.csv a b
```
For MIC, `x` is considered an input file and `a` and `b` are considered parameters with the value assigned during the command line invocation.

## Jupyter Notebook

Use a Jupyter Notebook to expose the files and parameters. Make sure that it is Binder-executable and available through a public GitHub repository. This option can be preferred if the software was written in Python and already written in Notebook format or can easily be transferred to one. This might be the case, for instance, for data transformation software.

If you would like to proceed with this option, the next step is to [prepare your notebook](../notebooks/index.md).

## MIC Command line

If the software is not written in Python or cannot be practically encapsulated in a notebook, using the command line version of MIC might be easier. To do so:

1. Place your software code in a local directory so it can be invoked from a command line along with any input data and configuration files if applicable. MIC will test that the code can be executed and will do so three times during the encapsulation process. Therefore, we recommend that your execution can be completed in a manner of minutes, for example, by reducing the size of the dataset (e.g., only considering a few months instead of a year). 

2.  The code should not contain any hardcoded paths or values for the input files/variables that you wish to expose. We recommend making them explicit in a configuration file or as parameters from the command line execution.

### Parameters

From here you have two options to continue (click on the option to follow the rest of the instructions):

* [Option 1](/model_configuration/03a-step1): The parameters to the model are passed using a command line invocation such as:

```bash
$ python mysoftware.py p1 p2 p3
```

* [Option 2](/model_configuration/03a-step1): The parameters are passed through configuration files, themselves inputs in the command line invocation:

```bash
$ python mysoftware.py config.json
```

Depending on which of the two options your software falls under, the encapsulation steps are slightly different. If you are using a mix of config files and command line parameters, you will need to merge the instructions (namely steps 3, 4 and 7).
