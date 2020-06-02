## Before you start

In order to use MIC, you should create a GitHub and a DockerHub account. We will use these accounts in MIC to help you publish your component. You only need to perform these steps once.


## Create a GitHub account

GitHub is a website and cloud-based service that helps developers store and manage their code, as well as track and control changes to their code. MIC uses GitHub to store a snapshot of your code and invocation by creating a GitHub repository and pushing your local code files. The code is stored in your account, so you will be the owner..

### Obtain your GitHub access token

In order for MIC to push code in your repository, you must generate a GitHub Token. 

This token can be generated on the GitHub website. Once logged, in at the top right dropdown menu there will be a "signed in as **[username]**"

The `GitHub Token` is the user's [personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line). To create a personal access token click [here](https://github.com/settings/tokens/new), or go to GitHub.com -> Settings -> Developer settings -> personal access token. Click **Generate new token** this will open the new personal access token page. The following options must be checked:
 
  - [x] repo: | Full control of private repositories
  - [x] write:packages | Upload packages to github package registry
  - [x] read:packages | Download packages from github package registry
 
 Writing "mic access token" under notes is also recommended
 
 When done click **Generate token** at the bottom of the page. Once the token is generated be sure to copy and save it in a secure location. Enter this key in the `GitHub API token` field when prompted.

!!! warning
    If this token is lost you will have to generate a new one.

## Create a DockerHub account

Docker Hub is a hosted repository service provided by Docker for sharing Docker images
If you don't have a Docker ID, head over to https://hub.docker.com to create one.

`MIC` creates and pushes Docker images for you.

### Login

To push the Docker image, you must login

```bash
docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: frink
Password:
```

### Configure MIC

Type `mic credentials` and fill in the information requested. You only need to do this once.
