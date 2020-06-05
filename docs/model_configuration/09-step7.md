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
