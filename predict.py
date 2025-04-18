#!/usr/bin/env python
import argparse
import pandas as pd
import numpy as np
import logging
import os
import subprocess
import tempfile
from typing import List
from rdkit import Chem

logger = logging.getLogger(__name__)

class BasePredictor:
    """
    Base class for all predictors
    
    This class defines the interface for molecule property predictors.
    """
    def __init__(self):
        pass
        
    def predict(self, smiles_list):
        """
        Predict properties for a list of SMILES strings
        
        Args:
            smiles_list (list): List of SMILES strings
            
        Returns:
            list: List of predictions for each SMILES
        """
        return [self.predict_single(s) for s in smiles_list]
        
    def predict_single(self, smiles):
        """
        Predict properties for a single SMILES string
        
        Args:
            smiles (str): SMILES string
            
        Returns:
            list: Property predictions
        """
        raise NotImplementedError("Subclasses must implement predict_single")

class ChempropPredictor(BasePredictor):
    """
    Predictor using Chemprop models via CLI
    
    This implementation calls the chemprop command line tool to make predictions.
    """
    def __init__(self, models_path):
        """
        Initialize predictor
        
        Args:
            models_path (str): Path to model files
        """
        super().__init__()
        
        # Try to check parent directory
        parent_dir = os.path.dirname(models_path)
        if parent_dir:
            logger.info(f"Parent directory: {parent_dir}")
            logger.info(f"Parent exists: {os.path.exists(parent_dir)}")
            if os.path.exists(parent_dir) and os.path.isdir(parent_dir):
                try:
                    contents = os.listdir(parent_dir)
                    logger.info(f"Parent directory contents: {contents}")
                except Exception as e:
                    logger.error(f"Error listing parent directory: {e}")
        
        if not os.path.exists(models_path):
            raise ValueError(f"Model path {models_path} does not exist.")
        self.models_path = models_path
        logger.info(f"Initialized ChempropPredictor with model at {models_path}")
    
    def predict_single(self, smiles: str) -> List[float]:
        """
        Predict properties for a single SMILES string using chemprop CLI.
        
        Args:
            smiles (str): SMILES string
            
        Returns:
            List[float]: List of mean predictions across the ensemble
        """
        logger.debug(f"Predicting properties for: {smiles}")
        try:
            # Create temporary input file with SMILES
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                f.write("smiles\n" + smiles)
                temp_input = f.name
            
            # Create temporary output file
            with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
                temp_output = f.name
            
            # Run chemprop predict
            try:
                logger.debug(f"Running chemprop prediction with model: {self.models_path}")
                cmd = [
                    "chemprop", "predict",
                    "--test-path", temp_input,
                    "--model-paths", self.models_path,
                    "--multi-hot-atom-featurizer-mode", "RIGR",
                    "--devices", "1",
                    "--batch-size", "1",
                    "--preds-path", temp_output
                ]
                result = subprocess.run(cmd, 
                                      check=True, 
                                      capture_output=True, 
                                      text=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Chemprop CLI error: {e}")
                logger.error(f"Stdout: {e.stdout if hasattr(e, 'stdout') else 'N/A'}")
                logger.error(f"Stderr: {e.stderr if hasattr(e, 'stderr') else 'N/A'}")
                raise RuntimeError(f"Chemprop prediction failed: {e}")
            
            # Read predictions
            if not os.path.exists(temp_output) or os.path.getsize(temp_output) == 0:
                logger.error("Chemprop produced empty output file")
                return [float("-inf")] * 3
            
            preds = pd.read_csv(temp_output)
            
            # Skip the SMILES column if it exists
            numeric_cols = preds.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                logger.warning("No numeric predictions found in output")
                return [float("-inf")] * 3
            
            # Get only numeric predictions
            means = preds[numeric_cols].iloc[0].tolist()
            
            # Convert to float and ensure we have 3 values
            means = [float(x) for x in means]
            if len(means) < 3:
                means.extend([float("-inf")] * (3 - len(means)))
            
            logger.info(f"Properties for {smiles[:20]}...: {means}")
            return means
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return [float("-inf")] * 3
            
        finally:
            # Cleanup temp files
            if 'temp_input' in locals():
                try:
                    os.unlink(temp_input)
                except Exception as e:
                    logger.debug(f"Error cleaning up input file: {e}")
            if 'temp_output' in locals():
                try:
                    os.unlink(temp_output)
                except Exception as e:
                    logger.debug(f"Error cleaning up output file: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description='Predict properties using a trained Chemprop model')
    parser.add_argument('--smiles', type=str, help='SMILES string to predict properties for')
    parser.add_argument('--csv', type=str, help='Path to CSV file containing SMILES strings')
    parser.add_argument('--models_path', type=str, 
                       default='./exp_results/03232025_split/checkpoints/chemprop_weights_RIGR_ensemble_03232025/fold_0',
                       help='Path to the trained model checkpoint')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize predictor
    predictor = ChempropPredictor(args.models_path)
    
    if args.smiles:
        # Predict for single SMILES
        preds = predictor.predict_single(args.smiles)
        print("\nPrediction Results:")
        print(f"smiles: {args.smiles}")
        print(f"max_abs_wavelength (nm): {int(round(preds[0], 0))}")
        print(f"extinct_coeff (log(M^-1 cm^-1)): {round(preds[1], 2)}")
        print(f"photoisomerization_QY: {round(preds[2], 2)}")
            
    elif args.csv:
        # Read CSV file
        df = pd.read_csv(args.csv)
        
        # Make predictions
        results = []
        for smiles in df['smiles']:
            preds = predictor.predict_single(smiles)
            results.append({
                'smiles': smiles,
                'max_abs_wavelength(nm)': int(round(preds[0], 0)),
                'extinct_coeff(log(M^-1 cm^-1))': round(preds[1], 2),
                'photoisomerization_QY': round(preds[2], 2)
            })
        
        # Create results dataframe
        results_df = pd.DataFrame(results)
        
        # Save results to CSV
        output_path = os.path.splitext(args.csv)[0] + '_predict.csv'
        results_df.to_csv(output_path, index=False)
        print(f"\nPredictions saved to: {output_path}")
        
    else:
        print("Error: Either --smiles or --csv must be provided")
        return

if __name__ == '__main__':
    main() 