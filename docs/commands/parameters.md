## Overview
```
mic encapsulate parameters [-n | --name] [-v | --value] [-d | --description] 
                           [-o | --overwrite] [-f | --mic_file] [--help] 
``` 

## Description

The parameters command has two main uses. If parameters is used without any options mic will automatically log any parameters found in the trace command to the mic yaml file. These parameters will later be used to generate the wrapper for use in the model catalog. 

Giving an option (such as `--name`) will manually add a new parameter into the mic file. This is useful if a parameter is not automatically detected in the trace command.

!!! note
    when manually adding a parameter the `name` and `value` must be given.
## Options

`-n, --name <name>` - [Optional]

Used when manually adding a parameter. Assigns a name the that parameter. If `name` is used a value must also be given 

`-v, --value <value>` - [Optional]

Used when manually adding a parameter. Assigns a value the that parameter. If `value` is used a name must also be given 

`-d, --description <description>` - [Optional]

Optional when adding a new parameter. Assigns a description the that parameter in case the parameter name is not self explanitory. If `description` is used a name and value must also be given.

`-o, --overwrite` - [Optional]

Flag used to overwrite an existing parameter. Useful for editing an incorrect description, name or default value

`-f, --mic_file <file>` - [Optional]

Used to declare an explicit path to the mic file. If none is given mic will automatically detect the file. 

`--help`

Show help message for this command - [Optional]


## Example usage:

Default usage: automatically detecting parameters from trace command
```
$ mic encapsulate parameters
Found mic.yaml in /home/users/test/mic/mic.yaml
Automatically adding any parameters from trace
Adding "param_1" from value 35
The parameters of the model component are available in the mic directory.
```

Manually adding a new parameter
```
$ mic encapsulate parameters --name "new_param" --value 101 --description "My parameters description"
Found mic.yaml in /home/users/test/mic/mic.yaml
Adding the parameter new_param, value 101 and type int
```

Overwriting that parameter with a new value and description 
```
$ mic encapsulate parameters --name "new_param" --value 11 --description "Overwritten parameter with new value and description" --overwrite
Found mic.yaml in /home/users/test/mic/mic.yaml
Adding the parameter new_param, value 11 and type int
```

