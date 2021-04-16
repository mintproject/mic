!!! warning
    DO NOT CLOSE the terminal in-between each step.  
    After inspecting the `mic.yml` file in-between steps, CLOSE the file.

## Preparing your configuration file

The MINT wrapper can replace the values of the parameters in their right configuration files, but it needs to know where they are. Therefore, we need to define **placeholders** in the configuration files stating which value will be replaced.

In the previous step, we defined two parameters that a user may change, which corresponds to the start and end of the simulation and named them `sim_start_year` and `sim_end_year` and we assigned them default values. Now we need to indicate to MIC where these parameters are located in the configuration file.

Let's open `config.json`:

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

and replace:

- the value `2015` with  ${sim_start_year}
- the value `2016` with ${sim_end_year}

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
  "data_start_year" : "${sim_start_year}",
  "data_end_year" : "${sim_end_year}",
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

Make sure that the names of the parameters match with the names we described in step2! Otherwise MIC will not be able to replace the values accordingly:

![Diagram](figures/config_comp.png)


## How to perform this step?

Once the mapping has been completed, we just need to add the file as a configuration file of the model component:

```bash
mic pkg configs [configuration_files]...
```

In the example, we must run
```
$ (climate) root@d8826beb2c59:/tmp/mint# mic pkg configs config.json
Found mic.yaml in /tmp/mint/mic/mic.yaml
Added: /tmp/mint/config.json as a configuration file
```

!!! info
    The `-a` option will automatically recognize any parameter under `${parameter_name}` in the configuration files and add it to the mic.yaml file automatically. This way you can change them directly without having to perform the mapping yourself in step 3.

## Expected results

The `mic.yaml` will have been updated with a new field named `configs`:

```yaml
parameters:
  sim_start_year:
    name: sim_start_year
    default_value: 2015
    type: int
    description: Start year for the simulation
  sim_end_year:
    name: sim_end_year
    default_value: 2016
    type: int
    description: End year for the simulation
configs:
  config_json:
    path: config.json
    format: json
```

## Help command

```bash
Usage: mic pkg configs [OPTIONS] CONFIGURATION_FILES...

  Note: If your model does not use configuration files, you can skip this
  step

  Specify which parameters of your model component you want to expose from
  any configuration file.

  - You must pass the MIC_FILE (mic.yaml) as an argument using the (-f)
  option or run the command from the same directory as mic.yaml

  - Pass your model configuration files as arguments

  mic pkg configs -f <mic_file> [configuration_files]...

  If you have manually changed some parameters, the -a option will attempt
  to recognize the configuration files automatically

  Example:

  mic pkg configs -f mic.yaml data/example_dir/file1.txt
  data/file2.txt

Options:
  -f, --mic_file FILE
  -a, --auto_param     Enable automatic detection of parameters
  --help               Show this message and exit.
```
