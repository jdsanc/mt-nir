# MT-NIR: Multi-task Photochemical Property Prediction Model (uvvis-nir range)

This repository contains code for predicting near-infrared (NIR) and UV-Vis  properties of photoswitches using multitask learning with Chemprop.

## Features

Current prediction capabilties of photochemical properties
  - Maximum absorption wavelength (nm)
  - Extinction coefficient (log(M^-1 cm^-1))
  - Photoisomerization quantum yield

## Citation

If you use this software in your research, please cite it using the following:

```bibtex
@software{mt-nir,
  author = {Jesus Diaz Sanchez},
  title = {MT-NIR: Multi-task Photochemical Property Prediction Model},
  year = {2024},
  url = {https://github.com/jdsanc/mt-nir},
  version = {1.0.0}
}
```

You can also use the CITATION.cff file in the repository for citation information.

## Installation

### 1. Install Miniconda3

First, install Miniconda3 if you haven't already:

#### macOS:
You can install Miniconda using Homebrew (recommended) or download directly:

##### Option 1: Using Homebrew
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Miniconda
brew install --cask miniconda
```

##### Option 2: Direct Download
```bash
# Download Miniconda
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh

# Install Miniconda
bash Miniconda3-latest-MacOSX-x86_64.sh
```

#### Linux:
```bash
# Download Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install Miniconda
bash Miniconda3-latest-Linux-x86_64.sh
```

For Linux users, you might need to install wget first:
```bash
# Ubuntu/Debian
sudo apt-get install wget

# CentOS/RHEL
sudo yum install wget

# Fedora
sudo dnf install wget
```

Follow the prompts during installation. After installation, restart your terminal or run:
```bash
source ~/.bashrc  # Linux
source ~/.zshrc   # macOS
```

For more detailed Linux commands and troubleshooting, refer to the [Linux Command Line Guide](https://www.guru99.com/linux-commands-cheat-sheet.html).

### 2. Clone the Repository
```bash
git clone https://github.com/jdsanc/mt-nir.git
cd mt-nir
```

### 3. Create Conda Environment

You can create the environment in two ways:

#### Option 1: Using environment.yml (Recommended)
```bash
conda env create -f environment.yml
```

#### Option 2: Manual Installation
```bash
conda create -n chemprop_v2 python=3.11
conda activate chemprop_v2
pip install chemprop pandas numpy rdkit
```

### 4. Activate the Environment
```bash
conda activate chemprop_v2
```

## Usage

Model is already trained all you need to do load the model into your terminal. Using script described in Predictions.

### Prediction

You can handle both single SMILES strings and CSV files for bulk prediction:

For a single SMILES:
```bash
python predict.py --smiles "C1=CC=C(C=C1)N=NC2=CC=CC=C2"
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

