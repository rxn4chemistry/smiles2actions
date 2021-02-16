# Action sequence prediction for arbitrary chemical equations

This repository contains the code for [Inferring Experimental Procedures from Text-Based Representations of Chemical Reactions](https://doi.org/10.26434/chemrxiv.13118423).

- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Training transformer](#training-the-transformer-model)
- [Code examples for processing compound names and actions](#examples)
- [Evaluation and notebooks](#evaluation-and-notebooks)

# Overview

This repository contains code for the prediction of action sequences for arbitrary chemical equations. 
In particular, it contains the following:
* Training and usage of a transformer-based model
* Simplification of compound names
* Validation and post-processing of action sequences
* Tokenization of compounds, temperatures, and durations

A trained model is integrated in the IBM RXN platform and can be freely used online at https://rxn.res.ibm.com.


# System Requirements

## Hardware requirements
The code can run on any standard computer.
It is recommended to run the training scripts in a GPU-enabled environment.

## Software requirements
### OS Requirements
This package is supported for *macOS* and *Linux*. The package has been tested on the following systems:
+ macOS: Big Sur (11.1)
+ Linux: Ubuntu 18.04.4

### Python
A Python version of 3.6 or greater is recommended.
The Python package dependencies are listed in [`requirements.txt`](requirements.txt).

# Installation guide

To use the package, we recommend creating a dedicated Conda environment:
```bash
conda create -n smiles2actions python=3.6 -y
conda activate smiles2actions
```

Then, the following command will install the package and its dependencies:
```bash
pip install -e .
```
The installation should not take more than a few minutes.

# Training the transformer model

Instructions for training the transformer model are given [here](./model_training/).


# Examples

Code examples for the processing of compound names and actions are presented in the [examples](./examples/) directory.

## Simplification of compound names

A script illustrating the simplification of compound names is given [here](./examples/name_simplification.py).

Output example:
```
Processing the name "dcm solution of 1:1 water / 30% sulfuric acid"
  Checking the following simplification: dcm solution of 1:1 water / 30% sulfuric acid
  Checking the following simplification: dcm, 1:1 water / 30% sulfuric acid
  Checking the following simplification: dcm, water / sulfuric acid
  Checking the following simplification: dcm, water, sulfuric acid
Simplified name(s): dcm, water, sulfuric acid
Replaced by synonym(s): DCM, water, H2SO4
```

## Action validation

A script illustrating the validation of actions [here](./examples/action_validation.py).
The functionality presented there is necessary to filter out undesired action sequences from the data set.

## Action postprocessing

In [one of the examples](./examples/postprocess_actions.py), we illustrate how actions are postprocessed during the data set generation, with changes such as:
* Harmonize formulation of equivalent actions (`MakeSolution` / `Add`, `Wait`, etc.)
* Tokenization of durations, temperatures, pH values
* Removal of quantities
* etc.

Example output:
```
OLD: MAKESOLUTION with CHCl2 (2 ml) and water (3 ml) ; ADD SLN ; STIR for 3 hours ; PH with acetic acid to pH 9.3 ; YIELD product
NEW: ADD CHCl2 ; ADD water ; STIR for @3@ ; PH with acetic acid to pH basic ; YIELD product
```

## Compound tokenization

The tokenization of the compounds is illustrated in another [script](./examples/tokenize_compounds.py).

Example output:
```
OLD: ADD ethane ; ADD methane ; ADD sodium chloride ; STIR for 8 hours ; QUENCH with brine ; YIELD propane
NEW: ADD $1$ ; ADD $2$ ; ADD $3$ ; STIR for 8 hours ; QUENCH with brine ; YIELD $-1$
```

# Evaluation and notebooks

The IPython notebooks in this repository can be executed with `jupyter lab`.
They assume the relevant data to be present in the directory given as the `S2A_PAPER_DATA_DIR` environment variable.

The notebook [metrics.ipynb](./notebooks/metrics.ipynb) is used to calculate the metrics presented in the paper.

Additional notebooks are included:
* [Reaction class distribution of the data set](./notebooks/class_distribution.ipynb)
* [Difference in class frequencies before and after data set processing](./notebooks/rxn_class_frequency.ipynb)
* [Creating plots for distribution of action lengths and calculating the single-action accuracy](./notebooks/action_length_analysis.ipynb)
* [Performance of the model on different reaction classes](./notebooks/metrics_on_classes.ipynb)

