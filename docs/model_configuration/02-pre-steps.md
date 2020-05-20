In order to use MIC effectively, your should create a GitHub and DockerHub account. We will use these accounts in MIC to help you publish your component.

!!! warning
    MIC **will not** store your credentials.

## GitHub 

### Create account

GitHub is a website and cloud-based service that helps developers store and manage their code, as well as track and control changes to their code.

`MIC` creates a GitHub repository and push your code.

### Obtain GitHub Token

To push your code, you must generate a GitHub Token.

!!! note
    A documentation

## DockerHub

Docker Hub is a hosted repository service provided by Docker for sharing Docker images
If you don't have a Docker ID, head over to https://hub.docker.com to create one.

`MIC` creates and pushes Docker images for you.

### Login

To push the image, you must login

```bash
docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: frink
Password:
```