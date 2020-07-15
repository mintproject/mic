## Overview
The `executables` command has a few different uses:
```
mic encapsulate executables <CUSTOM_EXECUTABLES> [-f | --mic_file] 
                           [-s | --show] [-r | --remove] [--help]
``` 

!!! note
    The `show` and `remove` options are mutually exclusive and cannot be used together

## Description

the executables command is designed to allow for easy adding and removing executable files from mic. This command abstracts the need to manually interface with mic's yaml file as well as automatically adding detected executable files into the yaml.
## Options

`<CUSTOM_EXECUTABLES>` - [Optional]

Path of code files to add manually. Multiple paths can be entered at once, just separate by a space

`-f, --mic_file <path-to-yaml>` - [Optional]

Declare an explicit path to the mic file. Mic will automatically detect the file if one is not given

`-s, --show` - [Optional]

List the path to any file mic has logged as an executable. Providing <CUSTOM_EXECUTABLE(S)> with this command will output if those files are already listed as executables in mic

`-r, --remove` - [Optional]

This option will remove the given executables from the mic file

`--help` - [Optional]

Show the help message for this command

## Example usage:


1). No inputs given
```
$ mic encapsulate executables
Automatically found mic.yaml in /home/user/Desktop/tests/mic/mic.yaml
Detecting executable files using information obtained by the `trace` command.
Creating the code files.
Adding addtoarray.sh as executable
Success
The executables of model component are available in the mic directory.
1 executable files detected
The next step is `mic encapsulate inputs`
For more information, you can type.
mic encapsulate inputs --help
```


2). Manually adding two files as executables
```
$ mic encapsulate executables a.jar tmp/sdsd.exe 
Automatically found mic.yaml in /home/user/Desktop/tests/mic/mic.yaml
Detecting executable files using information obtained by the `trace` command.
Creating the code files.
Adding addtoarray.sh as executable
Adding a.jar as executable
Adding sdsd.exe as executable
Success
The executables of model component are available in the mic directory.
3 executable files detected
The next step is `mic encapsulate inputs`
For more information, you can type.
mic encapsulate inputs --help
```


3). Showing which files mic has logged as executables. (based on last example)
```
$ mic encapsulate executables --show
Automatically found mic.yaml in /home/chris/Desktop/tests/mic/mic.yaml
Executable files:
  * addtoarray.sh
  * a.jar
  * tmp/sdsd.exe
```

4). Removing two executables from mic. (based on last example)
```
$ mic encapsulate executables a.jar tmp/sdsd.exe --remove
Automatically found mic.yaml in /home/user/Desktop/tests/mic/mic.yaml
removing a.jar from mic.yaml
removing tmp/sdsd.exe from mic.yaml
Done
```
