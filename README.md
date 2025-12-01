# TL4VCP

**TL4VCP** is a congestion prediction framework that captures generalizable multi-scale layout features from abundant source designs and adapts this knowledge to scarce target designs with distinct distribution characteristics, enhancing congestion prediction for low-resource placement designs. This repository provides scripts for datasets and evaluation.

- **Dataset:** The generated data is available on Hugging Face: [SynCircuitData-v0.1](https://huggingface.co/datasets/ishorn5/SynCircuitData-v0.1)
- **Purpose:** Automate the process of generating and evaluating large-scale synthetic digital circuits for research and AI applications.

---

## Table of Contents

- [Features](#features)
- [Environment Requirements](#environment-requirements)
- [Data Generation Pipeline](#data-generation-pipeline)
  - [1. Skeleton Generation](#1-skeleton-generation)
  - [2. Postprocessing](#2-postprocessing)
  - [3. Cone Code Generation](#3-cone-code-generation)
- [Evaluation](#evaluation)
- [AI Application (PPA Task)](#ai-application-ppa-task)
- [Acknowledgements](#acknowledgements)

---

## Code Structure

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
