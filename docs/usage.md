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
  configure           Configure your credentials to access the Model
                      Catalog...

  model               Command to create and edit Models
  modelconfiguration  Command to create and edit ModelConfigurations
  version             Show mic version.
```
The `configure` command allows setting up the credentials to be able to modify the catalog.

The `model` and `modelConfiguration` commands allow adding a new [model](https://mintproject.readthedocs.io/en/latest/modelcatalog/#making-your-model-findable) or [model configuration](https://mintproject.readthedocs.io/en/latest/modelcatalog/#model-configuration) metadata. 

The `version` command lists the current version of mic.
