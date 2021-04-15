This step will attempt to run your model component using the MIC wrapper and will validate that the expected output files are successfully generated.

## How to perform this step?

Type `mic pkg run`. Below is the result obtained with our simple Java model:

```bash
$ (climate) root@2417929e507e:/tmp/mint# mic pkg run
Found mic.yaml in /tmp/mint/mic/mic.yaml
MIC needs to create new directory mic/executions/04_15_01_50_06 to run the model component Do you want to continue [Y/n]: Y
Create a execution directory /tmp/mint/mic/executions/04_15_01_50_06
Copying the inputs
Source: /tmp/mint/mic/data
Destination: /tmp/mint/mic/executions/04_15_01_50_06/src
Running
./run   -i1 /tmp/mint/mic/executions/04_15_01_50_06/src/GLDAS2.1_TP_2000_2018.nc  -o1 results_mp4.mp4 -o2 results_nc.nc  -p1 2015 -p2 2016
+ pushd .
/tmp/mint/mic/executions/04_15_01_50_06/src /tmp/mint/mic/executions/04_15_01_50_06/src
+ python3 WM_climate_indices.py config.json
2021-04-15  01:51:04 WARNING IMAGEIO FFMPEG_WRITER WARNING: input image is not divisible by macro_block_size=16, resizing from (1500, 1000) to (1504, 1008) to ensure video compatibility with most codecs and players. To prevent resizing, make your input image divisible by the macro_block_size or set the macro_block_size to 1 (risking incompatibility).
[swscaler @ 0x6397a40] Warning: data is not aligned! This can lead to a speed loss
+ popd
/tmp/mint/mic/executions/04_15_01_50_06/src
+ set +x
[success] The model has exited with code SUCCESS
[success] The model has generated the output results/results.mp4
[success] The model has generated the output results/results.nc
Success
You can see the result at /tmp/mint/mic/executions/04_15_01_50_06
The next step is `mic pkg upload`
The step is going to upload the MIC Wrapper to GitHub, the DockerImage on DockerHub and the Model Configuration on the MINT Model Catalog
You model has passed all the tests. Please, review the outputs files.
If the model is ok, type "exit" to go back to your computer
IMPORTANT: type "exit" and then upload your Model Component
```

MIC will ask permission to create a folder, which will be placed under `executions` in the `mic` folder. MIC tested whether the execution of the model component finished successfully and whether the expected outputs (`results.nc` and `results.mp4`) were generated. After inspecting the result in `tmp/mint/mic/executions/04_15_01_50_06` and confirming that the output is correct, we conclude that the component is ready for publication.

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
