# oratio

Oratio (collect in Latin) is a library meant to provide an easy to use interface for creating a data pipeline for collecting, processing, and saving many types of data.
The core of the library is straightforward. It provides interfaces for a collector, processor, and data handler. Users of the library may choose to use some of our implementations of these interfaces or implements their own. 

# Installation

The library is available as a [conda](https://docs.conda.io/en/latest/) package. To install the package use the following command inside your conda enviorment:

```shell
$ conda install -c capi-bgu -c conda-forge oratio
```

or, if you have `conda-forge` configured as one of your channels you can simply use:

```shell
$ conda install -c capi-bgu oratio
```

# Project Structure

* `doc` - inside the doc folder we have some additional documentation and explanations of how this library works and how it fits inside our project.
* `init.py` - a cmd utility to setup the project for development.
* `conda_env.yml` and `conda_history.yml` - contain the environment used for development of the project.
* `tests` - contains all the tests for the library.
* `oratio` - contains all the sources.

Documentation on how to use this library can be found in the [github wiki](https://github.com/capi-bgu/oratio/wiki)
