

## Clone and build the Docker Image

The command `clone` create the following artifacts for each notebook:

- Docker Image
- A CWL document: CWL is a way to describe command line.

```bash
$ mic notebook clone <repo_url>

...
[Repo2Docker] Successfully tagged r2d-2ftmp-2frepo2cwl-5factynwz1-2frepo1618407245:latest
2021-04-14 09:34:06,916 - repo2cwl - INFO - Generated image id: r2d-2ftmp-2frepo2cwl-5factynwz1-2frepo1618407245
2021-04-14 09:34:06,916 - repo2cwl - INFO - Creating CWL command line tool: index.cwl
2021-04-14 09:34:06,918 - repo2cwl - INFO - Cleaning local temporary directory /tmp/repo2cwl_actynwz1/repo...
```

## Transform 

```bash
$ mic notebook transform index.cwl
```


## Upload 

### Upload the Docker Image

```
$ mic notebook upload-image mic-index.yaml
```

### Upload the component and create the Model Configuration

```bash
$ mic notebook upload-component mic-index.yaml
```