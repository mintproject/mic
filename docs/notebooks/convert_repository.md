This steps require the use of the `mic` package installed on your local machine. If you haven't already done so, [install `mic`](/installation).

## How to perform this step?

```bash
$ mic notebook read <repository_url>
```

!!! info
    URL must be the repository url, not the direct link to the notebook.

For instance,

```bash
$ mic notebook read https://github.com/<your_user_name>/simpleModel-1
[Repo2Docker] Successfully tagged r2d-2ftmp-2frepo2cwl-5f60lguuht-2frepo1618948318:latest

repo2cwl - INFO - Generated image id: r2d-2ftmp-2frepo2cwl-5f60lguuht-2frepo1618948318
repo2cwl - INFO - Creating CWL command line tool: simpleModelAnnotated-List-Input.cwl
repo2cwl - INFO - Creating CWL command line tool: simpleModelAnnotated.cwl
repo2cwl - INFO - Creating CWL command line tool: simpleModelAnnotated-Output-Wildcard.cwl
repo2cwl - INFO - Cleaning local temporary directory /tmp/repo2cwl_60lguuht/repo...
repo2cwl - INFO - cloning repo to temp directory: /tmp/repo2cwl_60lguuht/repo2021-04-20 15:51:57,957 - repo2cwl - INFO - Notebook /tmp/repo2cwl_60lguuht/repo/simpleModel.ipynb does not contains typing annotations. skipping...

...

[Repo2Docker] Successfully tagged r2d-2ftmp-2frepo2cwl-5f60lguuht-2frepo1618948318:latest

repo2cwl - INFO - Generated image id: r2d-2ftmp-2frepo2cwl-5f60lguuht-2frepo1618948318
repo2cwl - INFO - Creating CWL command line tool: simpleModelAnnotated-List-Input.cwl
repo2cwl - INFO - Creating CWL command line tool: simpleModelAnnotated.cwl
repo2cwl - INFO - Creating CWL command line tool: simpleModelAnnotated-Output-Wildcard.cwl
repo2cwl - INFO - Cleaning local temporary directory /tmp/repo2cwl_60lguuht/repo...

```

The commands performs the following actions for each annotated notebook in the repository:

1. Download the repository.
2. Build a Docker Image reading the Binder configuration files.
3. Convert each IPython Notebook to a command line script.
4. Generate a CWL Document for each notebook.

!!! warning
    The notebook will be ignored if it does not contain annotations.

!!! info
    If the repository contains more than one notebook, a separate model component will be created for each notebook.   

!!! info
    CWL is a way to describe model components (using command line tools)
    Because CWL is a specification and not a specific piece of software, tools and workflows described using CWL are portable across a variety of platforms that support the CWL standard.

## Expected outputs

In our example, the command generates four CWL Document.
Let's check the file `simpleModelAnnoted.cwl` and the important section for you.

```yaml
arguments:
- --
baseCommand: /app/cwl/bin/simpleModelAnnotated
class: CommandLineTool
cwlVersion: v1.1
hints:
  DockerRequirement:
    dockerImageId: r2d-2ftmp-2frepo2cwl-5fq3aa8np7-2frepo1618495110
inputs:
  a:
    inputBinding:
      prefix: --a
    type: int
  b:
    inputBinding:
      prefix: --b
    type: int
  c:
    inputBinding:
      prefix: --c
    type: int
  input_file:
    inputBinding:
      prefix: --input_file
    type: File
outputs:
  output_file:
    outputBinding:
      glob: ./y.csv
    type: File

```

- DockerRequirement: Indicates that a model component should be run in a Docker container, and specifies how to fetch the image.
- inputs: Defines the input parameters of the model component. The component is ready to run when all required input parameters are associated with concrete values.
- outputs: Defines the parameters representing the output of the process. May be used to generate and/or validate the output object.
