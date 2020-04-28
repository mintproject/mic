Model Insertion CLI (MIC) is a command-line interface for adding model metadata in the [MINT Model Catalog Service](https://models.mint.isi.edu/home).

MIC helps you complete the information of your model, model version, model configuration, parameters, inputs, outputs, authors and contributors (among other key metadata).

MIC has been tested in OSX, Unix and Windows. It can installed through a simple pip command (see below).

!!! info
    MIC is ongoing work. Please report any issue you experience in our [GitHub repository](https://github.com/mintproject/mic/issues/new/choose).

## Requirements

MIC has the following requirements:

1. Python >= 3.6

To install install Python 3, follow the instructions below:

- [Installation on Linux](https://realpython.com/installing-python/#linux)
- [Installation on Windows](https://realpython.com/installing-python/#windows)
- [Installation on Mac](https://realpython.com/installing-python/#macos-mac-os-x)

## Installation

To install MIC, open a terminal and run:

```bash
pip install mic
```

To check if mic was installed correctly, run:
```bash
mic version
```
You should see a message like the following one:
```bash
mic v0.2.0
```
