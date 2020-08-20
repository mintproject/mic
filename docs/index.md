Model Insertion CLI (MIC) is a command-line interface for adding  models on a Model Catalog Service.

MIC is an application that will guide you through the steps required for encapsulating your model component and exposing a set of inputs and parameters of interest. MIC also allows describing basic model metadata: model version, model configuration, parameters, inputs, outputs, authors and contribuors.

MIC has been tested in OSX, Linux and Windows. It is installed through a simple pip command. 

!!! info
    MIC is an ALPHA version, which we are still testing and developing continuously. If you find an error or experience any issue, please report them [here](https://github.com/mintproject/mic/issues/new/choose).

## Requirements

MIC has the following requirements:

1. Python >= 3.6
2. Docker


### Python 3

DAME uses Python. Please, follow the steps bellow to install it:

- [Installation on Linux](https://realpython.com/installing-python/#linux)
- [Installation on Windows](https://realpython.com/installing-python/#windows)
- [Installation on Mac](https://realpython.com/installing-python/#macos-mac-os-x)

### Docker

MIC uses Docker test and run model components.

- [Installation on Linux](https://docs.docker.com/engine/install/)
- [Installation on MacOS](https://docs.docker.com/docker-for-mac/install/)


## Installation

To install MIC, open a terminal and run:

```bash
$ pip install mic
```

You did it! If you want to verify the installation just type:

```bash
$ mic version
```

You should see a message similar to:

```bash
mic v1.0.1
```

## Limitations

Note that MIC has been designed to run Unix-based applications. Windows based applications (e.g., models that execute through an .exe) are not currently supported.

## Development version

If you want to install the latest development version, open a terminal and type:

```bash
$ pip install git+https://github.com/mintproject/mic.git@develop -U
```
Note theat the development version may be unstable.