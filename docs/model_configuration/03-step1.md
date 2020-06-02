## Step 1: Set up a MIC directory structure and MIC file template

This step is going to create:
The directory of your model component
Three subdirectories (data/, src/ and docker/) in the model component directory.
A MIC file template (mic.yaml). This file (which will be completed in subsequent steps) contains the executable information and metadata  about your model component.

#### How to perform this step?

To run this step, you must type the following command (where <model_component> is the name of your model component):

```bash
$ mic encapsulate step1 <model_component>
```

For example,

```bash
$ mic encapsulate step1 swat_precipitation_rates
Created: /Users/mosorio/tmp/swat_precipitation_rates/src
Created: /Users/mosorio/tmp/swat_precipitation_rates/docker
Created: /Users/mosorio/tmp/swat_precipitation_rates/data
Created: /Users/mosorio/tmp/swat_precipitation_rates/.gitignore
Searching files in the directory /Users/mosorio/tmp/swat_precipitation_rates
MIC has created the directories
You must add your data (files or directories) into the directory: /Users/mosorio/tmp/swat_precipitation_rates/data
```
!!!warning
    This command must **NOT** be executed on a folder already tracked by GitHub.


#### Expected Results

After executing the previous command, MIC creates three directories and a MIC file (mic.yaml):


data/: It contains your data (now it will be empty). In step 2,  you will have  to copy your data in this directory.
src/: It contains your code and MIC Wrapper (i.e., the  file that executes your code).
In step 3, MIC is going to help you generate the MINT Wrapper
In step 5, you are going to specify how to run your model in the MINT Wrapper (i.e., the series of commands).
docker/: It contains the required files to create the Docker Image (if everything goes well, you will not have to modify this directory). In `step 7`, MIC will populate this directory with the files that are needed to capture your computational infrastructure. 

The MIC file will have a single line at the moment:.

```yaml
step: 1
```


#### Help command

```bash
Usage: mic encapsulate step1 [OPTIONS] MODEL_COMPONENT_NAME

This step is going to create:
The required directories 
And the MIC file. The MIC file contains the metadata about your model component.

  mic encapsulate step1 <model_component_name>

  The argument: `model_component_name` is the name of your model
  component

Options:
  --help  Show this message and exit.

```
