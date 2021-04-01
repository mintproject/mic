Similarly to what we did with inputs, we must identify which outputs to expose in our model component. MIC will detect some of them automatically based on what we entered in previous steps, avoiding redundant questions.

For example, for our Java simple model, the command `mic pkg outputs` does most of the work for us:

```bash
$ mic pkg outputs
Automatically found mic.yaml in /tmp/mint/mic/mic.yaml
Detecting the output of your model using the information obtained by the `trace` command.
Output added: /tmp/mint/output.txt
Success
You model component has 1 outputs
The next step is `mic pkg wrapper`
MIC is going to generate the directory structure and commands required to run your model.
For more information, you can type.
mic pkg wrapper --help
```

### Expected results
If we inspect the `mic.yaml` file, we see that the output has been added correctly:

```yaml
outputs:
  output_txt:
    path: output.txt
    format: txt
```

If you detect that an output is missing from the `mic.yaml` file, you can always add it through the `outputs` command. For example, by doing `mic pkg outputs <path_to_file>`, where <path_to_file> represents the path to an output you would like to expose. Added files must exist, or the program will issue an error. MIC will use this information to confirm that the output files are generated when testing the component.

If your code generates intermediate outputs that do not need to be exposed to a user, you can remove them from the `mic.yaml` file. 

### Help command

```bash
Usage: mic pkg outputs [OPTIONS] [CUSTOM_OUTPUTS]...

  Describe the outputs of your model using the information obtained by the
  `trace` command. To identify  which inputs have been automatically
  detected, execute `mic pkg outputs -f mic/mic.yaml` and then
  inspect the mic.yaml file

  - You must pass the MIC_FILE (mic.yaml) as an argument using the (-f)
  option; or run the command from the same directory as mic.yaml

  - Identify undetected files or directories  in the mic.yaml file and pass
  them as as arguments to the command

  mic pkg outputs -f <mic_file> [undetected files]...

  Example:

  mic pkg outputs -f mic/mic.yaml output.txt outputs_directory

Options:
  -f, --mic_file       FILE
  --help               Show this message and exit.
```
