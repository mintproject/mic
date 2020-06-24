## Step 1: Start up a MIC encapsulation component and MIC file template

This step is going to create a computational environment based in the executables of your working directory and template MIC file template (`mic.yaml`) which will be placed in a  `/mic` directory.  This file (which will be completed in subsequent steps) contains the executable information and metadata  about your model component.

### How to perform this step?

To run this step, you must `cd` to the folder you usually use for executing your component. Please make sure that all the information needed for executing your model exists in this folder (including data, executable scripts, etc.). You don't need to create any special folder structure, just use the same file structure you would normally use to execute your component.

For example, let us consider a simple java model that reads an input file. In order to test it with MIC, we have  prepared a sample input file (input.txt), which we placed in the same folder as my executable:
```bash
$ ls
input.txt  test_192-1.0-SNAPSHOT-jar-with-dependencies.jar
```

Then, in the folder, type:

```bash
$ mic encapsulate start
```
MIC will ask for the component name you want to use, and will show you a message wimilar to this:

```bash
Model component name: test_192
MIC has initialized the component.
[Created] data:      C:\Users\dgarijo\Desktop\192\java_model\mic\data
[Created] docker:    C:\Users\dgarijo\Desktop\192\java_model\mic\docker
[Created] src:       C:\Users\dgarijo\Desktop\192\java_model\mic\src
[Created] mic.yaml:  C:\Users\dgarijo\Desktop\192\java_model\mic\mic.yaml
C:\Users\dgarijo\Desktop\192\java_model\mic\mic.yaml created
You can disable the detection of dependencies using the option --no-dependencies
Dockerfile has been created: C:\Users\dgarijo\Desktop\192\java_model\mic\docker\Dockerfile
Downloading the base image and building your image
Step 1/1 : FROM mintproject/java:8

 ---> 4950fcaa2d0d
Successfully built 4950fcaa2d0d
Successfully tagged test_192:latest

You are in a Linux environment Debian distribution
We detect the following dependencies.

- If you install new dependencies using `apt` or `apt-get`, remember to add them in Dockerfile mic\docker\Dockerfile
- If you install new dependencies using python. Before the step `publish` run

pip freeze > mic/docker/requirements.txt

Please, run your Model Component.
```
As can be seen in the message above, MIC is creating an execution environment from scratch to make sure we capture the minimum set of dependencies needed to execute a model. Since we had a java executable, MIC already selected a Java environment. If we had python files, MIC would have promted us to select which version of Python to start from.

!!! warning
    This command must **NOT** be executed on a folder already tracked by GitHub.


#### Expected Results

After executing the previous command, MIC creates a `mic` directory with three sub-directories and a MIC file (mic.yaml):

- data/: It contains your data (now it will be empty). 
- src/: It contains your code and MIC Wrapper (i.e., the  file that executes your code). In the next step, you are going to specify how to run your model in the command line. MIC will capture all the required information automatically.
- docker/: It contains the required files to create the Docker Image (if everything goes well, you will not have to modify this directory). In later steps, MIC will populate this directory with the files that are needed to capture your computational infrastructure. 

The MIC file will have a few lines at the moment, capturing the dependencies of the current environment:

```yaml
step: 1
name: test_192
docker_image: dgarijo/test_192:20.6.1
framework: 
  - java8
  - mintproject/java:8
  - .jar
```


#### Help command

```bash
Usage: mic encapsulate start [OPTIONS] USER_EXECUTION_DIRECTORY

  Generates mic.yaml and the directories (data/, src/, docker/) for your
  model component. Also initializes a local GitHub repository

  The argument: `model_configuration_name` is the name of your model
  configuration

Options:
  --dependencies / --no-dependencies Enable/Disable tracking dependencies   
                                    (enabled by default)
  --name TEXT     Name of the model component
  --help          Show this message and exit.
```

!!! info
    In the next version of MIC, we will let you start from your own Docker image if required.

