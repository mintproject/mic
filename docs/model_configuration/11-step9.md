Now that we have tested our model component, it's time do a snapshot of the mic wrapper, the docker image and save the model metadata in MINT.

MIC assumes that appropriate GitHub credentials, Docker login and MINT metadata credentials have been set up with the `mic credentials` command.

### How to perform this step?

If you are still on the environment MIC created, type `exit`. It is usually easy to identify whether you are on the MIC environment or not, as you will see `root@<random_number>:/tmp/mint#` in your console. 

Once exited, type `mic pkg upload`:

```bash
$ mic pkg upload
Automatically found mic.yaml in C:\Users\dgarijo\Desktop\192\java_model\mic\mic.yaml
This step uploads your code, DockerImage and ModelConfiguration
Creating the git repository
Compressing your code
Creating a new commit
Creating or using the GitHub repository
The git repository has not a remote server configured
Creating a new repository on GitHub
The url is: https://github.com/dgarijo/test_193.git
Creating a new version
New version: 20.6.1
Pushing your changes to the server
Repository: https://github.com/dgarijo/test_193.git
Version: 20.6.1
Downloading the base image and building your image
Uploading the Docker Image
Docker Image: dgarijo/test_192:20.6.1
```
For the publication in the MINT model catalog, MIC will ask you some questions. See an example below with our sample Java model:

```bash
A model component must be associated with a model
Existing models are:
[1] simplemodel
[2] swat
[3] widoco
[4] test_192
Do you want to use an existing model? [Y/n]: y
Please select the model to use [1]: 4
Existing versions are:
[1] 0.1.0
Do you want to use an existing version? [Y/n]: Y
Select enter the number of version to use [1]: 1
```
In this case, we selected a model that already exists (`test_192`). If the model component does not have a model associated yet, MIC will prompt you to describe its name and version.

### Expected results 
MIC will create a GitHub repository for your component (if the repository exist, it will create a new release in it); a Docker image and a MINT model configuration entry.

For example, for our Java component, MIC automatically created:

- A [GitHub repository](https://github.com/dgarijo/test_192) with a [tagged version](https://github.com/dgarijo/test_192/tree/20.6.1)
- A [Docker image in DockerHub](https://hub.docker.com/repository/docker/dgarijo/test_192)
- The corresponding [model configuration in MINT](https://w3id.org/okn/i/mint/da18b946-a7d5-4df6-b117-1452e47bca0c)

MIC will also tell you how to execute your model in DAME:
```
dame run 50c9168b-da2b-4515-84ad-17d9e144b9d6 -p default
```

You are done. Congratulations!


### Help command

```bash
Usage: mic pkg upload [OPTIONS]

  Upload your MIC wrapper (including all the contents of the /src folder)
  to GitHub, the Docker Image on DockerHub and the model component on MINT
  Model Catalog.

  - You must pass the MIC_FILE (mic.yaml) as an argument using the (-f)
  option or run the command from the same directory as mic.yaml

  mic pkg upload -f <mic_file>

  Example:

  mic pkg upload -f mic/mic.yaml

Options:
  -f, --mic_file FILE
  -p, --profile  <profile-name>
  --help         Show this message and exit.
```