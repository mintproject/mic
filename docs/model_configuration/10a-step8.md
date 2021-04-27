!!! warning
    DO NOT CLOSE the terminal in-between each step.  
    After inspecting the `mic.yml` file in-between steps, CLOSE the file.

This step will attempt to run your model component using the MIC wrapper and will validate that the expected output files are successfully generated.

## How to perform this step?

Type `mic pkg run`. Below is the result obtained with our simple Java model:

```bash
MIC needs to create new directory mic/executions/06_25_04_47_52 to run the model component Do you want to continue [Y/n]: Y
Create a execution directory /tmp/mint/mic/executions/06_25_04_47_52
Copying the inputs
Source: /tmp/mint/mic/data
Destination: /tmp/mint/mic/executions/06_25_04_47_52/src
Running
./run   -i1 /tmp/mint/mic/executions/06_25_04_47_52/src/input.txt  -o1 output_txt.txt  -p1 1350
+ pushd .
/tmp/mint/mic/executions/06_25_04_47_52/src /tmp/mint/mic/executions/06_25_04_47_52/src
+ java -jar test_192-1.0-SNAPSHOT-jar-with-dependencies.jar -i input.txt -p 1500 -o output.txt
Done
+ popd
/tmp/mint/mic/executions/06_25_04_47_52/src
+ set +x
[success] The model has exited with code SUCCESS
[success] The model has generated the output output.txt
Success
You can see the result at /tmp/mint/mic/executions/06_25_04_47_52
The next step is `mic pkg upload`
The step is going to upload the MIC Wrapper to GitHub, the DockerImage on DockerHub and the Model Configuration on the MINT Model Catalog
You model has passed all the tests. Please, review the outputs files.
If the model is ok, type "exit" to go back to your computer
IMPORTANT: type "exit" and then upload your Model Component
```

MIC will ask permission to create a folder, which will be placed under `executions` in the `mic` folder. MIC tested whether the execution of the model component finished successfully and whether the expected output (`output.txt`) was generated. After inspecting the result in `tmp/mint/mic/executions/06_25_04_47_52` and confirming that the output is correct, we conclude that the component is ready for publication.

## Expected result
A successful test of the candidate model component. **After you are done,  type `exit` to exit the MIC container and return to your desktop for the final step**.

## Help command
```bash
Usage: mic pkg run [OPTIONS]

  This step will test the model component you created in previous steps.

  - You must pass the MIC_FILE (mic.yaml) using the option (-f) or run the
  command from the same directory as mic.yaml

  mic pkg run -f <mic_file>

  Example:

  mic pkg wrapper -f mic/mic.yaml

Options:
  -f, --mic_file FILE
  --help               Show this message and exit.
```
