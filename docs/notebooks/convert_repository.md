Use the `mic` to convert the repository. 


!!! info

URL must be the repository url.

```bash
$ mic notebook read <repository_url>
```

The commands performs the following actions:

1. Download the repository.
2. Build a Docker Image reading the Binder configuration files.
3. Convert each IPython Notebook to a command line script.
4. Generate a CWL Document for each notebook. The notebook will be ignored if it does not contain annotations, 


## What is a CWL Document?

CWL is a way to describe command line tools and connect them together to create workflows. Because CWL is a specification and not a specific piece of software, tools and workflows described using CWL are portable across a variety of platforms that support the CWL standard.

### Example


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

Next, you must provide the input values. Create a file `values-example1.yml` 

```yaml
a: 1
b: 20
c: 30
input_file:
  class: File
  path: https://raw.githubusercontent.com/mosoriob/simpleModel-1/master/x.csv
```

Now, you can run the model using `cwltool`

```bash
$ cwltool simpleModelAnnotated.cwl simpleModelAnnotated.cwl 
INFO [job simpleModelAnnotated.cwl] completed success
{
    "output_file": {
        "location": "file:///home/mosorio/tmp/demo/y.csv",
        "basename": "y.csv",
        "class": "File",
        "checksum": "sha1$b70550bfaf3178152371dada56c7aaa826c85127",
        "size": 24950,
        "path": "/home/mosorio/tmp/demo/y.csv"
    }
}
INFO Final process status is success
```


### Possible issues

- Can we select a set of outputs as a collections