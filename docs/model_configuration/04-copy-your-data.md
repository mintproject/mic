## Identify your inputs and copy them

You must copy your inputs into the directory `data`.

!!! warning
    Your code is not an input.

An `input` can be:

- A file in the directory `data` is one input.
- A directory in the directory `data` is one input (MIC is going create a zip file).

Let's suppose that you have copied the following directory and file
- GLDAS_NOAH025_M.2.1/  - This is a directory
- prepicipitation_rates.txt - This is a file


## Identify your parameters

Analysts may want to explore indicators values under different initial conditions. These are expressed as adjustable parameters of models.


Let's suppose that you have identified two parameters:
- start_year: 
- end_year


## Creating `config.yaml` file

Then, you must run the command:

```bash
$ mic encapsulate step2 <model_dir> --inputs_dir data/ --number-parameters 2
or
$ mic encapsulate step2 <model_dir>  --number-parameters 2
```

This command generates `config.yaml` file. This YAML file with the information about your model configuration

```yaml
inputs:
  gldas_noaho25_m.2.1:
      path: data/GLDAS_NOAH025_M.2.1/
 prepicipitation_rates: 
      path: data/prepicipitation_rates.txt
parameters:
  parameter1:
      default_value: 
  parameter2:
      default_value: 
```

You **must** add:

    - A *default_value* for each parameter

You **can** edit 

  - The name of the parameters and inputs (Spaces are not admitted)

### Creating the invocation code

Then, we must generate the MINT wrapper to run your model

You must pass the `MIC_CONFIG_FILE` (`config.yaml`) using the option (`-f`).


```bash
$ mic encapsulate step3 -f config.yaml
The invocation has been created.
```

!!! warning
    If you edit the inputs or the parameters section in the `config.yaml` file, you must re-run ` mic encapsulate step3 -f config.yaml`


In the next step, you are going to learn how to run your models using the MINT Wrapper
