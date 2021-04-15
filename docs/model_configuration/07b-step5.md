!!! warning
    DO NOT CLOSE the terminal in-between each step.  
    After inspecting the `mic.yml` file in-between steps, CLOSE the file.

After tracing your execution, MIC has recorded all the input/output files that are needed and produced by your model component. However, we need to identify which of these input types you want to allow others to change. This step will help you describe the input data exposed in your model component. All inputs will be added by MIC in the MIC file.

Note that even though we are referring to concrete files in this step, these represent placeholders that will be expected as inputs for running your model component. Our example uses `GLDAS2.1_TP_2000_2018.nc` file with precipitation and temperature data. To expose it, your model component will expect a `input_nc` file as input in order to run; independently of its name.

## How to perform this step?

First you need to modify your configuration file in a similar fashion as you did for the parameters for MIC to replace its values in the file. In this particular example, we replaced the `GLDAS2.1_TP_2000_2018.nc` value with `${input_nc}` as shown below:

```json
{
"data" :
  {
  "dataset_name" : "${input_nc}",
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
Then type the following command: `mic pkg inputs`. MIC will ask you about whether the inputs and outputs used and produced are code, and based on that MIC will add the appropriate inputs into the `mic.yaml` file.

```bash
$ mic pkg inputs
```

For our example:

```bash
$ (climate) root@d8826beb2c59:/tmp/mint# mic pkg inputs
Found mic.yaml in /tmp/mint/mic/mic.yaml
Detecting the data of your model using the information obtained by the `trace` command.
Creating the inputs.
If the data is a directory, MIC is going to compress in a zipfile.
.py
Adding WM_climate_indices.py as executable
Input results added
Input GLDAS2.1_TP_2000_2018.nc added
Input figures added
Success
The inputs of model component are available in the mic directory.
You model component has 3 inputs
The next step is `mic pkg outputs`
MIC is going to detect the outputs of your model using the information obtained by the `trace` command.
For more information, you can type.
mic pkg outputs --help
```


## Expected results

Note that in this case, MIC incorrectly detected the output folders as inputs. We needed to delete them from the `mic.yml` file and replace the name of the netcdf file with `input_nc`:

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
inputs:
  input_nc:
    path: GLDAS2.1_TP_2000_2018.nc
    format: nc
code_files:
  wm_climate_indices_py:
    path: WM_climate_indices.py
    format: py
```

If you detect that an input is missing, you can always add it through the `inputs` command. For example, by doing `mic pkg inputs <path_to_file>`, where <path_to_file> represents the path to an input you would like to expose. Added files must exist, or the program will issue an error.

## Help command

```bash
Usage: mic pkg inputs [OPTIONS] [CUSTOM_INPUTS]...

  Describe the inputs of your model using the information obtained by the
  `trace` command. To identify  which inputs have been automatically
  detected, execute `mic pkg inputs -f mic/mic.yaml` and then
  inspect the mic.yaml file

  - You must pass the MIC_FILE (mic.yaml) as an argument using the (-f)
  option  or run the command from the same directory as mic.yaml

  - Identify undetected files in or directories in mic.yaml and add them as
  arguments to the `inputs` command

  mic pkg inputs -f <mic_file> [undetected files]...

  Usage example:

  mic pkg inputs -f mic/mic.yaml input.txt inputs_directory



Options:
  -f, --mic_file FILE
  --help               Show this message and exit.
```
