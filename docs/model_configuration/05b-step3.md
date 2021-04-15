!!! warning
    DO NOT CLOSE the terminal in-between each step.  
    After inspecting the `mic.yml` file in-between steps, CLOSE the file.

Models may use many parameters and input files, but we may not need to expose all of them as part of our component. The goal of this step is to only expose some parameters.

## How to perform this step?

Our Python executable takes the parameters value from its `config.json` file as shown below.

```json
{
"data" :
  {
  "dataset_name" : "GLDAS2.1_TP_2000_2018.nc",
  "dataset_type" : "GLDAS"
},
"output" :
  {
  "dynamic_name" : "False",
  "path" : "./",
  "fig" : "True"
},
"index" :
  {
  "name" : "SPI",
  "distribution" : "gamma",
  "periodicity" : "monthly",
  "scales" : "6",
  "data_start_year" : "2015",
  "data_end_year" : "2016",
  "calibration_start_year" : "2000",
  "calibration_end_year" : "2010"
},
"spatial" :
  {
  "global" : "False",
  "bounding_box": "[23,48,3,15]"
},
"debug" : "False"
}
```

In this particular example, we only want to expose the `data_end_year` and `data_start_year` parameters, which corresponds to the end and start year of the simulation respectively

```bash
$ (climate) root@d8826beb2c59:/tmp/mint# mic pkg parameters -n sim_start_year -v 2015
Found mic.yaml in /tmp/mint/mic/mic.yaml
Adding the parameter sim_start_year, value 2015 and type int
```

The `-n` flag stands for `parameter name` and the `-v` flag stands for the default value you would like the parameter to have. In the case above, we defined a parameter `sim_start_year` with value `2015`. MIC detected that it was an integer.

To add the second paramter, type:

```bash
$ (climate) root@d8826beb2c59:/tmp/mint# mic pkg parameters -n sim_end_year -v 2016
Found mic.yaml in /tmp/mint/mic/mic.yaml
Adding the parameter sim_end_year, value 2016 and type int
```

!!! warning
    Parameters are case sensitive: a parameter `sim_start_year` is different from `SIM_START_YEAR`.

## Expected result

If you open the `mic.yaml` file, you should see that the parameter has been added. We **encourage** adding a description so the role of the parameter becomes clear:

```yaml
parameters:
  sim_start_year:
    name: sim_start_year
    default_value: 2015
    type: int
    description: 'Start year for the simulation'
  sim_end_year:
    name: sim_end_year
    default_value: 2016
    type: int
    description: 'End year for the simulation'
```

You can also add the parameter yourself to the `mic.yaml` file directly following the structure above, if you prefer.

## Help command

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
