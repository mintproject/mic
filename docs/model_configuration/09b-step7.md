!!! warning
    DO NOT CLOSE the terminal in-between each step.  
    After inspecting the `mic.yml` file in-between steps, CLOSE the file.

The MINT Wrapper is a plain text file that contains a series of commands needed for executing a model.
The MINT Wrapper does the following tasks:

- Copy and extract your inputs in the src directory
- Feed the parameter values to your software.
- Detect errors on execution time.

The commands in the MINT Wrapper are a mixture of commands we would normally type ourselves on the command line (such as ls or cp). If this sequence of commands is needed to execute your model, we need to preserve it in your model component. Remember that anything you can run normally on the command line can be put into a script with equivalent functionality.

!!! info
    Many models have graphical interfaces for data preparation purposes and set up. However, the scope of this effort is making your software available on any infrastructure. Cloud servers and supercomputers don’t usually provide graphical interfaces, and therefore we cannot assume a graphical interface to be available. It is a good engineering practice to deliver a component that can be used without a graphical interface.

## How to perform this step?
Just type `mic pkg wrapper` and MIC will attempt to generate the wrapper script automatically. For example, in our Python software:

```bash
$ (climate) root@2417929e507e:/tmp/mint# mic pkg wrapper

```
## Expected results
If MIC has successfully created the wrapper and drafted an executable automatically, you should see the following:

1. The data has been moved to the data folder
2. The configuration file should have been moved as well
2. `output.sh`, `input.sh` and `run` have been created.

Next, you should ensure that the executable is correct. From our example, the executable at `/tmp/mint/mic/src/run` looks like follows:

```bash
#!/bin/bash
set +x
set -e
. .colors.sh

BASEDIR=$PWD
. $BASEDIR/io.sh 1 2 2 "$@"
CURDIR=`pwd`
## INPUTS VARIABLES
input_nc=${INPUTS1}


## PARAMETERS VARIABLES
sim_start_year=${PARAMS1}
sim_end_year=${PARAMS2}


set -xe

####### WRITE YOUR INVOCATION LINE AFTER THIS COMMENT


pushd .
python3 WM_climate_indices.py config.json
popd

set +x
echo -e "$(c G)[success] The model has exited with code SUCCESS"
####### WRITE YOUR INVOCATION LINE BEFORE THIS COMMENT
cd $BASEDIR
. $BASEDIR/output.sh
```
Make sure that the input files/parameters names correspond to the one you have assigned in the configuration file and that the invocation command is correct. Since you have already matched the names of the input files and parameters in step 4, you do not need to make further modification at this point.

## Help command
```bash
Usage: mic pkg wrapper [OPTIONS]

  Generates the MIC Wrapper:a directory structure and commands required to
  run your model component using the information gathered from previous
  steps

    - You must pass the MIC_FILE (mic.yaml) as an argument using the (-f)
    option or run the   command from the same directory as mic.yaml

    mic pkg wrapper -f <mic_file>

    Example:

    mic pkg wrapper -f mic/mic.yaml

Options:
  -f, --mic_file FILE
  --help               Show this message and exit.
```
