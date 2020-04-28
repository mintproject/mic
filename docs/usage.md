# Usage

## Available commands
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


## Login and credentials

The MINT model catalog requires credentials for modifying the contents in the catalog. Use this command to configure username and password for the Model Catalog API.

```
mic configure
```
!!! info
    [Contact the MINT team](mailto:mint@mailman.isi.edu) to create a new user/password if you want to edit your own models.

## Add a new model or model configuration

To show the available commands for modes, type: 
```bash
mic model --help
```
And you will see the following:
```bash
Usage: mic model [OPTIONS] COMMAND [ARGS]...

  Command to create and edit Models

Options:
  --help  Show this message and exit.

Commands:
  add   Add a model
  load  Load a model from file
```
The `add` command guides you through adding new model metadata.

The `load` command allows you loading an existing json file with the model metadata.

To add a model, you must run:

```bash
mic model add
```

You will be shown a table to fill such as:

```bash
======= Model ======
The actual values are:
+-------+----------------+---------+
|   no. | Property       | Value   |
+=======+================+=========+
|     1 | Name           |         |
+-------+----------------+---------+
|     2 | Description    |         |
+-------+----------------+---------+
|     3 | Keywords       |         |
+-------+----------------+---------+
|     4 | Website        |         |
+-------+----------------+---------+
|     5 | Documentation  |         |
+-------+----------------+---------+
|     6 | Versions       |         |
+-------+----------------+---------+
|     7 | Author         |         |
+-------+----------------+---------+
|     8 | Contributor    |         |
+-------+----------------+---------+
|     9 | Contact person |         |
+-------+----------------+---------+
|    10 | License        |         |
+-------+----------------+---------+
|    11 | Category       |         |
+-------+----------------+---------+
|    12 | Creation date  |         |
+-------+----------------+---------+
|    13 | Assumptions    |         |
+-------+----------------+---------+
|    14 | Download URL   |         |
+-------+----------------+---------+
|    15 | Logo           |         |
+-------+----------------+---------+
|    16 | Purpose        |         |
+-------+----------------+---------+
|    17 | Citation       |         |
+-------+----------------+---------+
Select the property to edit [1-17] or ['show', 'save', 'send', 'exit'] [1]:
```

Next, select the property you wish to complete. For example `name`. 
By typing the number of the property (in this case, 1), you will see:

```bash
No value for Name
Definition: Name of the model
Model - Name : Model for Flood analysis
```
We added as name" `Model for Flood analysis`. When pressing enter, the table will be completed:

```bash
======= Model ======
The actual values are:
+-------+----------------+------------------------------+
|   no. | Property       | Value                        |
+=======+================+==============================+
|     1 | Name           | ['Model for Flood analysis'] |
+-------+----------------+------------------------------+
|     2 | Description    |                              |
+-------+----------------+------------------------------+
<Rest of the table ommitted for simplicity>
```
Once you are done, you just have to type `send` and the model will be sent you will be prompted with a message to save your model description, and a URL which you can use to browse if the metadata was correctly posted to the model catalog. The message should look similar to:

```bash
Select the property to edit [1-17] or ['show', 'save', 'send', 'exit'] [1]: send
Success
Enter the file name to save (without extension): : MySavedModel
File saved successfully
Success
See the model/config/setup on your browser? [y/N]: y
Online URI for model/configuration/setup: 
    https://w3id.org/okn/i/mint/<modelID>
Success
```
Where `<modelID>` is the ID provided by the API to the target model.


