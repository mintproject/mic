## Overview
The `credentials` command has several options:
```
mic credentials [-p | --profile] [--server] [--username] [--password] [--name] 
                [--email] [--git_username] [--git_token] [--dockerhub_username] 
``` 

## Description

MIC uses several APIs (DockerHub and MINT Model catalog) to upload model components. The MINT Model Catalog requires credentials for adding and modifying contents in the catalog. You can use the `credentials` command to configure a username and password for the [Model Catalog API](https://model-catalog-python-api-client.readthedocs.io/en/latest/endpoints/) and DockerHub. For ease of use, this command can also be used with no parameters, it will prompt the user to enter any required field not given. 

## Options

`-p, --profile <profile-name>`

Credentials can be set up with multiple configuration profiles. This option lets the user choose which profile they are editing. If the profile does not already exist it will generate a new one.
    
`--server <server url> `

The Model Catalog API - [required]

`--username <username>`

Email for the Model Catalog API - [required]

`--password <password>`

Password for Model Catalog - [required]

`--name <name>`

Full name of the author - [required]

`--dockerhub_username <Username>`

Username for dockerhub


## Setting up DockerHub credentials

MIC will prompt you to add your user in [DockerHub](hub.docker.com/), a repository used for publishing Docker images. MIC will help you publish the computational dependencies of your model as a virtual image, giving you full control over the result.

### Example usage:

```
$ mic credentials
Model Catalog API [https://api.models.mint.isi.edu/v1.4.0]:
Username [mint@isi.edu]:
Password:
Name: 
Email:
Docker Username: 
```


!!! info
    [Contact the MINT team](mailto:mint@mailman.isi.edu) to create a new user/password if you want to edit your own models.