## Login and credentials

The MINT Model Catalog requires credentials for modifying the contents in the catalog. Use this command to configure username and password for the [Model Catalog API](https://model-catalog-python-api-client.readthedocs.io/en/latest/endpoints/).

mic also needs credentials to access GitHub. The GitHub username is the user's username for GitHub. The token is the user's GitHub personal access token. This token can be created under GitHub -> Settings -> Developer settings -> Personal access token. The token needs to have "repo, read and write" permissions. Click [here](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) for more information on personal access tokens. 
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
