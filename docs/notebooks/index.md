# Using a Jupyter Notebook to create a software component

For software written in Python, the MIC process can be simplified by using a Jupyter Notebook prepared to run using Binder.

## Requirements

- [IPython](https://ipython.org/) Jupyter Notebooks:
    - Code your software in the Notebook
    - Use the notebook as a wrapper to call your software (Your model must be Linux compatible). Example of such a notebook can be found in [this GitHub repository](https://github.com/khider/datatransformation_regrid). 

!!! warning
    The entire notebook should be executable without user input.

- Git repository: The notebook should be available in a public GitHub repository.
- Binder-ready repository: Prepare your repository for Binder (requires a requirements.txt or environment.yml file). Please read [Get started with Binder](https://mybinder.readthedocs.io/en/latest/introduction.html#what-is-a-binder).
- A DockerHub account
