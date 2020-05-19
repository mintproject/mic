## Login and credentials

The MINT Model Catalog requires credentials for modifying the contents in the catalog. Use this command to configure username and password for the [Model Catalog API](https://model-catalog-python-api-client.readthedocs.io/en/latest/endpoints/).


### Setting up GitHub credentials

GitHub credentials are also required for mic's GitHub features 
 
The `GitHub Username` field is the users GitHub username. If unknown the username can be found at [GitHub.com](https://github.com/). Once logged, in at the top right dropdown menu there will be a "signed in as **username**"

The `GitHub Token` is the user's GitHub [personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line). To create a personal access token go to Settings -> Developer settings -> personal access token. Click **Generate new token** this will open the new personal access token page. The following options must be checked:
 - [x] repo: | Full control of private repositories
- [x] write:packages | Upload packages to github package registry
- [x] read:packages | Download packages from github package registry
 
 Writing "mic access token" under notes is also recommended 
 
### Example usage:
```
$ mic configure
Model Catalog API [https://api.models.mint.isi.edu/v1.4.0]:
Username [mint@isi.edu]:
Password:
GitHub Username:
GitHub API token:
```



!!! info
    [Contact the MINT team](mailto:mint@mailman.isi.edu) to create a new user/password if you want to edit your own models.
