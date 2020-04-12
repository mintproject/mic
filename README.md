# Model Insertion CLI (MIC) 

Model Insertion CLI (MIC) is a command-line interface for addming  models on a Model Catalog Service.

MIC is an application that ask the information of your model, model version, model configuration, parameters, inputs, outputs, authors and contribuors.

MIC has been tested in OSX and Windows (currently under test in Linux). Mic is installed through a simple pip command:

`pip install mic`

Please report any issue with us [here](https://github.com/mintproject/mic/issues/new/choose).

## Features

- [x] Add model and th related resources: Author, Contributors, Model Version, Model Configuration, Parameters, Inputs and Outputs.
- [x] Save the resource as a file
- [x] Send the resource to the Model Catalog Server (you must have an account)

# Usage

## Add a new model

To add a model, you must run:

```bash
mic model add
```

Full documentation available at: [https://mic-cli.readthedocs.io/en/latest/](https://mic-cli.readthedocs.io/en/latest/)
