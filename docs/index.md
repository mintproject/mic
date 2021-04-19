## Introduction

The Model Insertion command-line interface (MIC) is an application to assist scientists in encapsulating their softwares (e.g., models, pre-processing and post-processing codes, visualizations) in a virtual environment to ensure their execution independently of the evolution of the libraries used to support them. In addition, MIC allows scientists to expose a set of inputs and parameters of interest and to describe basic metadata information to ensure maximum reuse.

!!! info
    MIC is an ALPHA version, which we are still testing and developing continuously. If you find an error or experience any issue, please report them [here](https://github.com/mintproject/mic/issues/new/choose).

### What is a software component?

Encapsulating software into components allows other users to easily access and run software on their own machine without worrying about the environment the software needs. Following well-established component-based software engineering principles, we want to create self-contained software components that only reveal functionality that is of interest to third party users. This is important because scientific softwares are often implemented in large packages or libraries that can be used for various steps such as data preparation and visualization in addition to writing software to model specific processes (such as atmospheric dynamics for climate models, runoff and infiltration for hydrology models, fuel density for fire modeling...).

These packages can be quite overwhelming for users, even if they are associated with the scientific domain for which the package has been written. It becomes an impossible tasks for users outside of the domain but who could make use of specific results.

Over the years, scientists have created various user interfaces to conveniently provide access to their software but these interfaces are often not reusable from another program, requiring significant movement of data from one platform to the next. However, the basic framework for these user interfaces involves a specific function to call the software from a button in the interface and a fillable form that sets specific parameters. That call (sometimes called a *command line invocation*) is reusable from one framework to the next, provided that the software itself is containerized in such as way that it can be executed from any local machine in its specific environment.  The call function is known as the *component interface*, and its inputs can be provided when invoking the component (as is done in a user interface where the values for some input parameters are filled out.) Other inputs can be pre-set within the component (including data files) if there are no reasons for third party users to change them given a specific application.

A **software component** corresponds to a single invocation function for software.  From a sophisticated software package, a software component could be created to include only certain processes and variables, a specific pre-processing step, or a specific visualization. For example, a hydrology model software could be pre-set to be working in hot arid region only and ignore the processes (and therefore inputs) describing snowmelt.   

The purpose of MIC is to assist a scientist in creating a model component for various pieces of their workflows, including data preparation and pre-processing, modeling, and visualizations.

MIC is meant to work with the [MINT Model Catalog](https://github.com/mintproject/ModelCatalog). However, the container it creates in the process can be reused outside of this framework.

### Why should you create a software component?

* Everyone will be able to execute your model in their own local environments and operating systems (Linux, MacOS or Windows).
* You can simplify the number of inputs needed for a particular application.
* You will be able to create a secure environment for executing the model. When others want to run your model, they will be reassured that the model will not disrupt or delete anything in their local environment.
* Everyone will be able to find your component in a model catalog supported by the [MINT model catalog ontology](https://github.com/mintproject/Mint-ModelCatalog-Ontology) such as [MINT model catalog](https://models.mint.isi.edu/) using [DAME](dame-cli.readthedocs.io/).  

## Getting Started

* [Installing MIC](installation)
* [Overview of the MIC process](overview)
* [Available commands](usage)
* [Step-by-step instructions](model_configuration/01-overview) for creating a software component
* Report bugs and problems with the code or documentation to our [GitHub repository](https://github.com/mintproject/mic/issues).
* [Frequently asked questions](faq)
