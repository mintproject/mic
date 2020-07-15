# Available commands
Run the following command in your terminal to know more about the features in mic:

```bash
mic --help
```

You should see a message such as the following one:
```bash
Usage: mic [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose
  --help         Show this message and exit.

Commands:
  credentials       Configure credentials
  encapsulate       Command to encapsulate a model component
  list-credentials  List credentials profiles
  model             Command to create new model metadata
  version           Show mic version
```
The `credentials` command allows setting up the necessary credentials to be able to modify the catalog.

The `encapsulate` command will walk you through 9 steps allowing you to encapsulate your model component so it can be run in any infrastructure.

The `list-credentials` command will allow you to see details about all credential profiles you have added.

The `model` command allows adding a new [model](https://mintproject.readthedocs.io/en/latest/modelcatalog/#making-your-model-findable) with accompanying metadata. 

The `version` command displays the installed mic version.
