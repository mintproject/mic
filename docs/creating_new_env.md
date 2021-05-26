# How to create and use Conda/Python environments?

## What Is a Virtual Environment?

At its core, the main purpose of Python virtual environments is to create an isolated environment for Python projects. This means that each project can have its own dependencies, regardless of what dependencies every other project has.


## Conda environments

1. To create an environment

```bash
conda create --name myenv
```

!!! info 
    Replace myenv with the environment name or directory path.


2. Activate environment

```bash
    $ conda activate myenv
```

For a detail tutorial, go to [Managing environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

## Python Virtual Environments

Start by making a new directory to work with:

```bash
$ mkdir ~/python-virtual-environments && cd python-virtual-environments
```

Create a new virtual environment inside the directory:

```bash
# Python 3
$ python3 -m venv env
```

In order to use this environment’s packages/resources in isolation, you need to *activate* it. To do this, just run the following:

```bash
$ source env/bin/activate
(env) $
```

Notice how your prompt is now prefixed with the name of your environment (env, in our case). This is the indicator that env is currently active, which means the python executable will only use this environment’s packages and settings.

For a detail tutorial, go to [Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/)