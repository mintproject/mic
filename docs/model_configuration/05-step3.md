Models may use many parameters and input files, but we may not need to expose all of them as part of our model component. If you know individual parameters that you would like to expose in your model component, you may expose them with the `parameters` command.

If your using a `config` file to set the input variables values and file path, you still need to complete this step, entering each of the parameters you wish to expose from the file one at a time.

### How to perform this step?

In our Java executable, we only had one parameter to expose through the command line (the parameter `p`). Note that you should use the `-f` option with the path of the mic file, typically under the `mic/mic.yaml` path:

```bash
$ mic pkg parameters -f mic/mic.yaml -n p -v 1350
Adding the parameter p, value 1350 and type int
```
The `-n` flag stands for `parameter name` and the `-v` flag stands for the default value you would like the parameter to have. In the case above, we defined a parameter `p` with value `1350`. MIC detected that it was an integer.

!!! warning
    Parameters are case sensitive: a parameter `start_year` is different from `START_YEAR`.

### Expected result

If you edit the mic.yaml file, you should see that the parameter has been added. We **encourage** adding a description so the role of the parameter becomes clear:

```yaml
parameters:
  p:
    default_value: 1350
    type: int
    description: 'Input parameter used in the model'
```

You can also add the parameter yourself to the `mic.yaml` file directly, if you prefer.

**Note**: If your parameters are declared in a configuration file, you must also complete the next step `mic pkg configs`.

### Help command

```bash
root@32fee4e4d205:/tmp/mint# mic pkg parameters --help
Usage: mic pkg parameters [OPTIONS]

  Add a parameter into the MIC file (mic.yaml).

  - You must pass the MIC file (mic.yaml) as an argument using the (-f)
  option; or run the command from the same directory as the MIC file
  (mic.yaml)

  Usage example:

  mic pkg parameters -f <mic_file> --name PARAMETER_NAME --value
  PARAMETER_VALUE

Options:
  -n, --name TEXT                 Name of the parameter  [required]
  -v, --value ANY TYPE (FLOAT, INTEGER, BOOL, STRING)
                                  Default value of the parameter  [required]
  -d, --description TEXT          Description for parameter
  -o, --overwrite                 Overwrite an existing parameter
  -f, --mic_file FILE
  --help                          Show this message and exit.
```
