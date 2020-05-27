
## Overview
```
mic configure [-p | --profile] [--server] [--username] [--password] [--name] 
              [--email] [--git_username] [--git_token] [--dockerhub_username] 
``` 

## Description

mic uses several APIs to upload models. The MINT Model Catalog requires credentials for modifying the contents in the catalog. Use this command to configure username and password for the [Model Catalog API](https://model-catalog-python-api-client.readthedocs.io/en/latest/endpoints/). This command can also be used with no parameters, it will prompt the user to enter any required field not given. 

## Options

`-p, --profile <profile-name>`

Credentials can be set up with multiple configuration profiles. This option lets the user choose which profile they are editing. If the profile does not already exist it will generate a new one
    
`--server <server url> `

The Model Catalog API - [required]

`--username <username>`

Email for the Model Catalog API - [required]

`--password <password>`

Password for Model Catalog - [required]

`--name <name>`

Full name of the author - [required]

`--git_username <GitHub Username>`

Author's Github username - [required]

`--git_token <GitHub API Token>`

Authors's GitHub API Token. More information can be found in the [setting up GitHub credentials](#GitHubCreds) section below - [required]

`--dockerhub_username <Username>`

Username for dockerhub


## <a name="GitHubCreds">Setting up GitHub credentials</a>

GitHub credentials are also required for mic's GitHub features 
 
The `GitHub Username` field is the users GitHub username. If unknown the username can be found at [GitHub.com](https://github.com/). Once logged, in at the top right dropdown menu there will be a "signed in as **[username]**"

The `GitHub Token` is the user's [personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line). To create a personal access token click [here](https://github.com/settings/tokens/new), or go to GitHub.com -> Settings -> Developer settings -> personal access token. Click **Generate new token** this will open the new personal access token page. The following options must be checked:
  
  - [x] repo: | Full control of private repositories
  - [x] write:packages | Upload packages to github package registry
  - [x] read:packages | Download packages from github package registry
 
 Writing "mic access token" under notes is also recommended 
 
 When done click **Generate token** at the bottom of the page. Once the token is generated be sure to copy and save it in a secure location. Enter this key in the `GitHub API token` field when prompted. 

!!! warning
    If this token is lost there is no way to recover it without generating a new one.

### Setting up DockerHub credentials

### Example usage:

```
$ mic configure
Model Catalog API [https://api.models.mint.isi.edu/v1.4.0]:
Username [mint@isi.edu]:
Password:
Name: 
Email:
GitHub Username:
GitHub API token:
Docker Username: 
```



!!! info
    [Contact the MINT team](mailto:mint@mailman.isi.edu) to create a new user/password if you want to edit your own models.