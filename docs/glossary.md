
- **Code repository**: Location where the code of a model resides (e.g., GitHub)
- **DAME**: Desktop Application for Model Execution, which we use to execute all the models in the MINT model catalog.
- **MIC file**: A file named mic.yaml that contains the information about your component, inputs, outputs and parameters. This file will tell MIC where to find all the files and executables to run your model.
- **MIC wrapper**: A script used by MIC to invoke your model and configure the inputs and parameters to be used.
- **MINT model catalog**: An online browseable catalog of model components. Accessible at: [https://models.mint.isi.edu/](https://models.mint.isi.edu/)
- **Model component**: A specific invocation function for model software that ensures the inclusion of certain model processes and variables while excluding others. For example, the MODFLOW groundwater model may be configured in many different ways: activating the infiltration package, having snowmelt and wells, exposing a parameter to indicate the recharge rate of an area, etc.
- **Software image**: Computational infrastructure needed to carry out a run of a model.
