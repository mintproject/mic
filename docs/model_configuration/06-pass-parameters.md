# Passing the parameter to your model

Analysts may want to explore indicators values under different initial conditions. These are expressed as adjustable parameters and input variables of models.

We identified two ways to pass the parameters to your model. To explain this, we are going to use example `config.yaml`


In this case, we have two basic parameters:

- start_date
- end_date

```yaml
...
parameters:
    - name: start_date
      default_value: 2010
    - name: edit_date
      default_value: 2012
```


## Arguments 

Some models read the parameters from the command line. For example, the invocation line for cycles is:

```bash
python3 cycles-wrapper.py --start-year 2010 --end-year 2012
```

Then, you must replace the value by the variable in the invocation line
```bash
python3 cycles-wrapper.py --start-year ${start_date} --end-year ${end_date}
```

## Configuration file

Some models read the parameters from a configuration file.

For example, the `SWAT+` model has the following invocation line.

```bash
swatplus
```

SWAT uses configuration files to pass the parameters. To manipulate the simulation dates, SWAT has a file named `time.sim`

```
 DAY_START YRC_START DAY_END YRC_END  STEP
         0      2001       0    2003     0
```

Then, we must open the file and replace the values with variables
```bash
 DAY_START YRC_START DAY_END YRC_END  STEP
         0      {{ start_date }}       0   {{ end_date }}     0
```

And add the file as configuration file of the model.

```bash
mic model_configuration config <path_1> <path_n>
```

In the example, we must run
```
mic model_configuration config `src/time.sim`
```

And the `config.yaml` has been updated

```
```yaml
inputs:
    - name: gldas_noaho25_m.2.1
      path: data/GLDAS_NOAH025_M.2.1/
    - name:  
      path: data/prepicipitation_rates.txt
parameters:
    - name: start_date
      default_value: 2010
    - name: end_date
      default_value: 2012
config_files
    - src/time.sim
```

!!! warning
    If you edit the inputs or the parameters section in the `config.yaml` file, you must re-run `mic model_configuration init config.yaml`

!!! info
    We are using a standard template language JINJA