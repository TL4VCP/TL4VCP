# TL4VCP

**TL4VCP** is a congestion prediction framework that captures generalizable multi-scale layout features from abundant source designs and adapts this knowledge to scarce target designs with distinct distribution characteristics, enhancing congestion prediction for low-resource placement designs. This repository provides scripts for datasets and evaluation.

- **Dataset:** The generated data is available on Hugging Face: [SynCircuitData-v0.1](https://huggingface.co/datasets/ishorn5/SynCircuitData-v0.1)
- **Purpose:** Automate the process of generating and evaluating large-scale synthetic digital circuits for research and AI applications.

---

## Table of Contents

- [Features](#features)
- [Code Structure](#Code-Structure)
- [Environment Requirements](#environment-requirements)
- [Data Generation Pipeline](#data-generation-pipeline)
  - [1. Skeleton Generation](#1-skeleton-generation)
  - [2. Postprocessing](#2-postprocessing)
  - [3. Cone Code Generation](#3-cone-code-generation)
- [Evaluation](#evaluation)
- [AI Application (PPA Task)](#ai-application-ppa-task)
- [Acknowledgements](#acknowledgements)

---

## Features

- **Generalizable Multi-Scale Feature Learning**  
  Learns multi-level spatial representations from large-scale source designs to capture both global and local layout patterns.

- **Cross-Design Adaptation**  
  Transfers knowledge from source datasets to target designs with different distribution characteristics, ensuring robust performance across heterogeneous chip layouts.

- **Low-Resource Design Enhancement**  
  Improves congestion prediction accuracy on target placement designs with limited data availability.

- **Dataset Preparation Scripts**  
  Provides modular tools for dataset construction, augmentation, and loading, supporting Congestion and SuperBlue/ISPD benchmarks.

- **Comprehensive Evaluation Pipeline**  
  Includes testing utilities and metrics (NRMSE, SSIM) for rigorous evaluation of congestion prediction models.


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

## Environment Requirements

This project has been tested with **Python 3.8+**.

### Required Python Packages

The core dependencies include:

## 🛠️ Environment Requirements

```txt
addict==2.4.0
certifi
charset-normalizer==2.1.1
idna==3.3
imageio==2.21.1
joblib==1.2.0
mmcv==1.6.1
numpy==1.23.2
opencv-python==4.6.0.66
packaging==21.3
Pillow==9.3.0
psutil==5.9.1
pyparsing==3.0.9
pyutil==3.3.0
PyWavelets==1.3.0
PyYAML==6.0
requests==2.28.1
scikit-image==0.19.3
scikit-learn==1.1.2
scipy==1.9.0
threadpoolctl==3.1.0
tifffile==2022.8.12
tqdm==4.64.0
typing_extensions==4.3.0
urllib3==1.26.12
yapf==0.32.0

You can install all dependencies using:

```bash
pip install -r requirements.txt



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



The result shows that the combination of Macro Region, RUDY, and RUDY pin provides the most effective feature set for TL4VCP, achieving optimal predictive performance. Including Cell Density introduces redundant or misleading signals, reducing overall effectiveness. Among individual features, RUDY is the most informative and critical for congestion prediction, while RUDY pin is the most fragile when used alone.
