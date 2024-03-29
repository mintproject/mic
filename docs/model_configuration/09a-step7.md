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
Just type `mic pkg wrapper` and MIC will attempt to generate the wrapper script automatically. For example, in our simple Java model:

```bash
$ mic pkg wrapper
Automatically found mic.yaml in /tmp/mint/mic/mic.yaml
Generating the MIC Wrapper. This generates the directory structure and commands required to run your model
{'p': {'default_value': 1350, 'type': 'int', 'description': ''}}
Copying the code: test_192-1.0-SNAPSHOT-jar-with-dependencies.jar to the MIC Wrapper directory mic/src
Success
The wrapper has been generated. You can see it at /tmp/mint/mic/src/run
The next step is `mic pkg run`
The command run is going to create a new directory (execution directory), and MIC is going the inputs, code, and configuration files and run the model.
For more information, you can type.
mic pkg run --help
```
## Expected results
If MIC has successfully created the wrapper and drafted an executable automatically, you should see the following:

1. The data has been moved to the data folder
2. `output.sh`, `input.sh` and `run` have been created.

Next, you should ensure that the executable is correct. Otherwise you need to update the command line execution to reflect the parameters. From our example, the executable at `/tmp/mint/mic/src/run` looks like follows:

```bash
#!/bin/bash
set +x
set -e
. .colors.sh

BASEDIR=$PWD
. $BASEDIR/io.sh 1 1 1 "$@"
CURDIR=`pwd`
## INPUTS VARIABLES
input_txt=${INPUTS1}


## PARAMETERS VARIABLES
p=${PARAMS1}


set -xe

####### WRITE YOUR INVOCATION LINE AFTER THIS COMMENT


pushd .
java -jar test_192-1.0-SNAPSHOT-jar-with-dependencies.jar -i input.txt -p 1500 -o output.txt
popd

set +x
echo -e "$(c G)[success] The model has exited with code SUCCESS"
####### WRITE YOUR INVOCATION LINE BEFORE THIS COMMENT
cd $BASEDIR
```

We see that MIC prepared already the command to run our component based on our trace, however, it failed to use the placehoder parameters we described in the `mic.yaml` file. We should update the invocation command:

```
java -jar test_192-1.0-SNAPSHOT-jar-with-dependencies.jar -i input.txt -p 1500 -o output.txt
```
to be
```
java -jar test_192-1.0-SNAPSHOT-jar-with-dependencies.jar -i ${input_txt} -p ${p} -o output.txt
```
which reflects what we had in our mic.yaml file:

```yaml
parameters:
  p:
    default_value: 1350
    type: int
    description: ''
inputs:
  input_txt:
    path: input.txt
    format: txt
```

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
