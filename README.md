# DTI_Article_Bioinformatics_2026
BIOINFORMATICS is part of BIOSTEC, the 19th International Joint Conference on Biomedical Engineering Systems and Technologies.

# A Matrix Factorization and Generative Modeling Framework for Drug–Target Interaction Prediction

This repository contains the full implementation, datasets, and reproducibility material for the paper:

**“A Matrix Factorization and Generative Modeling Framework for Drug–Target Interaction Prediction” (2026)**  
Vitor Magalhães Silva  
Université TÉLUQ — Bioinformatics and AI in Drug Discovery

---

## 🔍 Overview

Drug–target interaction (DTI) prediction plays a central role in computational drug discovery by prioritizing compounds for experimental validation.  
This project introduces an **integrated three-stage framework** that combines:

1. **Matrix Factorization (MSCMF, NNMF, LMF)** for latent representation learning  
2. **Generative Modeling (VAE, WGAN-GP)** for minority-class augmentation  
3. **Deep Neural Networks (DNN)** for final interaction prediction  

The method addresses major challenges in DTI prediction, including **data sparsity**, **class imbalance**, and **heterogeneous molecular representations**.

---

## 🧬 Methodology

<p align="center">
  <img src="assets/figures/New_Architecture_2.png" alt="Pipeline Diagram" width="700">
</p>

### 1. **Latent Representation Learning**
We compute drug and protein latent features using:
- **MSCMF** (Multiple Similarity Collaborative Matrix Factorization)  
- **NNMF** (Non-Negative Matrix Factorization)  
- **LMF** (Logistic Matrix Factorization)

MSCMF integrates structural and sequence similarity matrices to create a biologically meaningful latent space.

<p align="center">
  <img src="assets/figures/MSCMF.png" alt="MSCMF Diagram" width="700">
</p>

---

### 2. **Generative Augmentation**

We train two types of generators to augment minority-class interactions:

#### ⭐ **Variational Autoencoder (VAE)**  
- Smooth latent reconstructions  
- Performs best on enzyme and GPCR families  

#### ⭐ **Wasserstein GAN with Gradient Penalty (WGAN-GP)**  
- Most effective in sparse regimes  
- Enhances recall for ion channels and nuclear receptors  

Augmentation is applied **only on the training split**, ensuring no leakage into validation or test sets.

---

### 3. **Deep Neural Network (DNN) Classifier**

The final classifier receives both real and synthetic samples.  
It is a lightweight architecture with:

- Latent feature concatenation  
- Dense layers with dropout  
- Sigmoid output for binary prediction  

All evaluation metrics (accuracy, precision, recall, F1, ROC-AUC, PR-AUC) are reported for each of the four Yamanishi families.

---

## 📊 Results Summary

Our framework consistently outperforms existing baseline methods (SPCA, Random Forests) across all ligand families.  
Key findings:

- **WGAN-GP** improves recall in sparse families  
- **VAE** performs robustly in larger families  
- **MSCMF + WGAN-GP** provides the most stable overall performance  
- ROC-AUC often exceeds **0.99** in all protein families  

---

## 📁 Repository Structure
[Click here to view the full folder structure](FOLDER_STRUCTURE.md)
---

### 📫 Contact
For questions or collaborations:
Vitor Magalhães Silva
Université TÉLUQ — Department of Science and Technology
📧 silva.vitor_magalhaes@univ.teluq.ca
🔗 GitHub: @vitormag-gh


---
## 📄 Citation

If you use this work, please cite:

**Vitor Magalhaes Silva, Khadidja Henni, and Neila Mezghani (2026).  
*Benchmarking Data Augmentation Strategies for Drug–Target Interaction Prediction under Class Imbalance: A Controlled Comparative Study.*  
Department of Information Technology, TELUQ University, Montreal, Quebec, Canada;  
Imaging and Orthopedics Research Laboratory (LIO), CHUM Research Center, Montreal, Quebec, Canada.**

### BibTeX

bibtex
@unpublished{silva2026dti,
  title = {Benchmarking Data Augmentation Strategies for Drug--Target Interaction Prediction under Class Imbalance: A Controlled Comparative Study},
  author = {Silva, Vitor Magalhaes and Henni, Khadidja and Mezghani, Neila},
  year = {2026},
  note = {Manuscript submitted to BMC Bioinformatics},
  affiliation = {
    Department of Information Technology, TELUQ University, Montreal, Quebec, Canada;
    Imaging and Orthopedics Research Laboratory (LIO), CHUM Research Center, Montreal, Quebec, Canada
  },
  orcid = {
    Silva: 0009-0003-5233-9161;
    Henni: 0000-0002-3019-3187;
    Mezghani: 0000-0002-5935-4570
  }
}
