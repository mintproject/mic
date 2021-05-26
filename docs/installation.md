# Installation

MIC has been tested on Mac, Linux, and Windows Platforms

## Requirements

1. Python >= 3.6
2. Docker

If using MIC with a Jupyter Notebook, the following Python package is also needed:
3. [cwltool](https://github.com/common-workflow-language/cwltool#install)

### Getting Python 3

To install Python:

- [Installation on Linux](https://realpython.com/installing-python/#linux)
- [Installation on Windows](https://realpython.com/installing-python/#windows)
- [Installation on Mac](https://realpython.com/installing-python/#macos-mac-os-x)

You can also complete the installation using alternative distribution such as [Anaconda](https://www.anaconda.com), a popular platform for scientists. If you plan on using Anaconda, we recommend that you set up MIC in a new environment.

```bash
$ conda create --name myenv
$ conda activate myenv
```

Detailed instructions are available [here](/creating_new_env).

### Docker

- [Installation on Linux](https://docs.docker.com/engine/install/)
- [Installation on MacOS](https://docs.docker.com/docker-for-mac/install/)

## Limitations

Note that MIC has been designed to run Unix-based applications. Windows based applications (e.g., models that execute through an .exe) are not currently supported.

## Installing MIC

MIC install through `pip`. No Anaconda distribution currently available.

```bash
$ pip install mic
```

To check your installation:

```bash
$ mic version
mic v1.3.7
```

### Development version

If you want to install the latest development version, open a terminal and type:

```bash
$ pip install git+https://github.com/mintproject/mic.git@develop -U
```
Note that the development version may be unstable.

## Code Releases and Next Updates

The [latest release of MIC is available from GitHub](https://github.com/mintproject/mic/releases/latest). You can also check current development from our [GitHub milestones](https://github.com/mintproject/mic/milestones).
