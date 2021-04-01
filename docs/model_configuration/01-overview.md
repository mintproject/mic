# Creating a Model Component

The `pkg` command  in MIC guides you through nine steps to create a model component that encapsulates your model code and makes it available in MINT so others can easily run it in their own local environments.  To accomplish this, MIC relies on state-of-the-art virtualization tools (including Docker), software engineering best practices, and semantic reasoning for validation.

There are several reasons for creating a model component:

* You will be able to expose only the inputs and parameters that are more important for a particular use of the model, pre-setting the rest and making them internal to the model component and inaccessible to other users.
* You will be able to create a secure environment for executing the model. When others want to run your model, they will be reassured that the model will not disrupt or delete anything in their local environment.
* Everyone will be able to find your component in a model catalog supported by the [MINT model catalog ontology](https://github.com/mintproject/Mint-ModelCatalog-Ontology) such as [MINT model catalog](https://models.mint.isi.edu/) using [DAME](dame-cli.readthedocs.io/).  
* Everyone will be able to execute your model in their own local environments and operating systems (Linux, MacOS or Windows).

##  What is a Model Component

In preparation for creating a model component, you should consider what set of processes you would like to represent and what variables should be preset vs the ones you would want other users to vary.

## Prepare your executable

1. Place your model code in a local directory so it can be invoked from a command line along with any input data and configuration files needed. MIC will test that the code can be executed and will do so three times during the encapsulation process. Therefore, we recommend that your execution can be completed in a manner of minutes, for example, by reducing the size of the dataset (e.g., only considering a few months instead of a year). Because of limitation on GitHub which will be used during the process, files should not exceed **100 MB** each.
2.  The code should not contain any hardcoded paths or values for the input files/variables that you wish to expose. We recommend making them explicit in a configuration file or as parameters from the command line execution.  

## Before you start

Before you start, you should have a GitHub and Docker account setup following [these guidelines](02-pre-steps.md).

## Overview of the MIC process

MIC has an `pkg` command that will guide you through those steps in the form of nine subcommands. Each subcommand represents one of the nine steps to encapsulate your model. The steps should be followed in order, and after each step you will have a chance to check what MIC is doing to help you create your model component.  

MIC creates: 1) a MIC Directory, 2) a MIC File, 3) a MIC Wrapper, 4) a component virtualization image, 5) archival versions of your model code, MIC directories and files, and image in GitHub and DockerHub, and 6) a model component entry in the MINT Model Catalog.

Below is a summary of the steps, please click on each page for detailed instructions and troubleshooting.

!!! warning
DO NOT CLOSE the terminal in-between each step.
After inspecting the `.yml` file in-between steps, CLOSE the file. 

### Step 1: Start a MIC encapsulation component
Select a working directory (i.e., the directory where you have your input datasets and model executables) and start a new execution environment to run your model. MIC will create a template *MIC file* that will be modified in subsequent steps with information about the model component. The execution environment is created from scratch based on the files in your working directory. For example, if you have python executables, MIC will prepare a python Docker image to execute your model.

**Expected outcomes of this step**: A folder (`mic`) with  a placeholder MIC file that shows up as `mic.yaml` file in that folder.

### Step 2: Trace your model execution
Install any missing dependency needed to execute your model and trace the execution of your model.

**Expected outcome of this step**: You will see that your model took a little longer to run and that a .reprozip trace file was successfully added to your folder.

### Step 3: Select parameters to expose
Specify the input parameters that you would like users to provide for your model component.  This information will be added to the MIC file.

**Expected outcome of this step**: The MIC file will be automatically edited to include information about the input parameters that you specified for your model component.

### Step 4: Pre-populate the model configuration files
You will edit your model configuration files to include any new parameters that you specified as component inputs. In this step MIC will guide you to edit these configuration files so those parameters are appropriately set.

**Expected results after completing this step**: MIC will update the MIC file with pointers to the model configuration files that set the parameters that are input to your component.

### Step 5: Specify inputs to expose
MIC detects automatically most of the inputs your component used for execution. However, we need to determine which of these inputs do you actually want to expose in your model component.  This information will be added to the MIC file.

**Expected outcome of this step**: The MIC file will be automatically edited to include information about the input datasets that you specified for your model component.

### Step 6: Specify outputs to expose
MIC detects automatically most of the outputs your component produced after its execution. However, we need to determine which of these outputs do you actually want to expose in your model component.  This information will be added to the MIC file.

**Expected outcome of this step**: The MIC file will be automatically edited to include information about the output datasets that you specified for your model component.

### Step 7: Prepare MIC wrapper
Create three subfolders (`data`, `src` and `docker`) in the mic folder and *MIC wrapper* that indicates how the component invocation from Step 2 corresponds to the functions implemented in your model software.

**Expected outcome of this step**: The MIC Wrapper will automatically set up three files (run, io.sh, and output.sh) that capture how the component has been run. They can be found in the /src folder of the MIC directory.

### Step 8: Run your model through the MIC wrapper
Use the wrapper generated in Step 7 to execute your model.

**Expected outcome of this step**: A successful test run of your model.  If the tests are successful, the encapsulation of your model component has been successful.

### Step 9: Upload the model component software and image
MIC will upload the MIC Wrapper and your model software in GitHub.  MIC will also upload the model component image in DockerHub and upload your model in the MINT model catalog, which will make it accessible by others through MINT services and interfaces to be run in their own local hosts and servers. This will give them unique identifiers that represent the snapshot of the model that you wanted to encapsulate so that any future updates to your model or your model component can be distinct from each other.

**Expected results after completing this step**: Your model component wrapper will be uploaded to Github, and your model component image to DockerHub. Both will receive a tag and will be versioned, and will be archived so they are available to anyone anywhere.  MINT will have an entry for your model component in the MINT Model Catalog, which will be accessible through your browser.  Anyone using DAME can run your component with their own data.  Anyone using MINT can run your component with any dataset in MINT.


## Using MIC to Create Model Components

Once you have MIC installed, you can type `mic pkg --help` to see the following message that lists all the steps:

```bash
Usage: mic pkg [OPTIONS] COMMAND [ARGS]...

  Command to pkg your model component

Options:
  --help  Show this message and exit.

Commands:
  start       Create a Linux environment to run your model. The working
              directory selected must contain all the files required for the
              execution of your model

  trace       Trace any command line and extract the information about your
              model execution

  parameters  Expose parameters in the mic.yaml file
  configs     Select configuration file(s) for your model (if applicable)
  inputs      Expose model inputs into the mic.yaml file
  outputs     Expose model outputs in the mic.yaml file
  wrapper     Generate the directory structure and commands required to run
              your model component using the information from the previous
              steps

  run         Run your model component with the MIC Wrapper generated in the
              previous step

  upload     Upload your code to GitHub, DockerHub and your
              model component on the MINT Model Catalog.
```

You have to follow the commands in order to successfully upload your component. If you want to know more about a specific step, just do `mic pkg <stepName> --help`, where `<stepName>` represents one of the steps listed above (e.g., `trace`).
