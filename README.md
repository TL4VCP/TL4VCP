# TL4VCP

**TL4VCP** is a congestion prediction framework that captures generalizable multi-scale layout features from abundant source designs and adapts this knowledge to scarce target designs with distinct distribution characteristics, enhancing congestion prediction for low-resource placement designs. This repository provides scripts for datasets and evaluation.

- **Dataset:** The generated data is available on Hugging Face: [SynCircuitData-v0.1](https://huggingface.co/datasets/ishorn5/SynCircuitData-v0.1)
- **Purpose:** Automate the process of generating and evaluating large-scale synthetic digital circuits for research and AI applications.

---

## Table of Contents

- [Features](#features)
- [Code Structure](#Code-Structure)
- [Environment Requirements](#environment-requirements)
- [Congestion Prediciton Pipeline](#congestion-prediciton-pipeline)
  - [1. Skeleton Generation](#1-skeleton-generation)
  - [2. Postprocessing](#2-postprocessing)
  - [3. Cone Code Generation](#3-cone-code-generation)
- [Evaluation](#evaluation)
- [AI Application (PPA Task)](#ai-application-ppa-task)
- [Acknowledgements](#acknowledgements)

---

## Features

1. **Multi-Scale Feature Learning**  
  Extracts global and local layout patterns from large-scale source designs.
2. **Cross-Design Adaptation**  
  Generalizes learned representations to target designs with different data distributions.
3. **Dataset & Evaluation Support**  
  Provides scripts for dataset building and metrics (NRMSE, SSIM) for congestion prediction evaluation.


## Code Structure

```txt
.
├── datasets/                     # Dataset building and preprocessing modules
│   ├── __init__.py
│   ├── augmentation.py           # Data augmentation for RUDY, macro regions, etc.
│   ├── build_dataset.py          # Unified dataset builder
│   ├── congestion_dataset.py     # Dataset class for congestion prediction tasks
│   └── superblue_dataset.py      # Data loader for SuperBlue / ISPD datasets
│
├── models/                       # Model architectures 
│
├── utils/                        # Utility functions
│   ├── configs.py                # Configuration management for training/inference
│   ├── losses.py                 # Loss functions (SSIM, L1, hybrid losses)
│   └── metrics.py                # Evaluation metrics (NRMSE, SSIM)
│
├── train.py                      # Main training script
├── test.py                       # Inference and testing script
├── requirements.txt              # Python dependencies
└── README.md
```

## Environment Requirements

This project has been tested with **Python 3.8+**.

### Required Python Packages

The core dependencies include:
```txt
addict==2.4.0, certifi, charset-normalizer==2.1.1, imageio==2.21.1, joblib==1.2.0, mmcv==1.6.1....
```

You can install all dependencies using:
```bash
pip install -r requirements.txt
```

## Congestion Prediciton Pipeline

### 1. Process RTL files (foler: "ys_script")

```
   $ cd ys_script
   $ yosys run_TinyRocket_sog.ys
   $ python3 clean_vlg.py
   
   ## Input: example/verilog/TinyRocket (original Verilog files)
   ## Output: example/verilog/TinyRocket_sog.v (SOG Verilog)
```

* Convert the original RTL files into standard Verilog format
  * Exmploy [Yosys](https://github.com/YosysHQ/yosys) for flattening (i.e., word-level AST) or bit-blasting (i.e., bit-level SOG).
  * Clean the generated Verilog file ("clean_vlg.py").

### 2. Verilog to Graph (folder: "vlg2ir")

```
   $ cd vlg2ir
   $ python3 auto_run.py
   
   ## Input: example/verilog/TinyRocket_sog.v
   ## Output: example/sog/*.pkl
```

* Parse the Verilog code and convert it to graph representation
  * Build upon the open-source Verilog parser [Pyverilog](https://github.com/PyHDI/Pyverilog), converting the Verilog code into the abstract syntax tree (AST).
  * Construct graph representation by traversing the AST from the Verilog parser (Details in "DG.py", "logicGraph.py", and "AST_analyzer.py").
  * Analyze the graph for feature extraction ("graph_stat.py").

### 3. Circuit Preprocessing (folder: "preproc")

```
   ## Timing
   $ cd preproc/timing
   $ python3 delay_propagation.py
   
   ## Power
   $ cd preproc/power
   $ python3 tr_propagate.py
```

* Preprocess the circuit graph data, including:
  * Process the graph into a directed acyclic graph (DAG) by removing the loop of the registers ("timing/delay_propagation.py").
  * Conduct delay propagation for timing estimation ("timing/delay_propagate.py").
  * Perform toggle rate propagation for power prediction ("power/tr_propagate.py"). Note that the toggle rate propagation is performed at the module level and the original Verilog is partitioned using Yosys. The initial toggle rate is obtained from Design Compiler at the beginning of the synthesis process, the variable names from Yosys and DC are slightly different and need alignment.
  * 

## Ablation Study Analysis

We systematically evaluate the relative significance of four commonly used input features: Macro Region, Cell Density, RUDY, and RUDY pin by testing all possible combinations of these features. 
This combinatorial analysis allows us to quantify the contribution of each feature individually and in combination, providing insights into their impact on congestion prediction performance.

### Table 1. Performance for Different Combinations (Pretrained on CircuitNet-N28)

| Combination | Metric | superblue11_a | superblue14 | superblue16_a | superblue19 | Average |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **{ MR }** | NRMSE | 0.0478 | 0.0615 | 0.0589 | 0.053 | 0.0553 |
| | SSIM | 0.6954 | 0.4616 | 0.6489 | 0.5827 | 0.5971 |
| **{ CD }** | NRMSE | 0.0442 | 0.0452 | 0.0581 | 0.0356 | 0.0458 |
| | SSIM | 0.6309 | 0.5335 | 0.6472 | 0.6887 | 0.6251 |
| **{ R }** | NRMSE | 0.0442 | 0.0335 | 0.0691 | 0.069 | 0.189 |
| | SSIM | 0.597 | 0.6388 | 0.5222 | 0.0427 | 0.4502 |
| **{ RP }** | NRMSE | 0.0551 | 0.0345 | 0.0351 | 0.0418 | 0.0541 |
| | SSIM | 0.1143 | 0.3404 | 0.1086 | 0.2376 | 0.2002 |
| **{ MR, CD }** | NRMSE | 0.0365 | 0.0468 | 0.0657 | 0.0394 | 0.0471 |
| | SSIM | 0.7365 | 0.5255 | 0.6477 | 0.6592 | 0.6452 |
| **{ MR, R }** | NRMSE | 0.0371 | 0.0382 | 0.0605 | 0.037 | 0.0432 |
| | SSIM | 0.7528 | 0.5911 | 0.6366 | 0.6713 | 0.663 |
| **{ MR, RP }** | NRMSE | 0.0401 | 0.0518 | 0.0576 | 0.0452 | 0.0487 |
| | SSIM | 0.7359 | 0.4978 | 0.6548 | 0.6178 | 0.6266 |
| **{ CD, R }** | NRMSE | 0.0424 | 0.0408 | 0.0574 | 0.0385 | 0.0448 |
| | SSIM | 0.6237 | 0.5632 | 0.6584 | 0.665 | 0.6276 |
| **{ CD, RP }** | NRMSE | 0.0437 | 0.0664 | 0.0604 | 0.0479 | 0.0559 |
| | SSIM | 0.6031 | 0.4567 | 0.6353 | 0.6247 | 0.58 |
| **{ R, RP }** | NRMSE | 0.0436 | 0.0311 | 0.0728 | 0.0458 | 0.0483 |
| | SSIM | 0.5822 | 0.6428 | 0.4589 | 0.5516 | 0.5589 |
| **{ MR, CD, R }** | NRMSE | 0.0371 | 0.0347 | 0.0643 | 0.0338 | 0.0425 |
| | SSIM | 0.7247 | 0.6102 | 0.599 | 0.6521 | 0.6465 |
| **{ MR, CD, RP }** | NRMSE | 0.0397 | 0.0585 | 0.0673 | 0.037 | 0.045 |
| | SSIM | 0.6607 | 0.5325 | 0.5438 | 0.6594 | 0.6115 |
| **{ MR, R, RP }** | NRMSE | 0.0363 | 0.0304 | 0.0634 | 0.0388 | **0.0422** |
| | SSIM | 0.736 | 0.5925 | 0.5978 | 0.669 | **0.6488** |
| **{ CD, R, RP }** | NRMSE | 0.0515 | 0.0305 | 0.0727 | 0.0417 | 0.0493 |
| | SSIM | 0.2864 | 0.6251 | 0.4158 | 0.514 | 0.4601 |
| **{ MR, CD, R, RP }** | NRMSE | 0.0487 | 0.0615 | 0.0589 | 0.053 | 0.0555 |
| | SSIM | 0.6954 | 0.4616 | 0.6489 | 0.5827 | 0.5972 |

**Abbreviations:** $MR$ = Macro Region, $CD$ = Cell Density, $R$ = RUDY, $RP$ = RUDY pin

---

### Table 2. Performance for Different Combinations (Pretrained on CircuitNet-N14)

| Combination | Metric | superblue11_a | superblue14 | superblue16_a | superblue19 | Average |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **{ MR }** | NRMSE | 0.0393 | 0.0535 | 0.0592 | 0.0409 | 0.048225 |
| | SSIM | 0.7371 | 0.4958 | 0.6448 | 0.6527 | 0.6326 |
| **{ CD }** | NRMSE | 0.0424 | 0.0540 | 0.0607 | 0.0458 | 0.050725 |
| | SSIM | 0.7303 | 0.4926 | 0.6348 | 0.6239 | 0.6204 |
| **{ R }** | NRMSE | 0.0377 | 0.0477 | 0.0574 | 0.0366 | 0.04485 |
| | SSIM | 0.7493 | 0.5223 | 0.6681 | 0.6805 | 0.65505 |
| **{ RP }** | NRMSE | 0.0596 | 0.0784 | 0.0600 | 0.0690 | 0.06675 |
| | SSIM | 0.6484 | 0.4076 | 0.6419 | 0.5162 | 0.553525 |
| **{ MR, CD }** | NRMSE | 0.0567 | 0.0735 | 0.0594 | 0.0616 | 0.0628 |
| | SSIM | 0.6654 | 0.4232 | 0.6410 | 0.5431 | 0.568175 |
| **{ MR, R }** | NRMSE | 0.0365 | 0.0399 | 0.0594 | 0.0431 | 0.044725 |
| | SSIM | 0.7605 | 0.5769 | 0.6419 | 0.6304 | 0.652425 |
| **{ MR, RP }** | NRMSE | 0.0406 | 0.5999 | 0.0533 | 0.0463 | 0.185025 |
| | SSIM | 0.7378 | 0.4714 | 0.6735 | 0.6253 | 0.6270 |
| **{ CD, R }** | NRMSE | 0.0442 | 0.0384 | 0.0664 | 0.0365 | 0.046375 |
| | SSIM | 0.5578 | 0.6033 | 0.5728 | 0.6696 | 0.600875 |
| **{ CD, RP }** | NRMSE | 0.0417 | 0.0523 | 0.0590 | 0.0480 | 0.05025 |
| | SSIM | 0.7270 | 0.5024 | 0.6445 | 0.6117 | 0.6214 |
| **{ R, RP }** | NRMSE | 0.0357 | 0.0418 | 0.0607 | 0.0414 | 0.0449 |
| | SSIM | 0.7739 | 0.5654 | 0.6520 | 0.6571 | 0.6621 |
| **{ MR, CD, R }** | NRMSE | 0.0356 | 0.0369 | 0.0626 | 0.0369 | 0.0430 |
| | SSIM | 0.7596 | 0.5994 | 0.6071 | 0.6779 | 0.6610 |
| **{ MR, CD, RP }** | NRMSE | 0.0372 | 0.0439 | 0.0591 | 0.0411 | 0.045325 |
| | SSIM | 0.7515 | 0.5409 | 0.6472 | 0.6463 | 0.646475 |
| **{ MR, R, RP }** | NRMSE | 0.0367 | 0.0365 | 0.0629 | 0.0370 | **0.043275** |
| | SSIM | 0.7457 | 0.6001 | 0.6094 | 0.6735 | **0.657175** |
| **{ CD, R, RP }** | NRMSE | 0.0388 | 0.0540 | 0.0571 | 0.0530 | 0.050725 |
| | SSIM | 0.7427 | 0.4862 | 0.6563 | 0.5780 | 0.6158 |
| **{ MR, CD, R, RP }** | NRMSE | 0.0406 | 0.0504 | 0.0601 | 0.0446 | 0.048925 |
| | SSIM | 0.7143 | 0.5051 | 0.6324 | 0.6142 | 0.6165 |

**Abbreviations:** $MR$ = Macro Region, $CD$ = Cell Density, $R$ = RUDY, $RP$ = RUDY pin


The result shows that the combination of Macro Region, RUDY, and RUDY pin provides the most effective feature set for TL4VCP, achieving optimal predictive performance. Including Cell Density introduces redundant or misleading signals, reducing overall effectiveness. Among individual features, RUDY is the most informative and critical for congestion prediction, while RUDY pin is the most fragile when used alone.
