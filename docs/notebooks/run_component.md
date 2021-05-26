## How to perform this step?

### Specifying the inputs in a yaml file.

The `inputs` of a model component is a list of input parameters/files that control its execution. Each input has an `id` for the `name`, and `type` describing
what types of values are valid for that input.

Available primitive types are `string`, `int`, and `null`;
complex types are `array` and; in addition there are special type `File`.

To direct its execution, the inputs must be specified in a `.yml` file.

Using our simple line fitting model, we create a file called `simpleModelAnnotatedValues.yml`, containing the following text, representative of the input file, parameters, and output files in our Notebook:

```yaml
a: 1
b: 20
c: 30
input_file:
  class: File
  path: https://raw.githubusercontent.com/mosoriob/simpleModel-1/master/x.csv
```

Notice that `input_file`, as a File type, must be provided as an object with the fields class: `File` and `path`.

!!! info
    If the input file is hosted on GitHub, remember to copy the sharable download URL.
    [GitHub: how to find the sharable download URL for files on GitHub ](https://help.data.world/hc/en-us/articles/115006300048-GitHub-how-to-find-the-sharable-download-URL-for-files-on-GitHub)

### Run and test your component

!!! warning
    Make sure that [cwltool](https://github.com/common-workflow-language/cwltool#install) is installed on your system before proceeding.

The command line execution looks something like:
```bash
$ cwltool simpleModelAnnotated.cwl simpleModelAnnotatedValues.yml
```

where `simplemodelAnnotated.cwl` was automatically created [in the previous step](/notebooks/convert_repository/) and `simpleModelAnnotatedValues.yml` is the file generated above.

## Expected results

```bash
$ cwltool simpleModelAnnotated.cwl simpleModelAnnotatedValues.yml
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

The output file `y.csv` is generated in this step. 
