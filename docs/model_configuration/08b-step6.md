!!! warning
    DO NOT CLOSE the terminal in-between each step.  
    After inspecting the `mic.yml` file in-between steps, CLOSE the file.

Similarly to what we did with inputs, we must identify which outputs to expose in our model component. MIC will detect some of them automatically based on what we entered in previous steps, avoiding redundant questions.

## How to perform this step?

```bash
$ mic pkg outputs
```
For our Python example:

```bash
$ (climate) root@d8826beb2c59:/tmp/mint# mic pkg outputs
Found mic.yaml in /tmp/mint/mic/mic.yaml
Detecting the output of your model using the information obtained by the `trace` command.
Output added: spi_t15.jpeg
Output added: spi_t8.jpeg
Output added: spi_t18.jpeg
Output added: spi_t9.jpeg
Output added: spi_t21.jpeg
Output added: spi_t0.jpeg
Output added: spi_t10.jpeg
Output added: results.nc
Output added: results.mp4
Output added: spi_t4.jpeg
Output added: spi_t11.jpeg
Output added: spi_t13.jpeg
Output added: spi_t22.jpeg
Output added: spi_t7.jpeg
Output added: spi_t5.jpeg
Output added: spi_t19.jpeg
Output added: spi_t17.jpeg
Output added: spi_t1.jpeg
Output added: spi_t6.jpeg
Output added: spi_t14.jpeg
Output added: spi_t3.jpeg
Output added: spi_t12.jpeg
Output added: spi_t23.jpeg
Output added: spi_t16.jpeg
Output added: spi_t20.jpeg
Output added: spi_t2.jpeg
Success
You model component has 26 outputs
The next step is `mic pkg wrapper`
MIC is going to generate the directory structure and commands required to run your model.
For more information, you can type.
mic pkg wrapper --help
```

## Expected results
Outputs should be identified as followed in `mic.yaml`:

```yaml
outputs:
  results_nc:
    path: results/results.nc
    format: nc
  results_mp4:
    path: results/results.mp4
    format: mp4
```

If you detect that an output is missing from the `mic.yaml` file, you can always add it through the `outputs` command. For example, by doing `mic pkg outputs <path_to_file>`, where <path_to_file> represents the path to an output you would like to expose. Added files must exist, or the program will issue an error. MIC will use this information to confirm that the output files are generated when testing the component.

If your code generates intermediate outputs that do not need to be exposed to a user, you can remove them from the `mic.yaml` file. This is the case in our Python example where intermediate `jpeg` files are generated to produce the final `mp4` movie.

## Help command

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
