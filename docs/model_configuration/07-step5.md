## Step 5: Expose model inputs

After tracing your execution, MIC has recorded all the input/output files that are needed and produced by your model component. However, we need to identify which of these input types you want to allow others to change. This step will help you describe the input data exposed in your model component. All inputs will be added by MIC in the MIC file.

Note that even though we are referring to concrete files in this step, these represent placeholders that will be expected as input for running your model component. For example, if your model uses a `precip.csv` file with precipitation data and you expose it, your model component will expect a `precip` file as input in order to run; independently of its name.

### How to perform this step?
Just type the following command: `mic encapsulate inputs`. MIC will ask you about whether the inputs and outputs used and produced are code or not, and based on that MIC will add the appropriate inputs into the `mic.yaml` file. For our simple Java example, this is the result of the command execution:

```bash
$ mic encapsulate inputs 
Automatically found mic.yaml in /tmp/mint/mic/mic.yaml
Detecting the data of your model using the information obtained by the `trace` command.
Creating the inputs.
If the data is a directory, MIC is going to compress in a zipfile.
Is /tmp/mint/input.txt an executable script/program? [y/N]: N
Is /tmp/mint/output.txt an executable script/program? [y/N]: N
Is /tmp/mint/test_192-1.0-SNAPSHOT-jar-with-dependencies.jar an executable script/program? [y/N]: Y
Input input.txt is a file
Input input.txt  added
Ignoring the config /tmp/mint/test_192-1.0-SNAPSHOT-jar-with-dependencies.jar as an input.
Success
The inputs of model component are available in the mic directory.
You model component has 1 inputs
The next step is `mic encapsulate outputs`
MIC is going to detect the outputs of your model using the information obtained by the `trace` command.
For more information, you can type.
mic encapsulate outputs --help
```
### Expected results 
If we inspect the `mic.yaml` file, we now see that the inputs and executable files have been correctly annotated:

```yaml
inputs:
  input_txt:
    path: input.txt
    format: txt
code_files:
  test_192-1_0-snapshot-jar-with-dependencies_jar:
    path: test_192-1.0-SNAPSHOT-jar-with-dependencies.jar
    format: jar
```

If you detect that an input is missing, you can always add it through the `inputs` command. For example, by doing `mic encapsulate inputs <path_to_file>`, where <path_to_file> represents the path to an input you would like to expose. Added files must exist, or the program will issue an error.

### Help command

```bash
Usage: mic encapsulate inputs [OPTIONS] [CUSTOM_INPUTS]...

  Describe the inputs of your model using the information obtained by the
  `trace` command. To identify  which inputs have been automatically
  detected, execute `mic encapsulate inputs -f mic/mic.yaml` and then
  inspect the mic.yaml file

  - You must pass the MIC_FILE (mic.yaml) as an argument using the (-f)
  option  or run the command from the same directory as mic.yaml

  - Identify undetected files in or directories in mic.yaml and add them as
  arguments to the `inputs` command

  mic encapsulate inputs -f <mic_file> [undetected files]...

  Usage example:

  mic encapsulate inputs -f mic/mic.yaml input.txt inputs_directory



Options:
  -f, --mic_file FILE
  --help               Show this message and exit.
```
