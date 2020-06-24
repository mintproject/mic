

### Step 3.2: Generate the MINT Wrapper.

The MINT Wrapper is a plain text file that contains a series of commands needed for executing a model.
The MINT Wrapper does the following tasks:
Copy and extract your inputs in the src directory
Feed the parameter values to your models.
Detect errors on execution time.

The commands in the MINT Wrapper are a mixture of commands we would normally type ourselves on the command line (such as ls or cp). If this sequence of commands is needed to execute your model, we need to preserve it in your model component. Remember that anything you can run normally on the command line can be put into a script with equivalent functionality. 
!!! info
    Many models have graphical interfaces for data preparation purposes and set up. However, the scope of this effort is making your model available on any infrastructure. Cloud servers and supercomputers don’t usually provide graphical interfaces, and therefore we cannot assume a graphical interface to be available. It is a good engineering practice to deliver a component that can be used without a graphical interface.

### How to perform this step?

```
mic encapsulate step3 [OPTIONS]
Options:
  -f, --mic_file FILE      a path to the MIC file 
  --help                      Show this message and exit.
```

For example, in SWAT, we run the command using the MIC configure file:

```bash
$ mic encapsulate step3 -f swat_precipitation_rates/config.yaml
```



### Expected results

If everything runs correctly, MIC will create:
MINT Wrapper: available in src/run
Two internal files (io.sh and output.sh) that you must not modify. These files are auxiliary for MIC.

![Diagram](figures/03_02.png)

The MINT Wrapper matches each input and parameter to a variable. 

![Diagram](figures/03_03.png)

This is useful because now you can modify the parameters of your model configuration. In the next step we will cover how to feed parameters to a model in the case where the model uses custom configuration files.







Now that you have finished testing your component, it is time to version appropriately and register it, so it can be reused by others. By typing `mic encapsulate step7` you will be shown the steps followed by MIC to publish your component.

### How to perform this step?

```bash
mic encapsulate step7 --help 
Usage: mic encapsulate step7 [OPTIONS]

Publish your code and MIC wrapper on GitHub and the Docker Image on DockerHub

  mic encapsulate step7 -f <mic_config_file> [outputs]...

Options:
  -f, --mic_config_file FILE
  -p, --profile <profile-name>
  --help                        Show this message and exit.

```

For example, in our SWAT model component we type:
```
mic encapsulate step7  -f mic.yaml
```

And the following will be shown in your terminal:
```    
Publishing your code and MIC wrapper on GitHub and the Docker Image on DockerHub

Deleting the executions
Creating the git repository
Compressing your code
Creating a new commit
Creating or using the GitHub repository
Creating a new version
Previous version 20.5.27
New version: 20.5.28
Pushing your changes to the server
Repository: https://github.com/sirspock/swat_simulation.git
Version: 20.5.28
Publishing the Docker Image
```

As listed above, MIC compresses and submits your code to GitHub in a new repository that will have the same name you gave to your model component. Then, MIC will create a new version of your component, based on the date the component was issued (if you do some edits and execute this step again, a new version will be created on the same repository). In the example above, a previous version of the component existed (`20.5.27`); and a new one with the name `20.5.28` will be created. 

Next, your docker image will be published in DockerHub, assigning a version name as well. Note that MIC does not preserve the execution data, as here we are focusing on the model component. Therefore, the data sources in `data` will not be uploaded to GitHub. 

### Expected results 
Now you should be able to see your component in GitHub; and your Docker image in Dockerhub. Only submitting the component to the MINT model catalog remains!
