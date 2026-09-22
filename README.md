# Benchmarking Data Augmentation Strategies for Drug–Target Interaction Prediction under Class Imbalance

This repository contains the implementation, datasets, intermediate artifacts, audit outputs, and reproducibility material for the manuscript:

**Benchmarking Data Augmentation Strategies for Drug–Target Interaction Prediction under Class Imbalance: A Controlled Comparative Study**

Vitor Magalhães Silva, Khadidja Henni, and Neila Mezghani  
Department of Information Technology, TELUQ University, Montreal, Quebec, Canada  
Imaging and Orthopedics Research Laboratory (LIO), CHUM Research Center, Montreal, Quebec, Canada

## Overview

Drug–target interaction (DTI) prediction is affected by sparse interaction matrices, strong class imbalance, and limited experimentally validated interactions.

This project evaluates data augmentation, resampling, filtering, and generative strategies under a controlled experimental protocol. The benchmark uses the four Yamanishi protein families:

- Enzyme
- G-protein-coupled receptor (GPCR)
- Ion Channel
- Nuclear Receptor

The study compares 14 augmentation, resampling, filtering, and generative methods while controlling the main elements of the prediction pipeline, including data partitioning, latent representation learning, augmentation, DNN training, and out-of-fold evaluation.

## Experimental Design

The benchmark uses fixed stratified five-fold outer cross-validation.

Within each outer-training fold:

1. The outer-training data are divided into fixed 80/20 inner-training and validation subsets.
2. Matrix factorization is fitted using inner-training labels only.
3. Validation and outer-test labels are masked from the factorization loss and are not replaced by zeros.
4. Augmentation, resampling, and filtering are applied only to the inner-training observations.
5. The DNN is trained on the resulting training data.
6. Evaluation is performed on the untouched outer-test fold.
7. Predictions from the five outer-test folds are concatenated to produce one full-family out-of-fold prediction vector.

The complete procedure is repeated for ten stochastic DNN training runs under the same fixed data partitions.

## Latent Representation Learning

Three matrix-factorization backbones are included:

- **MSCMF** — Multiple Similarity Collaborative Matrix Factorization
- **NNMF** — Non-negative Matrix Factorization
- **LMF** — Logistic Matrix Factorization

The latent dimension is fixed at 50 for drugs and 50 for targets. Drug and target embeddings are concatenated to produce a 100-dimensional pair-level representation.

MSCMF incorporates drug and target similarity information through graph-Laplacian regularization. NNMF and LMF provide alternative latent representations under the same train/validation/test masking protocol.

## Augmentation, Resampling, and Filtering

The benchmark includes the following methods:

- Random Over-Sampling
- Random Under-Sampling
- Tomek Links
- CNN + Tomek Links
- SMOTE
- SMOTE + Tomek Links
- Basic SMOTE
- ADASYN
- KMeans-SMOTE
- Latent Sampling
- Noise Injection
- VAE
- WGAN-GP
- Latent Diffusion

Class-distribution configurations are evaluated at:

- 50/50
- 80/20
- 85/15
- 90/10

The first value denotes the proportion of non-interactions and the second the proportion of interactions in the resulting inner-training data.

Classical methods are evaluated with MSCMF representations. WGAN-GP and VAE are additionally evaluated with NNMF and LMF. Latent Diffusion is evaluated with MSCMF.

## Generative Models

### WGAN-GP

Wasserstein GAN with Gradient Penalty is trained only on positive inner-training observations. Positive representations are standardized before training, and generated samples are transformed back to the original feature scale before being added to the training set.

### Variational Autoencoder

The VAE is trained on positive inner-training observations and generates synthetic positive latent representations through sampling from the learned latent distribution.

### Latent Diffusion

Latent Diffusion operates on a compressed representation of the MSCMF pair features. A beta-VAE maps the 100-dimensional pair representation into a lower-dimensional latent space, where the diffusion process is trained and sampled.

## DNN Classifier

A common DNN architecture is used across configurations:

- Input dimension: 100
- Hidden layers: 512, 256, 128
- ReLU activations
- Dropout: 0.1 after the first hidden layer
- Two output units
- Sigmoid activation
- Binary cross-entropy
- Adam optimizer
- 12 training epochs
- No early stopping

Evaluation metrics include:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- PR-AUC

Metrics are calculated from the pooled out-of-fold prediction vector for each stochastic run. Final results are reported as the mean and 95% confidence interval across ten runs.

## Main Findings

The benchmark does not identify a single augmentation method or class ratio that performs best across all four protein families or all evaluation metrics.

Key observations include:

- Classical methods achieve the highest F1-score in each of the four protein families.
- Generative methods remain competitive and lead selected ranking metrics.
- MSCMF + VAE achieves the highest PR-AUC for GPCR.
- Latent Diffusion achieves the highest ROC-AUC for Nuclear Receptor.
- The MSCMF configuration without augmentation remains competitive, particularly for Enzyme and Ion Channel.
- WGAN-GP and VAE performance depends strongly on the latent representation used for sample generation.
- For both WGAN-GP and VAE, MSCMF produces higher F1-scores than NNMF and LMF across the four protein families.
- Augmentation therefore needs to be evaluated jointly with the latent representation, class ratio, and performance metric rather than treated as an independent preprocessing step.

## Important Evaluation Notes

In the Yamanishi interaction matrix:

- `1` denotes a validated interaction.
- `0` denotes an unobserved interaction.

For binary classification, zero-valued entries are treated operationally as non-interactions, but they should not be interpreted as experimentally confirmed negative interactions.

The reported confidence intervals quantify variability across repeated stochastic DNN training runs under fixed data partitions. They do not quantify variability associated with alternative cross-validation partitions.

The reported mean F1-score is calculated independently for each run before averaging and therefore does not necessarily equal the harmonic mean of the reported mean precision and mean recall.

## Repository Structure

The repository is organized around the complete experimental pipeline.

Main notebooks:

- `1 - Raw Data Preparation - Dictionary Version.ipynb`
- `2 - Fixed Stratified 5-Fold Outer Splits - All Families.ipynb`
- `3 - Fixed Inner 80-20 Train-Validation Splits - All Families.ipynb`
- `4 - Matrix Factorization and Leakage Audit - All Families.ipynb`
- `5 - Training-Only Augmentation and Augmentation Audit - All Families - With Diffusion.ipynb`
- `6 - Fixed DNN Training, OOF Evaluation and Results Tables - All Families.ipynb`

Supporting material includes:

- raw and processed Yamanishi data
- fixed outer and inner split manifests
- matrix-factorization audit outputs
- leakage checks
- augmentation protocol and ratio audits
- DNN run-level and fold-level metrics
- final result tables
- reproducibility seeds

See `FOLDER_STRUCTURE.md` for the full repository layout.

## Reproducibility and Leakage Controls

The repository includes explicit audit artifacts for:

- outer cross-validation splits
- inner train/validation splits
- overlap checks
- matrix-factorization inputs
- matrix-factorization masking
- factorization traceability
- leakage prechecks
- augmentation inputs
- augmentation ratios
- reconstructed augmented datasets
- fold-level DNN outputs
- run-level DNN metrics

The purpose of these audit files is to make the train/validation/test separation and training-only augmentation steps directly traceable.

## Previous Work

The MSCMF + WGAN-GP + DNN configuration was introduced in earlier work:

V. M. Silva, K. Henni, Y. Abdelliche, and N. Mezghani,  
**A Matrix Factorization and Generative Modeling Framework for Drug–Target Interaction Prediction**,  
BIOSTEC 2026, pp. 688–695.

DOI: `10.5220/0014484300004070`

In the present study, this framework is retained as a reference configuration within a broader controlled benchmark rather than presented as a universally superior augmentation strategy.

## Data

The study uses the Yamanishi benchmark datasets for the following protein families:

- Enzyme
- GPCR
- Ion Channel
- Nuclear Receptor

The datasets contain binary interaction matrices and drug/target similarity information used by the matrix-factorization stage.

## Contact

Vitor Magalhães Silva  
TELUQ University  
Email: `silva.vitor_magalhaes@univ.teluq.ca`  
GitHub: `@vitormag-gh`

## Citation

If you use this repository or the associated manuscript, please cite:

**Vitor Magalhaes Silva, Khadidja Henni, and Neila Mezghani (2026).  
Benchmarking Data Augmentation Strategies for Drug–Target Interaction Prediction under Class Imbalance: A Controlled Comparative Study.  
Department of Information Technology, TELUQ University, Montreal, Quebec, Canada;  
Imaging and Orthopedics Research Laboratory (LIO), CHUM Research Center, Montreal, Quebec, Canada.**

### BibTeX

```bibtex
@unpublished{silva2026dti,
  title  = {Benchmarking Data Augmentation Strategies for Drug--Target Interaction Prediction under Class Imbalance: A Controlled Comparative Study},
  author = {Silva, Vitor Magalhaes and Henni, Khadidja and Mezghani, Neila},
  year   = {2026},
  note   = {Manuscript submitted to BMC Bioinformatics}
}
```

## License

See the `LICENSE` file in this repository.
