## Specify the Input parameters

The `inputs` of a model component is a list of input parameters that control how to run it. 
Each parameter has an `id` for the `name` of parameter, and `type` describing 
what types of values are valid for that parameter.

Available primitive types are `string`, `int`, and `null`; 
complex types are `array` and; in addition there are special type `File`.

The following example demonstrates some input parameters with different types 
and appearing on the command line in different ways.

Create a file called simpleModelAnnotatedValues.yml, containing the following boxed text

```yaml
a: 1
b: 20
c: 30
input_file:
  class: File
  path: https://raw.githubusercontent.com/mosoriob/simpleModel-1/master/x.csv
```

Notice that `input_file`, as a File type, must be provided as an object with the fields
class: `File` and `path`.

!!! info
    If the input file is hosted on GitHub, remember to copy the sharable download URL. 
    [GitHub: how to find the sharable download URL for files on GitHub ](https://help.data.world/hc/en-us/articles/115006300048-GitHub-how-to-find-the-sharable-download-URL-for-files-on-GitHub)

## Run and test your component

Use the command `run` to run and test your component

```bash
$ mic notebook test simpleModelAnnotated.cwl simpleModelAnnotatedValues.cwl 
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

The command returns the output files