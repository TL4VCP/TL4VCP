# TL4VCP

**TL4VCP** is a congestion prediction framework that captures generalizable multi-scale layout features from abundant source designs and adapts this knowledge to scarce target designs with distinct distribution characteristics, enhancing congestion prediction for low-resource placement designs. This repository provides scripts for datasets and evaluation.

- **Dataset:** The dataset is available on: [CircuitNet](https://circuitnet.github.io/)
- **Purpose:** Congestion prediction in low-resource VLSI placements via multi-scale features from source designs.

## Table of Contents

- [Features](#features)
- [Code Structure](#code-structure)
- [Environment Requirements](#environment-requirements)
- [Congestion Prediciton Pipeline](#congestion-prediciton-pipeline)
  - [1. Skeleton Generation](#1-skeleton-generation)
  - [2. Postprocessing](#2-postprocessing)
  - [3. Cone Code Generation](#3-cone-code-generation)
- [Ablation Study Analysis](#ablation-study-analysis)

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
  

## Ablation Study Analysis

We systematically evaluate the relative significance of four commonly used input features: Macro Region, Cell Density, RUDY, and RUDY pin by testing all possible combinations of these features. 
This combinatorial analysis allows us to quantify the contribution of each feature individually and in combination, providing insights into their impact on congestion prediction performance.


<table>
<tr>
<td>

<!-- Table 1 -->
<table border="1" cellspacing="0" cellpadding="4">
  <caption style="caption-side: top; text-align: center;">
  <b>Table 1. Performance (Pretrained on CircuitNet-N28)</b>
  </caption>
  <tr><th>Combination</th><th>superblue11_a</th><th>superblue14</th><th>superblue16_a</th><th>superblue19</th><th>Avg</th></tr>
  <tr><td>{MR}</td><td>0.0478/0.6954</td><td>0.0615/0.4616</td><td>0.0589/0.6489</td><td>0.053/0.5827</td><td>0.0553/0.5971</td></tr>
  <tr><td>{CD}</td><td>0.0442/0.6309</td><td>0.0452/0.5335</td><td>0.0581/0.6472</td><td>0.0356/0.6887</td><td>0.0458/0.6251</td></tr>
  <tr><td>{R}</td><td>0.0442/0.597</td><td>0.0335/0.6388</td><td>0.0691/0.5222</td><td>0.069/0.0427</td><td>0.189/0.4502</td></tr>
  <tr><td>{RP}</td><td>0.0551/0.1143</td><td>0.0345/0.3404</td><td>0.0351/0.1086</td><td>0.0418/0.2376</td><td>0.0541/0.2002</td></tr>
  <tr><td>{MR,CD}</td><td>0.0365/0.7365</td><td>0.0468/0.5255</td><td>0.0657/0.6477</td><td>0.0394/0.6592</td><td>0.0471/0.6452</td></tr>
  <tr><td>{MR,R}</td><td>0.0371/0.7528</td><td>0.0382/0.5911</td><td>0.0605/0.6366</td><td>0.037/0.6713</td><td>0.0432/0.663</td></tr>
  <tr><td>{MR,RP}</td><td>0.0401/0.7359</td><td>0.0518/0.4978</td><td>0.0576/0.6548</td><td>0.0452/0.6178</td><td>0.0487/0.6266</td></tr>
  <tr><td>{CD,R}</td><td>0.0424/0.6237</td><td>0.0408/0.5632</td><td>0.0574/0.6584</td><td>0.0385/0.665</td><td>0.0448/0.6276</td></tr>
  <tr><td>{CD,RP}</td><td>0.0437/0.6031</td><td>0.0664/0.4567</td><td>0.0604/0.6353</td><td>0.0479/0.6247</td><td>0.0559/0.5800</td></tr>
  <tr><td>{R,RP}</td><td>0.0436/0.5822</td><td>0.0311/0.6428</td><td>0.0728/0.4589</td><td>0.0458/0.5516</td><td>0.0483/0.5589</td></tr>
  <tr><td>{MR,CD,R}</td><td>0.0371/0.7247</td><td>0.0347/0.6102</td><td>0.0643/0.599</td><td>0.0338/0.6521</td><td>0.0425/0.6465</td></tr>
  <tr><td>{MR,CD,RP}</td><td>0.0397/0.6607</td><td>0.0585/0.5325</td><td>0.0673/0.5438</td><td>0.037/0.6594</td><td>0.045/0.6115</td></tr>
  <tr><td>{MR,R,RP}</td><td>0.0363/0.736</td><td>0.0304/0.5925</td><td>0.0634/0.5978</td><td>0.0388/0.669</td><td><b>0.0422/0.6488</b></td></tr>
  <tr><td>{CD,R,RP}</td><td>0.0515/0.2864</td><td>0.0305/0.6251</td><td>0.0727/0.4158</td><td>0.0417/0.514</td><td>0.0493/0.4601</td></tr>
  <tr><td>{MR,CD,R,RP}</td><td>0.0487/0.6954</td><td>0.0615/0.4616</td><td>0.0589/0.6489</td><td>0.053/0.5827</td><td>0.0555/0.5972</td></tr>
</table>

</td>
<td style="padding-left:20px;">

<!-- Table 2 -->
<table border="1" cellspacing="0" cellpadding="4">
  <caption style="caption-side: top; text-align: center;">
    <b>Table 2. Performance (Pretrained on CircuitNet-N14)</b>
  </caption>
  <tr><th>Combination</th><th>superblue11_a</th><th>superblue14</th><th>superblue16_a</th><th>superblue19</th><th>Avg</th></tr>
  <tr><td>{MR}</td><td>0.0393/0.7371</td><td>0.0535/0.4958</td><td>0.0592/0.6448</td><td>0.0409/0.6527</td><td>0.0482/0.6326</td></tr>
  <tr><td>{CD}</td><td>0.0424/0.7303</td><td>0.0540/0.4926</td><td>0.0607/0.6348</td><td>0.0458/0.6239</td><td>0.0507/0.6204</td></tr>
  <tr><td>{R}</td><td>0.0377/0.7493</td><td>0.0477/0.5223</td><td>0.0574/0.6681</td><td>0.0366/0.6805</td><td>0.0449/0.6551</td></tr>
  <tr><td>{RP}</td><td>0.0596/0.6484</td><td>0.0784/0.4076</td><td>0.0600/0.6419</td><td>0.0690/0.5162</td><td>0.0668/0.5535</td></tr>
  <tr><td>{MR,CD}</td><td>0.0567/0.6654</td><td>0.0735/0.4232</td><td>0.0594/0.6410</td><td>0.0616/0.5431</td><td>0.0628/0.568175</td></tr>
  <tr><td>{MR,R}</td><td>0.0365/0.7605</td><td>0.0399/0.5769</td><td>0.0594/0.6419</td><td>0.0431/0.6304</td><td>0.0447/0.6524</td></tr>
  <tr><td>{MR,RP}</td><td>0.0406/0.7378</td><td>0.0599/0.4714</td><td>0.0533/0.6735</td><td>0.0463/0.6253</td><td>0.1850/0.6270</td></tr>
  <tr><td>{CD,R}</td><td>0.0442/0.5578</td><td>0.0384/0.6033</td><td>0.0664/0.5728</td><td>0.0365/0.6696</td><td>0.0464/0.6009</td></tr>
  <tr><td>{CD,RP}</td><td>0.0417/0.7270</td><td>0.0523/0.5024</td><td>0.0590/0.6445</td><td>0.0480/0.6117</td><td>0.0503/0.6214</td></tr>
  <tr><td>{R,RP}</td><td>0.0357/0.7739</td><td>0.0418/0.5654</td><td>0.0607/0.6520</td><td>0.0414/0.6571</td><td>0.0449/0.6621</td></tr>
  <tr><td>{MR,CD,R}</td><td>0.0356/0.7596</td><td>0.0369/0.5994</td><td>0.0626/0.6071</td><td>0.0369/0.6779</td><td>0.0430/0.6610</td></tr>
  <tr><td>{MR,CD,RP}</td><td>0.0372/0.7515</td><td>0.0439/0.5409</td><td>0.0591/0.6472</td><td>0.0411/0.6463</td><td>0.0453/0.6465</td></tr>
  <tr><td>{MR,R,RP}</td><td>0.0367/0.7457</td><td>0.0365/0.6001</td><td>0.0629/0.6094</td><td>0.0370/0.6735</td><td><b>0.0433/0.6572</b></td></tr>
  <tr><td>{CD,R,RP}</td><td>0.0388/0.7427</td><td>0.0540/0.4862</td><td>0.0571/0.6563</td><td>0.0530/0.5780</td><td>0.0507/0.6158</td></tr>
  <tr><td>{MR,CD,R,RP}</td><td>0.0406/0.7143</td><td>0.0504/0.5051</td><td>0.0601/0.6324</td><td>0.0446/0.6142</td><td>0.0489/0.6165</td></tr>
</table>

</td>
</tr>
</table>

**Abbreviations:** $MR$ = Macro Region, $CD$ = Cell Density, $R$ = RUDY, $RP$ = RUDY pin

The result shows that the combination of Macro Region, RUDY, and RUDY pin provides the most effective feature set for TL4VCP, achieving optimal predictive performance. Including Cell Density introduces redundant or misleading signals, reducing overall effectiveness. Among individual features, RUDY is the most informative and critical for congestion prediction, while RUDY pin is the most fragile when used alone.


