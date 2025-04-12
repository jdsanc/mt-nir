# MT-NIR: Multi-task UV-vis Near-Infrared Property Prediction

This repository contains code for predicting near-infrared (NIR) and UV-Vis  properties of photoswitches using multitask learning with Chemprop.

## Features

Current prediction capabilties of photochemical properties
  - Maximum absorption wavelength (nm)
  - Extinction coefficient (log(M^-1 cm^-1))
  - Photoisomerization quantum yield

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jdsanc/mt-nir.git
cd mt-nir
```

2. Create and activate a conda environment:
```bash
conda create -n chemprop_v2 python=3.11
conda activate chemprop_v2
```

3. Install dependencies:
```bash
pip install chemprop pandas numpy rdkit
```

## Usage

Model is already trained all you need to do load the model into your terminal. Using script described in Predictions.

### Prediction

You can handle both single SMILES strings and CSV files for bulk prediction:


For a single SMILES:
```bash
python predict.py --smiles "CC(=O)OC1=CC=CC=C1C(=O)O"
```
Ensure you surround your input smiles by quotes ""

For a CSV file:
```bash
python predict.py --csv your_input_file.csv
```
Ensure if using your own .csv file to have the header written as "smiles" verbatum. 

The script will output predictions in terminal for single prediction or in output csv called 'your_input_file_predict.csv' with the following properties:

- max_abs_wavelength (nm)
- extinct_coeff (log(M^-1 cm^-1))
- photoisomerization_QY

