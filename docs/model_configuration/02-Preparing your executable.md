## Preparing your executable

Ultimately, a user will want to run your code with whatever data is available. However, for the purpose of encapsulating your software, think of the MIC process as a test run. Therefore, we strongly advise that you are prepared to run with the minimum amount of data needed for an execution test. For instance, if your software is used to model hydrologic processes, can you test the software with just 3 hours worth of hourly data or do you really need to run the entire day? Remember that at this stage, you are testing whether the component is encapsulated successfully not that it will work for all data, regardless of whether they have been preprocessed successfully nor that the results are scientifically correct.

Once you are ready to proceed:

1. Place your software code in a local directory so it can be invoked from a command line along with any input data and configuration files if applicable. MIC will test that the code can be executed and will do so three times during the encapsulation process. Therefore, we recommend that your execution can be completed in a manner of minutes, for example, by reducing the size of the dataset (e.g., only considering a few months instead of a year). Because of GitHub limitations, files should not exceed **100 MB** each.
2.  The code should not contain any hardcoded paths or values for the input files/variables that you wish to expose. We recommend making them explicit in a configuration file or as parameters from the command line execution.

## Parameters

From here you have two options to continue:

* Option 1: The parameters to the model are passed using a command line invocation such as:

```bash
$ python mysoftware.py p1 p2 p3
```

* Option 2: The parameters are passed through configuration files, themselves inputs in the command line invocation:

```bash
$ python mysoftware.py config.json
```

Depending on which of the two options your software falls under, the encapsulation steps are slightly different. If you are using a mix of config files and command line parameters, you will need to merge the instructions (namely steps 3, 4 and 7).
