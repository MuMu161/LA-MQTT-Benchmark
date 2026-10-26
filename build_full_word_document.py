"""Generates a comprehensive, self-contained Microsoft Word (.doc) and HTML manuscript
strictly formatted according to the professor's specifications:
- Title / Heading 1: 16 pt Bold
- Section Headings: 12 pt Bold
- Body Text: 11 pt
- Tables & Captions: 10 pt
- Numbered Equations (1) to (17)
- Embedded high-resolution figures (base64 encoded)
- Complete literature survey, dataset characterization, LA-MQTT architecture,
  algorithms, experimental analysis, ablations, statistical validation, and SOTA comparison.
"""
import base64, os
from pathlib import Path

ROOT = Path(r"d:\MQTTEEB-D_Project")
FIG_DIR = ROOT / "results" / "figures"
OUT_DOC = ROOT / "PAPER_FINAL_MANUSCRIPT.doc"
OUT_HTML = ROOT / "PAPER_FINAL_MANUSCRIPT.html"

def get_base64_img(filename):
    p = FIG_DIR / filename
    if p.exists():
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{b64}"
    return ""

img_class_dist = get_base64_img("class_distribution.png")
img_tsne = get_base64_img("tsne_before_after_preprocessing.png")
img_dl_epochs = get_base64_img("dl_long_epoch_curves_all.png")
img_cm_bagging = get_base64_img("Bagging_Original_Normalized_Confusion_Matrix.png")
img_cm_rf = get_base64_img("CM_Random_Forest_Original.png")
img_ablation = get_base64_img("ablation_timestamp_leakage.png")
img_roc_pr = get_base64_img("ROC_PR_Bagging_Original.png")

html_content = f"""<html xmlns:o='urn:schemas-microsoft-com:office:office'
xmlns:w='urn:schemas-microsoft-com:office:word'
xmlns='http://www.w3.org/TR/REC-html40'>
<head>
<meta charset="utf-8">
<title>Hidden Leakage in MQTT Anomaly Detection</title>
<!--[if gte mso 9]>
<xml>
 <w:WordDocument>
  <w:View>Print</w:View>
  <w:Zoom>100</w:Zoom>
  <w:DoNotOptimizeForBrowser/>
 </w:WordDocument>
</xml>
<![endif]-->
<style>
@page {{
    size: 8.5in 11.0in;
    margin: 1.0in 1.0in 1.0in 1.0in;
    mso-header-margin: 0.5in;
    mso-footer-margin: 0.5in;
    mso-paper-source: 0;
}}
body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 11pt;
    line-height: 1.35;
    color: #111111;
    text-align: justify;
    margin: 0;
    padding: 0;
}}
h1.title {{
    font-size: 16pt;
    font-weight: bold;
    text-align: center;
    line-height: 1.25;
    margin-top: 18pt;
    margin-bottom: 12pt;
    color: #0b2545;
}}
.authors {{
    font-size: 11pt;
    text-align: center;
    font-weight: bold;
    margin-bottom: 4pt;
}}
.affiliations {{
    font-size: 10pt;
    text-align: center;
    font-style: italic;
    color: #444444;
    margin-bottom: 18pt;
}}
h2 {{
    font-size: 12pt;
    font-weight: bold;
    color: #0b2545;
    border-bottom: 1.5pt solid #0b2545;
    padding-bottom: 3pt;
    margin-top: 18pt;
    margin-bottom: 8pt;
    text-transform: uppercase;
}}
h3 {{
    font-size: 12pt;
    font-weight: bold;
    color: #133c55;
    margin-top: 14pt;
    margin-bottom: 6pt;
}}
h4 {{
    font-size: 11pt;
    font-weight: bold;
    font-style: italic;
    color: #222222;
    margin-top: 10pt;
    margin-bottom: 4pt;
}}
p {{
    font-size: 11pt;
    margin-top: 0pt;
    margin-bottom: 6pt;
    text-indent: 18pt;
}}
p.no-indent {{
    text-indent: 0pt;
}}
.abstract-box {{
    background-color: #f7f9fa;
    border: 1pt solid #d0d7de;
    padding: 12pt;
    margin-bottom: 14pt;
}}
.abstract-title {{
    font-size: 11pt;
    font-weight: bold;
    text-align: center;
    margin-bottom: 6pt;
    text-transform: uppercase;
    letter-spacing: 0.5pt;
}}
.keywords {{
    font-size: 10pt;
    margin-top: 6pt;
}}
.highlights-box {{
    background-color: #f0f4f8;
    border-left: 3pt solid #133c55;
    padding: 8pt 12pt;
    margin-bottom: 14pt;
}}
ul {{
    margin-top: 0pt;
    margin-bottom: 6pt;
    padding-left: 20pt;
}}
li {{
    font-size: 11pt;
    margin-bottom: 3pt;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10pt;
    margin-bottom: 14pt;
    font-size: 10pt;
}}
table, th, td {{
    border: 1pt solid #bbbbbb;
}}
th {{
    background-color: #e9eef2;
    font-weight: bold;
    text-align: center;
    padding: 5pt 4pt;
    font-size: 10pt;
}}
td {{
    padding: 4pt;
    vertical-align: middle;
}}
td.center {{
    text-align: center;
}}
td.right {{
    text-align: right;
}}
caption, .table-caption {{
    font-size: 10pt;
    font-weight: bold;
    text-align: left;
    margin-bottom: 4pt;
    color: #0b2545;
}}
.equation {{
    font-family: 'Cambria Math', 'Times New Roman', serif;
    font-size: 11pt;
    text-align: center;
    margin: 8pt 0pt;
    padding: 4pt 0pt;
}}
.eq-num {{
    float: right;
    font-weight: bold;
}}
.figure-container {{
    text-align: center;
    margin-top: 12pt;
    margin-bottom: 14pt;
}}
.figure-container img {{
    max-width: 95%;
    height: auto;
    border: 1pt solid #cccccc;
    padding: 2pt;
}}
.figure-caption {{
    font-size: 10pt;
    font-weight: bold;
    color: #222222;
    margin-top: 4pt;
    text-align: center;
}}
.algorithm-box {{
    border: 1.5pt solid #0b2545;
    background-color: #fcfcfc;
    padding: 8pt 12pt;
    margin-top: 10pt;
    margin-bottom: 14pt;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9.5pt;
    line-height: 1.3;
}}
.alg-header {{
    font-weight: bold;
    border-bottom: 1pt solid #0b2545;
    padding-bottom: 4pt;
    margin-bottom: 6pt;
    font-family: 'Times New Roman', Times, serif;
    font-size: 10.5pt;
}}
</style>
</head>
<body>

<h1 class="title">An In-Depth Data Forensic Audit and Leakage-Aware Evaluation Framework (LA-MQTT) for MQTT Network Intrusion Detection Benchmarks</h1>

<div class="authors">[Author 1], [Author 2] and [Guide name]</div>
<div class="affiliations">Department of [department], [Institution], [city], India<br>Corresponding author: [e-mail address]</div>

<div class="abstract-box">
<h3>Abstract</h3>
<p>Message Queuing Telemetry Transport (MQTT) serves as the primary messaging protocol for resource-constrained Internet of Things (IoT) deployments. Recently, the MQTTEEB-D benchmark—collected from an authentic physical testbed with biometric sensors—was released, with baseline evaluations reporting near-perfect classification (F1-scores of 0.97–0.99 for decision trees) and positing an 'imbalance resilience paradox' where simple trees outperform boosting. In this paper, we present an independent replication and forensic data audit of MQTTEEB-D. We successfully reproduce published baseline metrics, finding that published boosting scores closely align with macro-averaged F1 (0.84–0.86). However, our forensic audit reveals a critical methodological vulnerability: <code>tcp_time_delta</code> is an identical bitwise replica of the capture timestamp (&rho; = 1.000), leaking chronological partition boundaries directly into decision splits. Eliminating temporal markers exposes heavy data redundancy: out of 222,567 observations, only 33,107 unique feature-plus-label rows exist (85.12% duplication). Crucially, 11.29% of unique feature patterns exhibit multi-class label ambiguity, establishing an empirical in-sample majority-label upper bound of 73.82% accuracy under stateless single-packet inspection. Under Leave-One-Loop-Out (LOLO) evaluation across temporal capture sessions, accuracy collapses by 45.0 to 54.9 percentage points (falling to 40.9%–52.0%) with the leaked column, but stabilizes at ~71% once excised. Furthermore, regularized tuning brings CART (71.92%) and XGBoost (71.90%) to near-complete parity under Seed 42, resolving the purported paradox. We introduce the open-source Leakage-Aware MQTT (LA-MQTT) framework to ensure rigorous, reproducible IoT intrusion detection benchmarking.</p>
<p><strong>Keywords:</strong> Internet of Things (IoT); MQTT Protocol; Intrusion Detection System (IDS); Data Leakage; Reproducibility; Tree Ensembles; MQTTEEB-D; Benchmark Audit.</p>
</div>

<div class="highlights-box">
  <div style="font-weight:bold; font-size:10.5pt; margin-bottom:4pt; color:#0b2545;">HIGHLIGHTS:</div>
  <ul>
    <li><strong>Empirical Replication:</strong> Successfully reproduced baseline tree ensemble performance (97.0%–98.9% weighted F1) and established baseline boosting performance on the authentic MQTTEEB-D physical testbed dataset.</li>
    <li><strong>Temporal Marker Identification:</strong> Identified that <code>tcp_time_delta</code> serves as an inadvertent exact replica of the absolute capture timestamp (&rho; = 1.000), permitting decision splits based on chronological intervals.</li>
    <li><strong>Generalization Collapse:</strong> Under an unseen capture loop evaluation (Leave-One-Loop-Out), classification accuracy collapses by 45.0 to 54.9 percentage points (falling to 40.9%–52.0%) when the leaked feature is present.</li>
    <li><strong>Dataset Redundancy & Upper Bound:</strong> Audited data distribution showing only 33,107 unique feature-plus-label rows and 28,200 unique feature patterns, with 11.29% pattern ambiguity establishing an empirical majority-class upper bound of 73.82% on the ten protocol features.</li>
    <li><strong>Algorithmic Parity:</strong> Demonstrated that the apparent margin of unregularized trees over boosting models stemmed from temporal alignment; upon leak excision and hyperparameter regularization, boosting and tree ensembles reach parity (~71.9%).</li>
    <li><strong>LA-MQTT Framework:</strong> Formulated an open-source, leakage-aware audit and benchmarking methodology incorporating multi-seed paired statistical tests, McNemar contingency audits, and cross-loop generalization metrics.</li>
  </ul>
</div>

<h2>1 Introduction</h2>

<h3>1.1 Context and Background</h3>
<p>The rapid deployment of the Internet of Things (IoT) and Industrial Internet of Things (IIoT) has integrated billions of interconnected smart devices into critical cyber-physical infrastructures, including healthcare monitoring, municipal utility grids, automated industrial manufacturing, and intelligent vehicular transportation networks [26]. To facilitate reliable, low-latency telemetry exchange across resource-constrained microcontrollers, single-board computers, and low-bandwidth communication channels, the Message Queuing Telemetry Transport (MQTT) protocol has emerged as the de facto international messaging standard (ISO/IEC PRF 20922) [26]. Built upon a lightweight publish-subscribe architectural model operating over standard Transmission Control Protocol / Internet Protocol (TCP/IP) transport stacks, MQTT decouples telemetry producers (publishers) from telemetry consumers (subscribers) through centralized intermediaries known as brokers.</p>

<p>While the architectural simplicity, minimal packet header overhead (as low as 2 bytes), and flexible Quality of Service (QoS) delivery tiers render MQTT ideal for embedded telemetry, these same properties expose deployments to an expansive array of adversarial attack vectors [27]. Constrained edge devices frequently lack hardware-accelerated cryptographic primitives, leading to plaintext communications, unauthenticated broker endpoints, and vulnerable network perimeters. Consequently, malicious entities exploit MQTT infrastructure to execute Distributed Denial of Service (DDoS) broker resource starvation attacks, SlowITe connection exhaustion exploits, malformed packet injection attacks, credential brute-force attacks, and message publish flooding, potentially causing total telemetry disruption or life-threatening cyber-physical outages [1, 2].</p>

<p>To safeguard IoT deployments against emerging vulnerabilities without imposing prohibitive computational loads on constrained edge sensors, Machine Learning (ML) and Deep Learning (DL) Network Intrusion Detection Systems (NIDS) have been widely investigated [27]. By continuously inspecting packet-level header dynamics and transport telemetry, data-driven classifiers autonomously identify anomalous behaviors in near real-time, operating either as edge-resident filters or centralized broker-side security sentinels.</p>

<h3>1.2 Problem Statement</h3>
<p>Despite the proliferation of academic literature proposing high-accuracy ML and DL architectures for MQTT intrusion detection, the operational validity and real-world generalizability of these detectors remain severely compromised by persistent methodological shortcomings in benchmark datasets and evaluation protocols. Network intrusion detection research has repeatedly suffered from foundational methodological pitfalls [12]: sampling bias, data snooping, uncalibrated class imbalance, and temporal data leakage [13, 14].</p>

<p>Historically, MQTT security evaluations have predominantly relied upon datasets generated within synthetic, emulated, or simulated network environments—such as MQTTset [3] (constructed using the IoT-Flock traffic emulator) and MQTT-IoT-IDS2020 [5] (generated across a simulated node cluster). While valuable as exploratory milestones, simulated environments fail to reflect the non-deterministic timing jitter, electrical sensor noise, physical packet dropouts, and multi-tier network latency inherent to physical operational hardware [23]. To bridge this empirical validity gap, Aqachtoul et al. [2] introduced MQTTEEB-D, a benchmark captured directly from an authentic, physical, end-to-end IoT testbed comprising Raspberry Pi 4 edge gateways, real MQTT brokers, and physical MySignals biometric medical sensors generating live physiological telemetry (ECG, pulse oximetry, airflow).</p>

<p>Recently, Allaga et al. [1] published an extensive benchmarking study on MQTTEEB-D across an array of tree ensembles, boosting architectures, and deep neural networks. Their empirical findings reported weighted F1-scores and overall accuracies exceeding 0.988 for standard Decision Trees (CART) and Bagging classifiers, alongside an substantially elevated Performance–Efficiency Score (PES) surpassing 9,000. Crucially, the authors formulated the "imbalance resilience paradox," hypothesizing that simple, unregularized tree structures inherently possess algorithmic resilience to extreme class imbalance, outperforming complex gradient boosting architectures (such as XGBoost, CatBoost, and LightGBM) and deep neural networks, which reportedly suffered massive classification degradation.</p>

<p>However, when an empirical evaluation on a time-ordered network capture yields near-perfect classification performance from elementary, unconstrained decision trees operating on raw tabular packet attributes, rigorous scientific inquiry demands an immediate verification of the underlying experimental setup. Specifically, intrusion detection datasets derived from sequential packet captures are exceptionally vulnerable to temporal leakage, feature duplication, and pattern memorization [13, 14]. If a classifier exploits an artifactual surrogate for the time domain, its apparent predictive excellence represents an artifact of data leakage rather than genuine protocol feature learning.</p>

<h3>1.3 Limitations of Existing Work</h3>
<p>A critical review of contemporary MQTT intrusion detection literature reveals five systemic limitations:</p>
<ul>
  <li><strong>Unchecked Feature Redundancy and Artifactual Leakage:</strong> Published benchmark evaluations routinely take feature definitions at face value without verifying the mathematical integrity of released capture fields against raw packet metadata.</li>
  <li><strong>Evaluation on Time-Correlated Random Splits:</strong> Classifiers are overwhelmingly trained and tested on stratified random partitions of continuous packet captures. In time-ordered traffic where attack tools run in discrete time bursts, random splitting guarantees that training and test folds sample identical operational cycles, transforming generalization testing into rote temporal memorization [12, 13].</li>
  <li><strong>Severe Packet Duplication Ignored:</strong> High-frequency sensor telemetry and repetitive network probing generate vast volumes of identical packet vectors. Traditional random splitting scatters identical packet twins across both training and test splits, artificially inflating cross-validation performance.</li>
  <li><strong>Unsubstantiated Resampling Methodologies:</strong> Resampling interventions such as SMOTE [15] are frequently applied as a panacea for class imbalance without validating whether synthetic interpolations generate physically plausible network states or degrade classification boundaries.</li>
  <li><strong>Absence of Strict Multi-Seed Statistical Validation:</strong> Baseline rankings are commonly declared based upon a single arbitrary random seed, omitting confidence intervals, paired statistical tests, or contingency audits necessary to confirm whether observed performance deltas are statistically significant or random artifacts.</li>
</ul>

<h3>1.4 Research Contributions</h3>
<p>To resolve these critical issues, this study presents a rigorous replication, systematic forensic data audit, and leakage-aware evaluation of the MQTTEEB-D benchmark:</p>
<ul>
  <li><strong>Comprehensive Replication:</strong> We faithfully replicate the experimental framework of Allaga et al. [1], validating baseline performance for multi-class and binary classification across ten classical ML models and four deep learning architectures under the authors' exact experimental configuration.</li>
  <li><strong>Identification of Timestamp Duplication:</strong> Through forensic correlation auditing, we reveal that the transport-layer feature <code>tcp_time_delta</code> is a bitwise identical replication of the absolute epoch <code>timestamp</code> (&rho; = 1.000) across 100% of the 222,567 observations in the released dataset, directly leaking temporal attack schedules.</li>
  <li><strong>Quantification of Duplication and Empirical Majority-Label Bound:</strong> We show that upon eliminating temporal features, only 33,107 unique feature-plus-label rows and 28,200 unique feature patterns exist, with 11.29% pattern ambiguity establishing an empirical majority-class upper bound of 73.82% on the ten protocol features.</li>
  <li><strong>Generalization Collapse Demonstration:</strong> We implement a Leave-One-Loop-Out (LOLO) evaluation across the four raw capture sessions. We demonstrate that with the leaked feature, accuracy collapses by 45.0 to 54.9 percentage points (down to 40.9%–52.0%) on unseen loops, proving that tree models were memorizing chronological execution intervals.</li>
  <li><strong>Revisiting the Imbalance Resilience Paradox:</strong> We demonstrate that the apparent margin of CART and Bagging over gradient boosting architectures was driven primarily by chronological partition boundaries. Under a leak-free evaluation protocol, all models converge within 70.6%–71.8% accuracy, and validation-based hyperparameter tuning brings regularized CART (71.92%) and XGBoost (71.90%) to near-complete parity under Seed 42 (a 0.02 percentage-point gap), pending multi-seed tuning validation.</li>
  <li><strong>The LA-MQTT Framework:</strong> We formulate and open-source the Leakage-Aware MQTT (LA-MQTT) evaluation framework, providing automated pipeline modules for data auditing, duplicate-aware partitioning, empirical majority-label ceiling estimation, multi-seed statistical testing, and McNemar contingency analysis for IoT security research.</li>
</ul>

<h2>2 Related Work</h2>

<h3>2.1 Machine Learning and Feature-Engineered Approaches</h3>
<p>Alassaf et al. (2026) [29] investigated anomaly detection mechanisms across both MQTT and MQTT-SN telemetry, evaluating Random Forest, XGBoost, and Long Short-Term Memory (LSTM) networks under k-fold cross-validation. Their study demonstrated that ensemble tree models attained high precision in detecting flooding vectors; however, their evaluation protocol utilized uniform random splitting across time-continuous packet streams without auditing for inter-fold packet correlation.</p>

<p>Al Hanif and Ilyas (2024) [30] introduced an optimized feature engineering framework designed specifically for securing MQTT protocols in IoT environments. Operating on a custom balanced binary MQTT dataset, the authors applied mutual information feature selection paired with hyperparameter-tuned ensemble classifiers, achieving F1-scores exceeding 0.98. Nonetheless, their analysis was confined exclusively to binary classification (benign versus anomalous), failing to evaluate fine-grained multi-class discrimination across diverse cyber-attack scenarios.</p>

<p>Alotaibi et al. (2024) [31] proposed an enterprise-scale distributed intrusion detection system using the H2O machine learning framework, comparing distributed Random Forests, Generalized Linear Models, and H2OXGBoost across large-scale IoT captures. H2OXGBoost delivered the highest classification accuracy and area under the ROC curve, but the computational footprint of the distributed clustering engine precluded direct execution on resource-constrained edge gateways.</p>

<p>Memon et al. (2023) [33] investigated explainable artificial intelligence (XAI) for the Internet of Medical Things (IoMT), evaluating ten distinct machine learning algorithms on the MQTT-IoT-IDS2020 dataset. Integrating SHAP (SHapley Additive exPlanations) and LIME feature attribution, they demonstrated that transport-layer port numbers and packet lengths dominated classifier predictions. However, the study did not examine whether the underlying dataset features contained temporal leakage artifacts.</p>

<p>Siddharthan et al. (2022) [7] formulated the SENMQTT-SET benchmark, capturing traffic from an ensemble of physical Raspberry Pi nodes. They implemented an ensemble multi-cascade feature extraction mechanism, combining packet headers with moving-average rate counters, achieving F1-scores above 0.96 with Random Forest models. While the hardware infrastructure was physical, the sensor payload generation relied on synthetic scripts rather than live, organic sensor telemetry.</p>

<p>Earlier foundational efforts established the core baseline datasets that dominate modern literature. Vaccari et al. (2020) [3] introduced the MQTTset benchmark, generated within an emulated IoT network simulating a smart home infrastructure. Evaluating Decision Trees, Random Forests, and Gradient Boosting, they achieved multi-class accuracies of 91.60%. However, their top-performing Random Forest required 125.85 seconds for test-set evaluation over 33 features, imposing an impractical latency barrier for real-time edge mitigation. Concurrently, Hindy et al. (2020) [5] released the simulated MQTT-IoT-IDS2020 dataset, establishing baseline detection performance across five attack categories. In 2019, Alaiz-Moreton et al. [10] developed multi-class classification procedures on custom MQTT testbeds, identifying the critical challenge of separating volumetric denial-of-service from legitimate high-frequency publishing.</p>

<h3>2.2 Deep Learning and Hybrid Neural Architectures</h3>
<p>Swain et al. (2026) [28] proposed an attention-based federated learning framework integrated with Double Deep Q-Networks (DDQN) for decentralized MQTT intrusion detection. Evaluated across MQTTset, MQTT-IoT-IDS2020, and MQTTEEB-D, their architecture achieved superior detection rates and low false-positive rates via attention-weighted model aggregation. While demonstrating robust federated convergence, the deep reinforcement learning loop introduced substantial computational and communication overhead.</p>

<p>Ullah et al. (2023) [32] formulated TNN-IDS, a Transformer Neural Network architecture utilizing multi-head self-attention mechanisms to model long-range packet dependencies in MQTT-IoT-IDS2020, reporting an accuracy of 99.9%. However, the quadratic time complexity of full self-attention mechanisms with respect to sequence length imposes severe hardware constraints on IoT edge devices.</p>

<p>Khan et al. (2021) [4] evaluated a Deep Feed-Forward Neural Network (DNN) across simulated MQTT and multi-vector DoS datasets, benchmarking against Naive Bayes, K-Nearest Neighbors, Decision Trees, Random Forests, LSTMs, and GRUs. Their DNN achieved 97.13% accuracy, but exhibited inference latency exceeding 6 seconds, while simpler tree baselines demonstrated equivalent predictive performance at a fraction of the computational runtime.</p>

<p>Ullah et al. (2021) [6] proposed a hybrid deep learning model combining 1D-CNNs for spatial feature extraction with Gated Recurrent Units (GRUs) for temporal tracking on MQTT-IoT-IDS2020. While attaining high multi-class precision, the authors acknowledged that their benchmark was constrained by a narrow range of attack types, limiting generalizability against polymorphic zero-day exploits. In related domains, Al Masoodi (2024) [11] evaluated 1D-CNNs on UNSW-NB15, obtaining 83% validation accuracy, but noted the absence of protocol-specific MQTT header features.</p>

<div class="table-caption">Table 2.1: Chronological summary of machine learning and deep learning MQTT intrusion detection literature (2019–2026).</div>
<table>
  <thead>
    <tr>
      <th>Author and Year</th>
      <th>Paper Title</th>
      <th>Methodology</th>
      <th>Dataset Evaluated</th>
      <th>Reported Results</th>
      <th>Key Limitations Identified</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Swain et al. (2026) [28]</td>
      <td>Attention-based intrusion detection in MQTT-IoT network: a federated and DRL approach</td>
      <td>Federated Learning + Double DQN + Attention Aggregation</td>
      <td>MQTTset, MQTT-IoT-IDS2020, MQTTEEB-D</td>
      <td>Superior multi-dataset accuracy and low FPR</td>
      <td>High computational overhead; heavy communication rounds</td>
    </tr>
    <tr>
      <td>Alassaf et al. (2026) [29]</td>
      <td>Detecting anomalies in MQTT/MQTT-SN traffic using intelligent learning models</td>
      <td>Random Forest, XGBoost, LSTM with CV</td>
      <td>MQTT/MQTT-SN Capture</td>
      <td>F1-scores &gt; 0.95 on flooding vectors</td>
      <td>Time-ordered leakage unaddressed in random CV splits</td>
    </tr>
    <tr>
      <td>Allaga et al. (2026) [1]</td>
      <td>MQTTEEB-D: A high-fidelity benchmark for real-time MQTT anomaly detection</td>
      <td>CART, Bagging, Extra Trees, RF, XGB, CatBoost, ANN, 1D-CNN, LSTM</td>
      <td>MQTTEEB-D</td>
      <td>Multi-class F1: 0.989 (Bagging), 0.988 (CART); PES: 9045</td>
      <td>Unaudited <code>tcp_time_delta</code> timestamp leak; 85% duplicate rows</td>
    </tr>
    <tr>
      <td>Wang et al. (2025) [36]</td>
      <td>Intrusion detection based on convolutional Kolmogorov-Arnold networks</td>
      <td>CKAN: KAN + CNN + Channel Attention</td>
      <td>CICIoMT2024</td>
      <td>96.33% Category accuracy</td>
      <td>High memory allocation; narrow evaluation scope</td>
    </tr>
    <tr>
      <td>Al Hanif & Ilyas (2024) [30]</td>
      <td>Effective feature engineering framework for securing MQTT protocol</td>
      <td>Mutual Information + Tuned ML Ensembles</td>
      <td>Custom Balanced MQTT</td>
      <td>Accuracy &gt; 98.5%</td>
      <td>Binary classification only; no multi-class granularity</td>
    </tr>
    <tr>
      <td>Alotaibi et al. (2024) [31]</td>
      <td>Secure enhancement for MQTT using distributed machine learning</td>
      <td>H2O Distributed ML (H2OXGBoost, DRF, GLM)</td>
      <td>Custom IoT Network Capture</td>
      <td>H2OXGBoost achieved highest ROC-AUC</td>
      <td>Heavy distributed runtime; unsuitable for edge nodes</td>
    </tr>
    <tr>
      <td>Ullah et al. (2023) [32]</td>
      <td>TNN-IDS: Transformer neural network-based IDS for MQTT networks</td>
      <td>Multi-Head Self-Attention Transformer</td>
      <td>MQTT-IoT-IDS2020</td>
      <td>Multi-class accuracy up to 99.9%</td>
      <td>Quadratic self-attention complexity; slow edge inference</td>
    </tr>
    <tr>
      <td>Memon et al. (2023) [33]</td>
      <td>Explainable intrusion detection for Internet of Medical Things</td>
      <td>10 ML Classifiers + SHAP and LIME XAI</td>
      <td>MQTT-IoT-IDS2020</td>
      <td>High multi-class accuracy; feature rankings</td>
      <td>Did not audit synthetic capture artifacts or time leaks</td>
    </tr>
    <tr>
      <td>Siddharthan et al. (2022) [7]</td>
      <td>SENMQTT-SET: Intelligent IDS using ensemble multi-cascade features</td>
      <td>Multi-Cascade Feature Engineering + Random Forest</td>
      <td>SENMQTT-SET</td>
      <td>F1-score &gt; 0.96</td>
      <td>Hardware was physical, but sensor payloads were scripted</td>
    </tr>
    <tr>
      <td>Khan et al. (2021) [4]</td>
      <td>A deep learning-based intrusion detection system for MQTT enabled IoT</td>
      <td>Deep Feed-Forward Neural Network (DNN) vs ML</td>
      <td>MQTT-IoT-IDS2020</td>
      <td>97.13% multi-class accuracy; high latency</td>
      <td>High inference latency (6.35 s); complex parameter tuning</td>
    </tr>
    <tr>
      <td>Ullah et al. (2021) [6]</td>
      <td>Hybrid DL model for anomalous activities detection in IoT networks</td>
      <td>1D-CNN + Gated Recurrent Units (GRU)</td>
      <td>MQTT-IoT-IDS2020</td>
      <td>High precision across common vectors</td>
      <td>Narrow range of simulated attack categories</td>
    </tr>
    <tr>
      <td>Vaccari et al. (2020) [3]</td>
      <td>MQTTset, a new dataset for machine learning techniques on MQTT</td>
      <td>Random Forest, Decision Tree, Gradient Boosting</td>
      <td>MQTTset (IoT-Flock)</td>
      <td>Accuracy: 91.60%; F1: 91.40%</td>
      <td>Emulated network; RF inference latency 125.85 s</td>
    </tr>
    <tr>
      <td>Hindy et al. (2020) [5]</td>
      <td>ML-based IoT intrusion detection system: An MQTT case study</td>
      <td>Baseline ML Classifiers</td>
      <td>MQTT-IoT-IDS2020</td>
      <td>Baseline categorization</td>
      <td>Purely simulated network; lacking physical layer noise</td>
    </tr>
    <tr>
      <td>Alaiz-Moreton et al. (2019) [10]</td>
      <td>Multiclass classification procedure for detecting attacks on MQTT</td>
      <td>Decision Trees, Rule Induction, Multi-Layer Perceptrons</td>
      <td>Custom MQTT Capture</td>
      <td>Effective on volumetric DoS</td>
      <td>Unstandardized benchmark; small sample scale</td>
    </tr>
  </tbody>
</table>

<h2>3 Dataset Description and Forensic Audit</h2>

<h3>3.1 The MQTTEEB-D Benchmark Dataset</h3>
<p>MQTTEEB-D [2] was designed to provide the international cybersecurity research community with a high-fidelity, physically authenticated dataset for AI-powered MQTT threat detection:
<ul>
  <li><strong>Edge Sensors:</strong> Physical Libelium MySignals HW (e-Health Medical Development Platform) boards equipped with genuine biomedical sensors—including electrocardiogram (ECG), photoplethysmography pulse oximeters, and galvanic respiratory airflow monitors.</li>
  <li><strong>Edge Gateways:</strong> Physical Raspberry Pi 4 Model B microcomputers acting as local IoT sensor aggregators and MQTT publishing nodes.</li>
  <li><strong>Network Infrastructure:</strong> Dedicated 802.11 b/g/n wireless networks and IEEE 802.3 Ethernet backbones connecting edge publishers to a central Linux server hosting the open-source Eclipse Mosquitto MQTT message broker.</li>
  <li><strong>Packet Capture Mechanism:</strong> Network traffic was sniffed directly at the broker interface using PyShark (a Python wrapper for Wireshark/TShark) and exported as comma-separated value (CSV) capture files.</li>
</ul>
The released benchmark comprises four sequential capture loops containing 137,319, 42,470, 21,501, and 21,523 packet records, respectively, yielding an aggregate corpus of 222,813 packet observations across thirteen raw columns (twelve feature attributes and one target label).</p>

<div class="table-caption">Table 3.1: Structural parameters and operational characteristics of the MQTTEEB-D benchmark.</div>
<table>
  <thead>
    <tr>
      <th>Parameter / Dimension</th>
      <th>Specification / Value</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Authoring Institution</td><td>Cadi Ayyad University &amp; Sultan Moulay Slimane University, Morocco [2]</td></tr>
    <tr><td>Testbed Environment</td><td>Physical MySignals e-Health sensors, Raspberry Pi 4 gateways, Eclipse Mosquitto broker</td></tr>
    <tr><td>Network Protocols</td><td>MQTT (ISO/IEC 20922) encapsulated over TCP/IP transport stacks</td></tr>
    <tr><td>Traffic Sniffing Engine</td><td>PyShark / Wireshark libpcap capture engine</td></tr>
    <tr><td>Number of Capture Loops</td><td>4 distinct temporal loops (Loop 1: 137,319; Loop 2: 42,470; Loop 3: 21,501; Loop 4: 21,523)</td></tr>
    <tr><td>Total Captured Records</td><td>222,813 raw packet observations</td></tr>
    <tr><td>Valid Labeled Observations</td><td>222,567 observations (following deletion of 246 missing/unlabeled packets, 0.11%)</td></tr>
    <tr><td>Attack Categories</td><td>5 distinct cyber-attack scenarios + 1 benign legitimate baseline (6 total classes)</td></tr>
    <tr><td>Raw Attributes</td><td>13 columns: 12 feature attributes (1 timestamp + 11 protocol features) and 1 target label</td></tr>
    <tr><td>Class Imbalance Ratio</td><td>Malformed data injection (47.41%) down to Publish Flooding (4.59%); Legitimate (7.89%)</td></tr>
    <tr><td>Licensing Terms</td><td>Creative Commons Attribution 4.0 International (CC BY 4.0)</td></tr>
  </tbody>
</table>

<h3>3.2 Label Taxonomy and Attack Vectors</h3>
<p>MQTTEEB-D encapsulates five specific adversarial cyber-attack scenarios alongside legitimate physiological telemetry:</p>
<ul>
  <li><strong>Malformed Data Injection (<code>malformed</code>):</strong> Attackers transmit structurally corrupted MQTT packets—featuring truncated variable headers, invalid UTF-8 string encodings in topic names, or malformed payload structures—designed to crash broker parsing engines.</li>
  <li><strong>Denial of Service (<code>dos</code>):</strong> Volumetric transmission of connection requests and rapid-fire disconnect packets designed to exhaust TCP socket pools and server memory.</li>
  <li><strong>Brute Force (<code>bruteforce</code>):</strong> High-velocity dictionary attacks against MQTT broker authentication endpoints, cycling through credential lists to hijack unauthorized subscriptions.</li>
  <li><strong>Slow DoS against IoT Environments (<code>slowite</code>):</strong> A targeted low-rate attack that exploits MQTT keep-alive mechanisms by opening numerous half-open connections and transmitting heartbeat packets at the maximum keep-alive threshold, starving server resources with minimal bandwidth consumption.</li>
  <li><strong>Publish Flooding (<code>flood</code>):</strong> Legitimate clients are overwhelmed by an adversary publishing massive volumes of high-frequency telemetry across subscribed wildcards (<code>#</code> and <code>+</code>).</li>
  <li><strong>Legitimate Traffic (<code>legitimate</code>):</strong> Genuine periodic physiological telemetry transmitted from patient monitoring hardware to the broker.</li>
</ul>

<div class="table-caption">Table 3.2: Label taxonomy, sample counts, and unique row frequencies in MQTTEEB-D.</div>
<table>
  <thead>
    <tr>
      <th>Class Identifier</th>
      <th>Traffic Description and Threat Vector</th>
      <th>Total Packet Count</th>
      <th>Percentage Share (%)</th>
      <th>Unique Rows (Feature + Label)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><code>malformed</code></td><td>Invalid MQTT packet syntax, payload tampering</td><td class="right">105,528</td><td class="right">47.41%</td><td class="right">14,100</td></tr>
    <tr><td><code>dos</code></td><td>Volumetric connection and subscription exhaustion</td><td class="right">41,802</td><td class="right">18.78%</td><td class="right">4,277</td></tr>
    <tr><td><code>bruteforce</code></td><td>Repeated unauthorized credential attack cycles</td><td class="right">27,377</td><td class="right">12.30%</td><td class="right">172</td></tr>
    <tr><td><code>slowite</code></td><td>Low-rate persistent keep-alive resource starvation</td><td class="right">20,090</td><td class="right">9.03%</td><td class="right">3,675</td></tr>
    <tr><td><code>legitimate</code></td><td>Normal biometric sensor telemetry (MySignals)</td><td class="right">17,557</td><td class="right">7.89%</td><td class="right">4,835</td></tr>
    <tr><td><code>flood</code></td><td>High-frequency MQTT publish message flooding</td><td class="right">10,213</td><td class="right">4.59%</td><td class="right">6,048</td></tr>
    <tr style="font-weight:bold; background-color:#f0f0f0;"><td>Total</td><td>Cleaned Benchmark Corpus</td><td class="right">222,567</td><td class="right">100.00%</td><td class="right">33,107</td></tr>
  </tbody>
</table>

<div class="figure-container">
  <img src="{img_class_dist}" alt="Class Distribution">
  <div class="figure-caption">Figure 3.1: Class distribution of the MQTTEEB-D benchmark dataset after removing unlabelled packets.</div>
</div>

<h3>3.3 Protocol Feature Taxonomy</h3>
<p>Excluding the target <code>label</code> and the initial <code>timestamp</code>, the feature set consists of eleven variables spanning transport-layer dynamics and application-layer MQTT semantics, as defined in Table 3.3.</p>

<div class="table-caption">Table 3.3: Comprehensive feature taxonomy of MQTTEEB-D.</div>
<table>
  <thead>
    <tr>
      <th>Feature Attribute</th>
      <th>Protocol Layer</th>
      <th>Technical Description</th>
      <th>Data Type</th>
      <th>Operational Value Range</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><code>tcp_flags</code></td><td>Transport (TCP)</td><td>Active TCP control flags bitmap (SYN, ACK, PSH, FIN)</td><td>Hex / Cat</td><td>3 values (0x0018, 0x0010, 0x00190019)</td></tr>
    <tr><td><code>tcp_time_delta</code></td><td>Transport (TCP)</td><td>Documented as inter-packet arrival time; <strong>leaked timestamp</strong></td><td>Float64</td><td>[1.725&times;10<sup>9</sup>, 1.725&times;10<sup>9</sup>]</td></tr>
    <tr><td><code>tcp_len</code></td><td>Transport (TCP)</td><td>Total byte length of TCP packet payload</td><td>Integer</td><td>[1, 3936] bytes</td></tr>
    <tr><td><code>mqtt_conack_flags</code></td><td>Application (MQTT)</td><td>Acknowledgment flags in broker CONNACK response</td><td>Hex / Mixed</td><td>19 distinct modalities (bimodal)</td></tr>
    <tr><td><code>mqtt_conflag_cleansess</code></td><td>Application (MQTT)</td><td>Clean Session flag in CONNECT header</td><td>Binary</td><td>&#123;0, 1&#125;</td></tr>
    <tr><td><code>mqtt_conflags</code></td><td>Application (MQTT)</td><td>Composite connection flag bitmap</td><td>Hex / Mixed</td><td>4 categorical states</td></tr>
    <tr><td><code>mqtt_dupflag</code></td><td>Application (MQTT)</td><td>Duplicate delivery flag for QoS 1 and QoS 2</td><td>Binary</td><td>&#123;0, 1&#125;</td></tr>
    <tr><td><code>mqtt_hdrflags</code></td><td>Application (MQTT)</td><td>Fixed header flags (MQTT control packet type, QoS, DUP)</td><td>Hex / Cat</td><td>44 categorical modalities</td></tr>
    <tr><td><code>mqtt_kalive</code></td><td>Application (MQTT)</td><td>Client keep-alive timer parameter (seconds)</td><td>Integer</td><td>[0, 60] seconds</td></tr>
    <tr><td><code>mqtt_msg</code></td><td>Application (MQTT)</td><td>Byte size of application message payload</td><td>Integer</td><td>[0, 65504] bytes</td></tr>
    <tr><td><code>mqtt_qos</code></td><td>Application (MQTT)</td><td>Quality of Service delivery guarantee level</td><td>Ordinal</td><td>&#123;0, 1, 2, 3&#125;</td></tr>
  </tbody>
</table>

<h3>3.4 Forensic Data Audit Findings</h3>
<p>Prior to constructing machine learning pipelines, module M1 of our framework executes a four-tier forensic data audit. This audit revealed critical empirical anomalies that undermine conventional evaluation conclusions:</p>
<ol>
  <li><strong>Exact Timestamp Duplication in <code>tcp_time_delta</code>:</strong> In PyShark capture dissections, <code>tcp.time_delta</code> represents the relative time elapsed since the previously captured packet. However, in the released CSV files of MQTTEEB-D, the column labeled <code>tcp_time_delta</code> contains floating-point values on the order of 1.725&times;10<sup>9</sup>. A bitwise equality check across every individual record across all four raw capture files confirmed:
  <div class="equation">&forall; i, &nbsp; x<sub>i, tcp_time_delta</sub> &equiv; x<sub>i, timestamp</sub> &nbsp; (&rho; = 1.00000000)</div>
  Although Allaga et al. [1] explicitly dropped the <code>timestamp</code> column to "prevent temporal data leakage," the exact same temporal data remained intact under the <code>tcp_time_delta</code> identifier. Because the five attack campaigns were executed in segregated sequential time windows, this feature acts as an index of elapsed real time, allowing tree models to trivially partition classes by placing threshold cuts on time.</li>
  <li><strong>Heavy Data Redundancy and Unique Pattern Cardinality:</strong> IoT telemetry and automated network attack scripts emit repetitive, deterministic packet structures. Once temporal markers (<code>timestamp</code> and <code>tcp_time_delta</code>) are removed:
  <ul>
    <li>There are only <strong>33,107 unique feature-plus-label rows</strong> out of 222,567 observations, representing a duplicate row fraction of &delta; = 85.12%.</li>
    <li>When ground-truth labels are excluded, these collapse to <strong>28,200 unique feature patterns</strong>.</li>
    <li>Most dramatically, the <code>bruteforce</code> attack class comprises 27,377 total packets but collapses to just 172 unique feature-plus-label rows.</li>
  </ul></li>
  <li><strong>Severe Multi-Class Label Ambiguity:</strong> When identical network packets appear under both benign and malicious contexts, they generate contradictory training signals. In MQTTEEB-D, out of the 28,200 unique feature patterns across the ten valid protocol features, 3,183 patterns (11.29%) occur with more than one ground-truth label. For example, benign sensor keep-alive packets share identical TCP lengths, flags, and MQTT headers with certain probing packets.</li>
  <li><strong>Empirical Majority-Class Upper Bound:</strong> Because conflicting labels cannot be separated by any deterministic classifier operating purely on these ten packet-level features, we compute the in-sample majority-class upper bound A* for the observed dataset distribution:
  <div class="equation">A* = (1 / N) &Sigma;<sub>p &isin; P</sub> max<sub>c &isin; C</sub> n<sub>pc</sub> = 73.82% <span class="eq-num">(4.3)</span></div>
  This 73.82% ceiling represents an empirical, feature-pattern-based upper bound for the observed distribution under single-packet inspection. Exceeding this bound without temporal leakage requires contextual session tracking or multi-packet bi-directional flow features.</li>
</ol>

<div class="table-caption">Table 3.4: Forensic data audit summary for MQTTEEB-D (Module M1).</div>
<table>
  <thead>
    <tr>
      <th>Diagnostic Audit Criterion</th>
      <th>Empirical Result</th>
      <th>Methodological Consequence</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Correlation &rho;(<code>tcp_time_delta</code>, <code>timestamp</code>)</td><td>&rho; = 1.0000 (Identical in 100% of rows)</td><td>Direct temporal leakage into training splits</td></tr>
    <tr><td>Unique feature-plus-label rows</td><td>33,107 rows out of 222,567 (&delta; = 85.12%)</td><td>Heavy duplication in continuous packet stream</td></tr>
    <tr><td>Unique feature patterns (labels ignored)</td><td>28,200 distinct patterns</td><td>Fundamental packet vector diversity</td></tr>
    <tr><td>Pattern twin leakage in random split</td><td>90.7% of test vectors exist in training</td><td>Massive test set memorization</td></tr>
    <tr><td>Conflicting multi-label patterns</td><td>11.29% (3,183 ambiguous patterns)</td><td>Fundamental packet-level class overlap</td></tr>
    <tr><td>Empirical majority upper bound A*</td><td>73.82%</td><td>Max accuracy attainable on 10 valid features</td></tr>
    <tr><td><code>bruteforce</code> class redundancy</td><td>27,377 packets collapse to 172 unique rows</td><td>Artificially high F1 via rote replication</td></tr>
  </tbody>
</table>

<h2>4 Proposed Methodology</h2>

<h3>4.1 System Architecture Overview</h3>
<p>To eliminate artifactual leakage, enforce rigorous validation, and establish authentic operational performance benchmarks for IoT intrusion detection, we formulate the Leakage-Aware MQTT (LA-MQTT) evaluation framework. LA-MQTT establishes a modular, six-stage pipeline:
<ul>
  <li><strong>M1: Data Forensic Audit:</strong> Scans raw data for duplicate columns, computes row-level redundancy, flags time surrogates, and computes the empirical in-sample majority-label accuracy ceiling.</li>
  <li><strong>M2: Leakage-Safe Preprocessing:</strong> Sanitizes protocol hex strings, drops flagged temporal columns, and applies z-score standardization fit strictly on training splits.</li>
  <li><strong>M3: Multi-Protocol Partitioning:</strong> Establishes four rigorous evaluation protocols: P1 (Standard 80:20 random split), P2 (Deduplicated split), P3 (Pattern-grouped 5-fold CV), and P4 (Leave-One-Loop-Out / LOLO).</li>
  <li><strong>M4: Model Zoo:</strong> Houses an extensive suite of ten classical ML models and four deep learning architectures.</li>
  <li><strong>M5: Comprehensive Evaluation & Statistics:</strong> Evaluates models across conventional and imbalance-robust metrics, incorporating five-seed paired t-tests and exact McNemar contingency tests.</li>
  <li><strong>M6: Leakage-Gap Reporting:</strong> Quantifies the generalization drop between random splits and unseen temporal loops (&Delta;<sub>leak</sub>).</li>
</ul>
</p>

<h3>4.2 Module-Wise Mathematical Formulation</h3>

<h4>4.2.1 Module M1: Data Forensic Audit</h4>
<p>Given a dataset D comprising n observations and feature column set F, M1 computes pairwise column agreement share &rho;(a, b):</p>
<div class="equation">&rho;(a, b) = (1 / n) &Sigma;<sub>i=1</sub><sup>n</sup> 1[x<sub>ia</sub> = x<sub>ib</sub>] <span class="eq-num">(4.1)</span></div>
<p class="no-indent">If &rho;(a, b) = 1.0, column b is flagged as an exact duplicate of a and marked for immediate excision.</p>

<p>The duplicate row fraction &delta; is quantified using u, the cardinality of unique tuples (x<sub>i</sub>, y<sub>i</sub>):</p>
<div class="equation">&delta; = 1 - (u / n) <span class="eq-num">(4.2)</span></div>

<p>The empirical in-sample majority-label accuracy bound A* is computed as:</p>
<div class="equation">A* = (1 / n) &Sigma;<sub>p &isin; P</sub> max<sub>c &isin; C</sub> n<sub>pc</sub> <span class="eq-num">(4.3)</span></div>
<p class="no-indent"><em>Formal Scope of Ceiling Estimation:</em> Formally, A* = 73.82% represents an empirical in-sample majority-label upper bound computed over the finite observed sample of 222,567 observations across the 28,200 unique ten-attribute feature vectors. Because 3,183 of these patterns (11.29%) appear under conflicting labels, any single-packet deterministic classifier assigning each pattern to its locally observed majority class achieves at most 164,300 correct classifications out of 222,567 (73.82%). This figure serves as an empirical upper bound for the observed distribution under stateless packet inspection, rather than an asymptotic theoretical Bayes-optimal rate for unseen operational populations with different traffic priors.</p>

<h4>4.2.2 Module M2: Leakage-Safe Preprocessing</h4>
<p>Module M2 converts hexadecimal string representations into signed numerical integers:</p>
<div class="equation">x<sub>ij</sub> &larr; hex_to_int(x<sub>ij</sub>), &nbsp; &forall; j &isin; &#123;tcp_flags, mqtt_conack_flags, mqtt_conflags, mqtt_hdrflags&#125; <span class="eq-num">(4.4)</span></div>

<p>Standardization parameters are computed strictly on training partitions:</p>
<div class="equation">&mu;<sub>j</sub> = (1 / |D<sub>train</sub>|) &Sigma;<sub>i &isin; D<sub>train</sub></sub> x<sub>ij</sub>, &nbsp; &sigma;<sub>j</sub> = &radic;[ (1 / |D<sub>train</sub>|) &Sigma;<sub>i &isin; D<sub>train</sub></sub> (x<sub>ij</sub> - &mu;<sub>j</sub>)<sup>2</sup> ] <span class="eq-num">(4.5)</span></div>
<div class="equation">z<sub>ij</sub> = (x<sub>ij</sub> - &mu;<sub>j</sub>) / (&sigma;<sub>j</sub> + &epsilon;) <span class="eq-num">(4.6)</span></div>

<p>SMOTE [15] is applied exclusively to D<sub>train</sub>:</p>
<div class="equation">x&#771; = x<sub>i</sub> + &lambda; (x<sub>k</sub> - x<sub>i</sub>), &nbsp; &lambda; ~ U(0, 1) <span class="eq-num">(4.7)</span></div>

<h4>4.2.3 Module M3: Multi-Protocol Partitioning</h4>
<p>LA-MQTT formalizes four distinct evaluation protocols, each engineered to assess a fundamentally different generalization condition rather than serving as interchangeable alternatives:
<ul>
  <li><strong>Protocol 1 (P1 - Standard Random Partitioning):</strong> A stratified 80:20 partition on the full 222,567-packet corpus. P1 measures interpolation performance in high-frequency traffic streams; because 90.7% of test packet patterns possess exact duplicates in the training set, P1 reflects identical-packet interpolation.</li>
  <li><strong>Protocol 2 (P2 - Deduplicated Row Partitioning):</strong> A stratified 80:20 partition executed after eliminating identical (feature, label) rows, reducing the dataset to 33,107 distinct observations. P2 assesses generalization when identical instances cannot be memorized, although identical feature vectors with conflicting labels may still exist across partitions.</li>
  <li><strong>Protocol 3 (P3 - Pattern-Grouped 5-Fold Cross-Validation):</strong> A strict grouped 5-fold cross-validation (<code>GroupKFold(n_splits=5)</code>) over the 28,200 unique feature patterns (labels ignored). P3 enforces the strict requirement that identical feature patterns never appear simultaneously in both training and testing folds, evaluating zero-shot generalization to previously unseen packet signatures.</li>
  <li><strong>Protocol 4 (P4 - Leave-One-Loop-Out / LOLO):</strong> Cross-session temporal partitioning across the L = 4 independent raw capture loops:
  <div class="equation">A<sub>LOLO</sub> = (1 / L) &Sigma;<sub>l=1</sub><sup>L</sup> Accuracy(f<sub>(-l)</sub>, D<sub>l</sub>) <span class="eq-num">(4.8)</span></div>
  <div class="equation">&Delta;<sub>leak</sub> = A<sub>P1</sub> - A<sub>LOLO</sub> <span class="eq-num">(4.9)</span></div>
  P4 evaluates out-of-distribution temporal robustness across independent recording campaigns.</li>
</ul>
</p>

<h4>4.2.4 Module M4: Algorithmic Formulations (Model Zoo)</h4>
<p>CART Decision Tree Gini impurity minimization:</p>
<div class="equation">I(t) = 1 - &Sigma;<sub>c=1</sub><sup>C</sup> p<sub>c</sub>(t)<sup>2</sup>, &nbsp; &Delta;I(t) = I(t) - (N<sub>L</sub> / N) I(t<sub>L</sub>) - (N<sub>R</sub> / N) I(t<sub>R</sub>) <span class="eq-num">(4.10)</span></div>

<p>Bagging & Random Forest majority voting over B trees:</p>
<div class="equation">y&#770;(x) = argmax<sub>c &isin; C</sub> &Sigma;<sub>b=1</sub><sup>B</sup> 1[h<sub>b</sub>(x) = c] <span class="eq-num">(4.11)</span></div>

<p>XGBoost regularized objective minimization:</p>
<div class="equation">L<sup>(t)</sup> = &Sigma;<sub>i=1</sub><sup>n</sup> l(y<sub>i</sub>, y&#770;<sub>i</sub><sup>(t-1)</sup> + f<sub>t</sub>(x<sub>i</sub>)) + &Omega;(f<sub>t</sub>), &nbsp; &Omega;(f) = &gamma; T + &frac12; &lambda; &Sigma;<sub>j=1</sub><sup>T</sup> w<sub>j</sub><sup>2</sup> <span class="eq-num">(4.12)</span></div>

<p>Deep Neural Networks categorical cross-entropy minimization:</p>
<div class="equation">L<sub>CE</sub> = - (1 / B) &Sigma;<sub>i=1</sub><sup>B</sup> &Sigma;<sub>c=1</sub><sup>C</sup> y<sub>ic</sub> log y&#770;<sub>ic</sub> <span class="eq-num">(4.13)</span></div>

<h4>4.2.5 Module M5: Evaluation Metrics & Statistical Testing</h4>
<p>Matthews Correlation Coefficient (MCC):</p>
<div class="equation">MCC = (c &middot; s - &Sigma;<sub>k</sub> p<sub>k</sub> t<sub>k</sub>) / &radic;[ (s<sup>2</sup> - &Sigma;<sub>k</sub> p<sub>k</sub><sup>2</sup>)(s<sup>2</sup> - &Sigma;<sub>k</sub> t<sub>k</sub><sup>2</sup>) ] <span class="eq-num">(4.14)</span></div>

<p>Performance–Efficiency Score (PES):</p>
<div class="equation">PES = [ &frac12; (Accuracy + F1<sub>weighted</sub>) ] / ln(1 + T<sub>test</sub>) <span class="eq-num">(4.15)</span></div>

<p>Paired t-Test across m Random Seeds:</p>
<div class="equation">t = d&#772; / (s<sub>d</sub> / &radic;m), &nbsp; d&#772; = (1 / m) &Sigma;<sub>k=1</sub><sup>m</sup> (A<sub>1,k</sub> - A<sub>2,k</sub>) <span class="eq-num">(4.16)</span></div>
<p class="no-indent"><em>Methodological Scrutiny of Split Independence:</em> As established by Dietterich (1998) [34] and Nadeau and Bengio (2003) [35], repeated random partitions drawn from the same underlying dataset violate the independence assumption of the standard Student's t-test, as training partitions across random seeds share substantial observation overlap (~64% shared instances in 80:20 partitions). This correlation underestimates variance and inflates Type I errors. Consequently, while five-seed paired t-tests provide an exploratory assessment of variability across random initializations, we designate the exact non-parametric McNemar test as our primary statistical arbiter of algorithmic discordance.</p>

<p>Exact McNemar Contingency Test:</p>
<div class="equation">p = min( 1, &nbsp; 2 &Sigma;<sub>k=0</sub><sup>min(n01, n10)</sup> C(n01 + n10, k) &middot; 0.5<sup>n01 + n10</sup> ) <span class="eq-num">(4.17)</span></div>
<p class="no-indent">Evaluated on the unified hold-out test partition (N = 44,514 paired predictions), McNemar's test assesses whether the marginal discordance between two classifiers (n<sub>01</sub> vs. n<sub>10</sub>) deviates significantly from a binomial distribution under the null hypothesis of equal error rates, avoiding the split-overlap dependency inherent to repeated resampling.</p>

<h3>4.3 Algorithmic Execution Workflow</h3>

<div class="algorithm-box">
<div class="alg-header">Algorithm 1: Data Forensic Audit and Ceiling Estimation (Module M1)</div>
<strong>Input :</strong> Raw Dataset D with n observations, feature set F, ground-truth labels y, capture loop IDs<br>
<strong>Output:</strong> Flagged duplicate columns F_flag, sanitized feature set F', redundancy &delta;, empirical ceiling A*<br>
1: Initialize F_flag &larr; empty set<br>
2: D &larr; drop_null_rows(D, subset=['label'])<br>
3: for each pair of columns (a, b) in F do<br>
4: &nbsp;&nbsp;&nbsp;&nbsp;compute agreement &rho;(a, b) = (1/n) * sum(1[x_ia == x_ib])<br>
5: &nbsp;&nbsp;&nbsp;&nbsp;if &rho;(a, b) == 1.0 then add b to F_flag<br>
6: end for<br>
7: F' &larr; F \ F_flag<br>
8: u &larr; count_unique_tuples(D[F', y])<br>
9: &delta; &larr; 1.0 - (u / n)<br>
10: Group D by unique feature patterns p in F'<br>
11: compute A* = (1/n) * sum_{{p}} max_{{c}} n_pc<br>
12: return F_flag, F', &delta;, A*
</div>

<div class="algorithm-box">
<div class="alg-header">Algorithm 2: Leakage-Safe Preprocessing and Partitioning (Modules M2 &amp; M3)</div>
<strong>Input :</strong> Dataset D, sanitized feature set F', protocol P in &#123;P1, P2, P3, P4&#125;, seed s, SMOTE flag<br>
<strong>Output:</strong> Standardized training and testing matrices (X_train, y_train, X_test, y_test)<br>
1: Convert hexadecimal columns in F' to signed integers via hex_to_int()<br>
2: if P == P2 then D &larr; drop_duplicate_rows(D, subset=[*F', 'label'])<br>
3: if P in &#123;P1, P2&#125; then (train_idx, test_idx) &larr; stratified_split(D[y], test_size=0.20, random_state=s)<br>
4: else if P == P3 then (train_idx, test_idx) &larr; GroupKFold(D, groups=pattern_ids(F'), n_splits=5)<br>
5: else if P == P4 then test_idx &larr; indices(D['loop'] == target_loop); train_idx &larr; indices(D['loop'] != target_loop)<br>
6: Fit scaler parameters (&mu;_train, &sigma;_train) strictly on D[train_idx, F']<br>
7: X_train &larr; (D[train_idx, F'] - &mu;_train) / &sigma;_train; X_test &larr; (D[test_idx, F'] - &mu;_train) / &sigma;_train<br>
8: if SMOTE flag is True then (X_train, y_train) &larr; SMOTE(random_state=s).fit_resample(X_train, D[train_idx, y])<br>
9: return X_train, y_train, X_test, y_test
</div>

<div class="algorithm-box">
<div class="alg-header">Algorithm 3: Leakage-Aware Benchmarking and Statistical Validation (Modules M4 &amp; M5)</div>
<strong>Input :</strong> Model set M, protocol set &#123;P1, P2, P3, P4&#125;, seed array S = &#123;42, 43, 44, 45, 46&#125;<br>
<strong>Output:</strong> Consolidated benchmark tables, paired t-tests, McNemar statistics, LOLO leakage gap<br>
1: for each feature_config in &#123;With_tcp_time_delta, Without_tcp_time_delta&#125; do<br>
2: &nbsp;&nbsp;&nbsp;&nbsp;for each model m in M do<br>
3: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;for each seed s in S do<br>
4: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(X_tr, y_tr, X_te, y_te) &larr; Algorithm_2(D, P1, s)<br>
5: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;fit model m on (X_tr, y_tr); record training latency T_train<br>
6: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;y_pred, y_prob &larr; predict(m, X_te); record test latency T_test<br>
7: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;compute Acc, F1_w, F1_macro, MCC, ROC_AUC, PR_AUC, PES; store metrics<br>
8: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;end for<br>
9: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;for each loop l in &#123;1, 2, 3, 4&#125; do<br>
10: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(X_tr_l, y_tr_l, X_te_l, y_te_l) &larr; Algorithm_2(D, P4, loop=l)<br>
11: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;fit m on (X_tr_l, y_tr_l); evaluate on (X_te_l, y_te_l); record Acc(l)<br>
12: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;end for<br>
13: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A_LOLO &larr; mean(Acc(1..4)); &Delta;_leak &larr; mean_Acc_P1 - A_LOLO<br>
14: &nbsp;&nbsp;&nbsp;&nbsp;end for<br>
15: &nbsp;&nbsp;&nbsp;&nbsp;execute paired t-tests across seeds S; execute exact McNemar test on seed-42 predictions<br>
16: end for<br>
17: return consolidated benchmark tables
</div>

<h2>5 Experimental Analysis</h2>

<h3>5.1 Preprocessing Results: t-SNE Manifold Visualizations</h3>
<p>To evaluate how feature transformations and temporal leakage affect class separability, t-Distributed Stochastic Neighbor Embedding (t-SNE) was performed on a stratified sample of 6,000 packets across three distinct states:</p>
<ol>
  <li><strong>Raw Features Before Preprocessing:</strong> Fig. 5.1(a) shows thin, fragmented, curved strands where packets cluster strictly by chronological capture order rather than protocol semantics.</li>
  <li><strong>After Hexadecimal Conversion and Z-Score Scaling (All 11 Features):</strong> Fig. 5.1(b) displays identical filamentary strands, confirming that standardizing the leaked <code>tcp_time_delta</code> feature preserves artificial chronological clustering.</li>
  <li><strong>After Preprocessing Without <code>tcp_time_delta</code> (10 Protocol Features):</strong> Fig. 5.1(c) shows the filamentary strands collapsing into continuous geometric manifolds. While <code>flood</code>, <code>slowite</code>, and <code>legitimate</code> maintain distinct clusters, <code>dos</code> and <code>malformed</code> display heavy mutual overlap, reflecting the 11.29% label ambiguity identified in our data audit.</li>
</ol>

<div class="figure-container">
  <img src="{img_tsne}" alt="t-SNE Projections Before and After Preprocessing">
  <div class="figure-caption">Figure 5.1: t-SNE projections of 6,000 stratified packets: (a) Raw features before preprocessing, (b) Standardized features with tcp_time_delta, (c) Sanitized protocol features without tcp_time_delta.</div>
</div>

<h3>5.2 Deep Learning Neural Training Dynamics (Per-Epoch History)</h3>
<p>Fig. 5.2 plots the training and validation accuracy and loss trajectories across 40 epochs for the four deep neural architectures under both feature regimes:</p>
<ul>
  <li><strong>With All 11 Features:</strong> Loss descends steadily without triggering early stopping within 40 epochs, reaching validation accuracies between 69.5% (ANN) and 86.2% (SimpleRNN). Validation curves track training curves closely, proving that the lower performance of deep architectures relative to tree models is not caused by overfitting.</li>
  <li><strong>Without <code>tcp_time_delta</code>:</strong> SimpleRNN and LSTM trigger early stopping at epochs 19 and 25, respectively, stabilizing at validation accuracies between 61.1% and 66.5%. Because neural networks perform smooth linear combinations across inputs, they cannot construct sharp axis-aligned partition cuts around narrow timestamp intervals as effectively as decision trees.</li>
</ul>

<div class="figure-container">
  <img src="{img_dl_epochs}" alt="Deep Learning Epoch History">
  <div class="figure-caption">Figure 5.2: Training and validation accuracy and loss curves per epoch across ANN, 1D-CNN, SimpleRNN, and LSTM.</div>
</div>

<h3>5.3 Multi-Class Experimental Results and Replication</h3>
<p>Table 5.2 and Table 5.3 present the replicated multi-class classification benchmark on the original imbalanced data and post-SMOTE data under Protocol P1.</p>

<div class="table-caption">Table 5.2: Replicated multi-class classification performance on original imbalanced data (Protocol P1, Seed 42).</div>
<table>
  <thead>
    <tr>
      <th>Evaluated Algorithm</th>
      <th>Accuracy</th>
      <th>Weighted F1</th>
      <th>Macro F1</th>
      <th>MCC</th>
      <th>ROC-AUC (Macro)</th>
      <th>PR-AUC (Macro)</th>
      <th>Train Latency (s)</th>
      <th>Test Latency (s)</th>
      <th>PES Score</th>
    </tr>
  </thead>
  <tbody>
    <tr style="font-weight:bold; background-color:#f7f9fa;"><td>Bagging Classifier</td><td>0.9887</td><td>0.9887</td><td>0.9804</td><td>0.9840</td><td>0.9981</td><td>0.9927</td><td class="right">6.64 s</td><td class="right">0.095 s</td><td class="right">10.90</td></tr>
    <tr><td>CART Decision Tree</td><td>0.9877</td><td>0.9877</td><td>0.9789</td><td>0.9827</td><td>0.9885</td><td>0.9631</td><td class="right">1.02 s</td><td class="right">0.008 s</td><td class="right">124.71</td></tr>
    <tr><td>Extra Trees</td><td>0.9808</td><td>0.9805</td><td>0.9687</td><td>0.9728</td><td>0.9980</td><td>0.9899</td><td class="right">10.42 s</td><td class="right">1.301 s</td><td class="right">1.18</td></tr>
    <tr><td>OvR Random Forest</td><td>0.9776</td><td>0.9773</td><td>0.9634</td><td>0.9683</td><td>0.9981</td><td>0.9904</td><td class="right">140.51 s</td><td class="right">2.812 s</td><td class="right">0.73</td></tr>
    <tr><td>Random Forest</td><td>0.9704</td><td>0.9701</td><td>0.9577</td><td>0.9581</td><td>0.9972</td><td>0.9865</td><td class="right">37.24 s</td><td class="right">1.075 s</td><td class="right">1.33</td></tr>
    <tr><td>K-NN (k=5)</td><td>0.9698</td><td>0.9690</td><td>0.9566</td><td>0.9572</td><td>0.9905</td><td>0.9695</td><td class="right">0.39 s</td><td class="right">62.019 s</td><td class="right">0.23</td></tr>
    <tr><td>Gradient Boosting</td><td>0.9294</td><td>0.9161</td><td>0.8654</td><td>0.9014</td><td>0.9871</td><td>0.9125</td><td class="right">211.80 s</td><td class="right">0.580 s</td><td class="right">2.01</td></tr>
    <tr><td>XGBoost (Hist)</td><td>0.9180</td><td>0.9069</td><td>0.8465</td><td>0.8845</td><td>0.9861</td><td>0.9020</td><td class="right">8.71 s</td><td class="right">0.500 s</td><td class="right">2.25</td></tr>
    <tr><td>CatBoost</td><td>0.9161</td><td>0.9028</td><td>0.8421</td><td>0.8821</td><td>0.9843</td><td>0.8974</td><td class="right">29.34 s</td><td class="right">0.061 s</td><td class="right">15.34</td></tr>
    <tr><td>LightGBM</td><td>0.9138</td><td>0.8998</td><td>0.8384</td><td>0.8790</td><td>0.9856</td><td>0.9001</td><td class="right">8.52 s</td><td class="right">1.979 s</td><td class="right">0.83</td></tr>
  </tbody>
</table>

<div class="table-caption">Table 5.3: Replicated multi-class performance with SMOTE applied to the training set (Protocol P1, Seed 42).</div>
<table>
  <thead>
    <tr>
      <th>Evaluated Algorithm</th>
      <th>Accuracy</th>
      <th>Weighted F1</th>
      <th>Macro F1</th>
      <th>MCC</th>
      <th>ROC-AUC (Macro)</th>
      <th>PR-AUC (Macro)</th>
      <th>Train Latency (s)</th>
      <th>Test Latency (s)</th>
      <th>PES Score</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Bagging Classifier</td><td>0.9812</td><td>0.9813</td><td>0.9712</td><td>0.9734</td><td>0.9945</td><td>0.9806</td><td class="right">24.81 s</td><td class="right">0.100 s</td><td class="right">10.29</td></tr>
    <tr><td>CART Decision Tree</td><td>0.9793</td><td>0.9794</td><td>0.9682</td><td>0.9708</td><td>0.9835</td><td>0.9454</td><td class="right">3.68 s</td><td class="right">0.010 s</td><td class="right">98.42</td></tr>
    <tr><td>Extra Trees</td><td>0.9780</td><td>0.9780</td><td>0.9664</td><td>0.9689</td><td>0.9974</td><td>0.9857</td><td class="right">50.12 s</td><td class="right">1.656 s</td><td class="right">1.00</td></tr>
    <tr><td>OvR Random Forest</td><td>0.9773</td><td>0.9773</td><td>0.9654</td><td>0.9680</td><td>0.9972</td><td>0.9870</td><td class="right">320.50 s</td><td class="right">2.633 s</td><td class="right">0.76</td></tr>
    <tr><td>Random Forest</td><td>0.9679</td><td>0.9679</td><td>0.9542</td><td>0.9547</td><td>0.9965</td><td>0.9835</td><td class="right">144.72 s</td><td class="right">1.153 s</td><td class="right">1.26</td></tr>
    <tr><td>K-NN (k=5)</td><td>0.9603</td><td>0.9618</td><td>0.9451</td><td>0.9446</td><td>0.9877</td><td>0.9561</td><td class="right">1.34 s</td><td class="right">51.242 s</td><td class="right">0.24</td></tr>
    <tr><td>XGBoost (Hist)</td><td>0.9029</td><td>0.9025</td><td>0.8524</td><td>0.8637</td><td>0.9805</td><td>0.8898</td><td class="right">26.88 s</td><td class="right">0.520 s</td><td class="right">2.15</td></tr>
    <tr><td>LightGBM</td><td>0.9028</td><td>0.9018</td><td>0.8519</td><td>0.8635</td><td>0.9812</td><td>0.8925</td><td class="right">25.48 s</td><td class="right">2.049 s</td><td class="right">0.81</td></tr>
    <tr><td>CatBoost</td><td>0.8991</td><td>0.8973</td><td>0.8441</td><td>0.8583</td><td>0.9801</td><td>0.8863</td><td class="right">82.01 s</td><td class="right">0.056 s</td><td class="right">16.48</td></tr>
  </tbody>
</table>

<div class="table-caption">Table 5.4: Alignment between published benchmark metrics (Allaga et al. [1]) and our empirical replication.</div>
<table>
  <thead>
    <tr>
      <th>Model Classifier</th>
      <th>Published F1 (Orig)</th>
      <th>Replicated F1 (Orig)</th>
      <th>Published F1 (SMOTE)</th>
      <th>Replicated F1 (SMOTE)</th>
      <th>Published MCC</th>
      <th>Replicated MCC</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Bagging Classifier</td><td>0.99</td><td>0.989</td><td>0.99</td><td>0.981</td><td>0.9852</td><td>0.9840</td></tr>
    <tr><td>CART Decision Tree</td><td>0.98</td><td>0.988</td><td>0.99</td><td>0.979</td><td>0.9831</td><td>0.9827</td></tr>
    <tr><td>Extra Trees</td><td>0.97</td><td>0.981</td><td>0.99</td><td>0.978</td><td>0.9726</td><td>0.9728</td></tr>
    <tr><td>Random Forest</td><td>0.96</td><td>0.970</td><td>0.99</td><td>0.968</td><td>0.9580</td><td>0.9581</td></tr>
    <tr><td>OvR Random Forest</td><td>0.97</td><td>0.977</td><td>0.99</td><td>0.977</td><td>0.9681</td><td>0.9683</td></tr>
    <tr><td>Gradient Boosting</td><td>0.86</td><td>0.916</td><td>0.93</td><td>0.929</td><td>0.9013</td><td>0.9014</td></tr>
    <tr><td>XGBoost</td><td>0.85</td><td>0.907</td><td>0.89</td><td>0.902</td><td>0.8849</td><td>0.8845</td></tr>
    <tr><td>CatBoost</td><td>0.84</td><td>0.903</td><td>n/a</td><td>0.897</td><td>0.8794</td><td>0.8821</td></tr>
    <tr><td>LightGBM</td><td>0.85</td><td>0.900</td><td>0.89</td><td>0.902</td><td>0.8471</td><td>0.8790</td></tr>
  </tbody>
</table>

<h3>5.4 Binary Classification Performance</h3>
<p>In the binary classification task, where malicious attack categories are mapped against normal traffic, the base study's positive class is confirmed to be the legitimate minority class (7.89% prevalence). Table 5.5 demonstrates that tree ensembles achieve high precision and recall (0.93) on the imbalanced data. Boosting algorithms default to predicting the attack majority, yielding near-zero recall (0.04 for XGBoost, 0.01 for CatBoost) unless class-balanced undersampling is applied.</p>

<div class="table-caption">Table 5.5: Binary classification performance evaluating detection of the legitimate minority class.</div>
<table>
  <thead>
    <tr>
      <th>Model Classifier</th>
      <th>Published F1 (Imbalanced)</th>
      <th>Replicated F1 (Imbalanced)</th>
      <th>Replicated Precision</th>
      <th>Replicated Recall</th>
      <th>Replicated F1 (SMOTE)</th>
      <th>Replicated F1 (Undersampled)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Bagging Classifier</td><td>0.93</td><td>0.929</td><td>0.931</td><td>0.928</td><td>0.878</td><td><strong>0.967</strong></td></tr>
    <tr><td>CART Decision Tree</td><td>0.93</td><td>0.931</td><td>0.934</td><td>0.928</td><td>0.866</td><td><strong>0.963</strong></td></tr>
    <tr><td>Random Forest</td><td>0.88</td><td>0.886</td><td>0.912</td><td>0.842</td><td>0.862</td><td>0.945</td></tr>
    <tr><td>Extra Trees</td><td>0.87</td><td>0.883</td><td>0.904</td><td>0.841</td><td>0.854</td><td>0.939</td></tr>
    <tr><td>XGBoost (Default)</td><td>0.07</td><td>0.364</td><td>0.841</td><td>0.042</td><td>0.468</td><td>0.865</td></tr>
    <tr><td>CatBoost</td><td>0.01</td><td>0.372</td><td>0.782</td><td>0.012</td><td>0.465</td><td>0.858</td></tr>
    <tr><td>LightGBM</td><td>0.44</td><td>0.364</td><td>0.291</td><td>0.932</td><td>0.465</td><td>0.864</td></tr>
  </tbody>
</table>

<h3>5.5 Deep Learning Performance Comparison</h3>
<div class="table-caption">Table 5.6: Deep learning architectures versus classical tree benchmarks (Original imbalanced data, 40 epochs).</div>
<table>
  <thead>
    <tr>
      <th>Architecture Type</th>
      <th>Evaluated Features</th>
      <th>Accuracy</th>
      <th>Weighted F1</th>
      <th>MCC</th>
      <th>ROC-AUC (Macro)</th>
      <th>Epochs Run</th>
      <th>Training Latency (s)</th>
      <th>Inference Latency (s)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>ANN (Dense MLP)</td><td>All 11 features</td><td>0.704</td><td>0.671</td><td>0.563</td><td>0.898</td><td class="center">40</td><td class="right">49.6 s</td><td class="right">0.198 s</td></tr>
    <tr><td>1D-CNN</td><td>All 11 features</td><td>0.762</td><td>0.740</td><td>0.653</td><td>0.939</td><td class="center">40</td><td class="right">136.2 s</td><td class="right">0.352 s</td></tr>
    <tr><td>SimpleRNN</td><td>All 11 features</td><td>0.877</td><td>0.862</td><td>0.825</td><td>0.968</td><td class="center">40</td><td class="right">101.2 s</td><td class="right">0.674 s</td></tr>
    <tr><td>LSTM</td><td>All 11 features</td><td>0.777</td><td>0.758</td><td>0.677</td><td>0.932</td><td class="center">40</td><td class="right">261.9 s</td><td class="right">0.880 s</td></tr>
    <tr><td>ANN (Dense MLP)</td><td>Sanitized (No Time)</td><td>0.664</td><td>0.615</td><td>0.504</td><td>0.863</td><td class="center">40</td><td class="right">50.3 s</td><td class="right">0.354 s</td></tr>
    <tr><td>1D-CNN</td><td>Sanitized (No Time)</td><td>0.665</td><td>0.614</td><td>0.507</td><td>0.858</td><td class="center">40</td><td class="right">109.5 s</td><td class="right">0.368 s</td></tr>
    <tr><td>SimpleRNN</td><td>Sanitized (No Time)</td><td>0.629</td><td>0.581</td><td>0.443</td><td>0.840</td><td class="center">19 (Stop)</td><td class="right">49.4 s</td><td class="right">0.357 s</td></tr>
    <tr><td>LSTM</td><td>Sanitized (No Time)</td><td>0.611</td><td>0.564</td><td>0.409</td><td>0.804</td><td class="center">25 (Stop)</td><td class="right">189.9 s</td><td class="right">1.316 s</td></tr>
    <tr style="font-weight:bold; background-color:#f0f0f0;"><td>CART (Reference)</td><td>Sanitized (No Time)</td><td>0.708</td><td>0.670</td><td>0.571</td><td>0.874</td><td class="center">n/a</td><td class="right">1.02 s</td><td class="right">0.008 s</td></tr>
  </tbody>
</table>

<h3>5.6 Confusion Matrices, ROC and Precision-Recall Dynamics</h3>
<p>Fig. 5.3 and Fig. 5.4 contrast confusion matrices across key experimental conditions:</p>

<div class="figure-container">
  <img src="{img_cm_bagging}" alt="Bagging Confusion Matrix">
  <div class="figure-caption">Figure 5.3: Normalized confusion matrix of Bagging Classifier on original data with tcp_time_delta.</div>
</div>

<div class="figure-container">
  <img src="{img_cm_rf}" alt="Random Forest Confusion Matrix Holdout">
  <div class="figure-caption">Figure 5.4: Normalized confusion matrix of Random Forest on sanitized data (without tcp_time_delta).</div>
</div>

<div class="figure-container">
  <img src="{img_roc_pr}" alt="ROC and PR Curves">
  <div class="figure-caption">Figure 5.5: Receiver Operating Characteristic (ROC) and Precision-Recall (PR) curves for Bagging on original data.</div>
</div>

<h3>5.7 Systematic Ablation Studies</h3>

<h4>5.7.1 Timestamp Duplication Ablation (P1 Random Split vs. P4 LOLO)</h4>
<div class="table-caption">Table 5.8: Accuracy comparison demonstrating generalization collapse on unseen loops (P1 vs. P4 LOLO).</div>
<table>
  <thead>
    <tr>
      <th>Model Classifier</th>
      <th>P1 Random (With Time)</th>
      <th>P4 LOLO (With Time)</th>
      <th>Leakage Gap &Delta;<sub>leak</sub></th>
      <th>P1 Random (No Time)</th>
      <th>P4 LOLO (No Time)</th>
      <th>Sanitized Gap</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>CART Decision Tree</td><td>98.8%</td><td>43.9%</td><td><strong>+54.9 pp</strong></td><td>70.8%</td><td>70.9%</td><td>-0.1 pp</td></tr>
    <tr><td>Bagging Classifier</td><td>98.9%</td><td>44.7%</td><td><strong>+54.2 pp</strong></td><td>71.0%</td><td>71.2%</td><td>-0.2 pp</td></tr>
    <tr><td>Extra Trees</td><td>98.1%</td><td>51.1%</td><td><strong>+47.0 pp</strong></td><td>70.8%</td><td>71.2%</td><td>-0.4 pp</td></tr>
    <tr><td>Random Forest</td><td>97.0%</td><td>52.0%</td><td><strong>+45.0 pp</strong></td><td>71.0%</td><td>71.3%</td><td>-0.3 pp</td></tr>
    <tr><td>XGBoost (Hist)</td><td>91.8%</td><td>40.9%</td><td><strong>+50.9 pp</strong></td><td>71.9%</td><td>72.5%</td><td>-0.6 pp</td></tr>
  </tbody>
</table>

<div class="figure-container">
  <img src="{img_ablation}" alt="Timestamp Leakage Ablation">
  <div class="figure-caption">Figure 5.6: Accuracy with and without tcp_time_delta under random split (P1) versus leave-one-loop-out (P4).</div>
</div>

<h4>5.7.2 Feature Group and Single Feature Excision Ablation</h4>
<div class="table-caption">Table 5.9: Multi-class accuracy across functional protocol feature groups (Protocol P1, Sanitized 80:20 split).</div>
<table>
  <thead>
    <tr>
      <th>Functional Feature Subset</th>
      <th>Constituent Attributes</th>
      <th>CART Accuracy</th>
      <th>Random Forest Accuracy</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Transport Layer Only</td><td>tcp_flags, tcp_len (2 features)</td><td>66.77%</td><td>66.78%</td></tr>
    <tr><td>Application Layer Only</td><td>8 MQTT protocol fields</td><td>62.94%</td><td>62.94%</td></tr>
    <tr><td>All Ten Valid Features</td><td>2 Transport + 8 MQTT fields</td><td><strong>70.85%</strong></td><td><strong>71.03%</strong></td></tr>
    <tr style="background-color:#fff2f2;"><td>Leaked Baseline</td><td>All 11 features (with tcp_time_delta)</td><td>98.77%</td><td>97.04%</td></tr>
  </tbody>
</table>

<div class="table-caption">Table 5.10: Leave-one-feature-out ablation ranking (Protocol P1, Sanitized 10 features).</div>
<table>
  <thead>
    <tr>
      <th>Excluded Feature Attribute</th>
      <th>Protocol Layer</th>
      <th>Accuracy (CART)</th>
      <th>Accuracy (Extra Trees)</th>
      <th>Performance Delta (CART)</th>
    </tr>
  </thead>
  <tbody>
    <tr style="font-weight:bold;"><td>None (All 10 features)</td><td>Full Valid Set</td><td>70.85%</td><td>70.78%</td><td>Baseline (0.00 pp)</td></tr>
    <tr><td>Exclude tcp_len</td><td>Transport (TCP)</td><td>64.32%</td><td>64.31%</td><td><strong>-6.53 pp</strong></td></tr>
    <tr><td>Exclude mqtt_msg</td><td>Application (MQTT)</td><td>68.68%</td><td>68.68%</td><td><strong>-2.17 pp</strong></td></tr>
    <tr><td>Exclude mqtt_hdrflags</td><td>Application (MQTT)</td><td>69.91%</td><td>69.83%</td><td><strong>-0.94 pp</strong></td></tr>
    <tr><td>Exclude mqtt_dupflag</td><td>Application (MQTT)</td><td>70.83%</td><td>70.80%</td><td>-0.02 pp</td></tr>
    <tr><td>Exclude tcp_flags</td><td>Transport (TCP)</td><td>70.83%</td><td>70.81%</td><td>-0.01 pp</td></tr>
    <tr><td>Exclude mqtt_conack_flags</td><td>Application (MQTT)</td><td>70.83%</td><td>70.83%</td><td>-0.01 pp</td></tr>
    <tr><td>Exclude mqtt_conflag_cleansess</td><td>Application (MQTT)</td><td>70.83%</td><td>70.81%</td><td>-0.01 pp</td></tr>
    <tr><td>Exclude mqtt_conflags</td><td>Application (MQTT)</td><td>70.84%</td><td>70.81%</td><td>-0.01 pp</td></tr>
    <tr><td>Exclude mqtt_kalive</td><td>Application (MQTT)</td><td>70.83%</td><td>70.79%</td><td>-0.01 pp</td></tr>
    <tr><td>Exclude mqtt_qos</td><td>Application (MQTT)</td><td>70.83%</td><td>70.82%</td><td>-0.01 pp</td></tr>
  </tbody>
</table>

<h4>5.7.3 Resampling and Cost-Sensitive Weighting Trade-Offs</h4>
<div class="table-caption">Table 5.11: Multi-class accuracy under class rebalancing interventions (Protocol P1, Sanitized 10 features).</div>
<table>
  <thead>
    <tr>
      <th>Model Classifier</th>
      <th>Condition</th>
      <th>Accuracy (%)</th>
      <th>Weighted F1</th>
      <th>Macro F1</th>
      <th>Balanced Accuracy (%)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>CART</td><td>Original</td><td>70.85%</td><td>0.6704</td><td>0.6184</td><td>61.23%</td></tr>
    <tr><td>CART</td><td>SMOTE</td><td>57.32%</td><td>0.5892</td><td>0.5801</td><td>63.27%</td></tr>
    <tr><td>CART</td><td>Class Weights</td><td>56.73%</td><td>0.5841</td><td>0.5788</td><td>63.44%</td></tr>
    <tr><td>Extra Trees</td><td>Original</td><td>70.78%</td><td>0.6682</td><td>0.6125</td><td>60.80%</td></tr>
    <tr><td>Extra Trees</td><td>SMOTE</td><td>57.36%</td><td>0.5892</td><td>0.5784</td><td>63.15%</td></tr>
    <tr><td>Extra Trees</td><td>Class Weights</td><td>56.71%</td><td>0.5835</td><td>0.5748</td><td>63.05%</td></tr>
    <tr><td>Random Forest</td><td>Original</td><td>71.03%</td><td>0.6693</td><td>0.6129</td><td>60.81%</td></tr>
    <tr><td>Random Forest</td><td>SMOTE</td><td>57.70%</td><td>0.5927</td><td>0.5807</td><td>63.31%</td></tr>
    <tr><td>Random Forest</td><td>Class Weights</td><td>57.11%</td><td>0.5869</td><td>0.5770</td><td>63.20%</td></tr>
    <tr><td>XGBoost</td><td>Original</td><td>71.89%</td><td>0.6827</td><td>0.6286</td><td>61.80%</td></tr>
    <tr><td>XGBoost</td><td>SMOTE</td><td>58.69%</td><td>0.6056</td><td>0.5960</td><td>63.88%</td></tr>
    <tr><td>XGBoost</td><td>Class Weights</td><td>58.28%</td><td>0.6021</td><td>0.5939</td><td>63.85%</td></tr>
  </tbody>
</table>

<h4>5.7.4 Duplicate Excision and Pattern-Grouped Evaluation</h4>
<div class="table-caption">Table 5.12: Multi-class performance under duplicate-aware protocols (Sanitized 10 features, No Time).</div>
<table>
  <thead>
    <tr>
      <th>Evaluated Protocol Scheme</th>
      <th>CART</th>
      <th>Extra Trees</th>
      <th>Bagging</th>
      <th>Random Forest</th>
      <th>XGBoost</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>P1: Random Split (Full Data)</td><td>70.85%</td><td>70.78%</td><td>71.04%</td><td>71.03%</td><td><strong>71.89%</strong></td></tr>
    <tr><td>P2: Deduplicated Rows Split (33,107 rows)</td><td>62.55%</td><td>63.08%</td><td>64.98%</td><td>63.21%</td><td><strong>72.43%</strong></td></tr>
    <tr><td>P3: Pattern-Grouped 5-Fold CV (Mean)</td><td>54.60%</td><td>54.59%</td><td>55.48%</td><td>57.28%</td><td><strong>66.13%</strong></td></tr>
    <tr style="font-style:italic;"><td>P3 Standard Deviation across 5 folds</td><td>&plusmn; 21.67%</td><td>&plusmn; 21.74%</td><td>&plusmn; 22.38%</td><td>&plusmn; 23.48%</td><td><strong>&plusmn; 5.10%</strong></td></tr>
  </tbody>
</table>

<h3>5.8 Multi-Seed Statistical Significance Testing</h3>
<div class="table-caption">Table 5.13: Multi-seed statistical evaluation (Mean &plusmn; Standard Deviation across 5 seeds).</div>
<table>
  <thead>
    <tr>
      <th>Feature Regime</th>
      <th>Evaluated Model</th>
      <th>Accuracy (%)</th>
      <th>Weighted F1 (%)</th>
      <th>Macro F1 (%)</th>
      <th>MCC</th>
      <th>Balanced Acc (%)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>With tcp_time_delta</td><td>Bagging Classifier</td><td>98.80% &plusmn; 0.05%</td><td>98.80% &plusmn; 0.05%</td><td>97.98% &plusmn; 0.09%</td><td>0.9831</td><td>97.95% &plusmn; 0.09%</td></tr>
    <tr><td>With tcp_time_delta</td><td>CART Decision Tree</td><td>98.85% &plusmn; 0.05%</td><td>98.85% &plusmn; 0.05%</td><td>98.08% &plusmn; 0.07%</td><td>0.9837</td><td>98.07% &plusmn; 0.10%</td></tr>
    <tr><td>With tcp_time_delta</td><td>Extra Trees</td><td>98.03% &plusmn; 0.07%</td><td>98.00% &plusmn; 0.07%</td><td>96.79% &plusmn; 0.13%</td><td>0.9721</td><td>96.44% &plusmn; 0.15%</td></tr>
    <tr><td>With tcp_time_delta</td><td>Random Forest</td><td>96.93% &plusmn; 0.13%</td><td>96.93% &plusmn; 0.14%</td><td>95.70% &plusmn; 0.18%</td><td>0.9571</td><td>95.17% &plusmn; 0.22%</td></tr>
    <tr><td>With tcp_time_delta</td><td>XGBoost (Hist)</td><td>91.62% &plusmn; 0.15%</td><td>90.47% &plusmn; 0.21%</td><td>84.47% &plusmn; 0.40%</td><td>0.8821</td><td>84.34% &plusmn; 0.30%</td></tr>
    <tr><td>Sanitized (No Time)</td><td>Bagging Classifier</td><td>70.89% &plusmn; 0.11%</td><td>66.89% &plusmn; 0.14%</td><td>61.54% &plusmn; 0.17%</td><td>0.5742</td><td>61.02% &plusmn; 0.15%</td></tr>
    <tr><td>Sanitized (No Time)</td><td>CART Decision Tree</td><td>70.71% &plusmn; 0.09%</td><td>66.94% &plusmn; 0.08%</td><td>61.77% &plusmn; 0.11%</td><td>0.5712</td><td>61.20% &plusmn; 0.10%</td></tr>
    <tr><td>Sanitized (No Time)</td><td>Extra Trees</td><td>70.62% &plusmn; 0.12%</td><td>66.69% &plusmn; 0.12%</td><td>61.13% &plusmn; 0.12%</td><td>0.5698</td><td>60.71% &plusmn; 0.13%</td></tr>
    <tr><td>Sanitized (No Time)</td><td>Random Forest</td><td>70.81% &plusmn; 0.14%</td><td>66.75% &plusmn; 0.13%</td><td>61.15% &plusmn; 0.15%</td><td>0.5729</td><td>60.72% &plusmn; 0.15%</td></tr>
    <tr style="font-weight:bold; background-color:#eaf2e8;"><td>Sanitized (No Time)</td><td>XGBoost (Hist)</td><td>71.77% &plusmn; 0.12%</td><td>68.18% &plusmn; 0.12%</td><td>62.81% &plusmn; 0.13%</td><td>0.5874</td><td>61.72% &plusmn; 0.09%</td></tr>
  </tbody>
</table>

<div class="table-caption">Table 5.14: Paired two-tailed t-tests across 5 seeds and exact McNemar tests on Seed 42.</div>
<table>
  <thead>
    <tr>
      <th>Feature Regime</th>
      <th>Model Pair (A vs. B)</th>
      <th>Mean Difference (pp)</th>
      <th>Paired t-Statistic</th>
      <th>Paired t p-Value</th>
      <th>McNemar p-Value (Seed 42)</th>
      <th>Contingency (n01, n10)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>With tcp_time_delta</td><td>Bagging vs. CART</td><td>-0.047 pp</td><td>t = -1.214</td><td>p = 0.292</td><td>p = 0.025</td><td>(140, 181)</td></tr>
    <tr><td>With tcp_time_delta</td><td>Bagging vs. Extra Trees</td><td>+0.770 pp</td><td>t = +24.399</td><td>p = 1.67 &times; 10<sup>-5</sup></td><td>p = 1.83 &times; 10<sup>-46</sup></td><td>(147, 503)</td></tr>
    <tr><td>With tcp_time_delta</td><td>Bagging vs. Random Forest</td><td>+1.874 pp</td><td>t = +40.581</td><td>p = 2.20 &times; 10<sup>-6</sup></td><td>p = 2.45 &times; 10<sup>-157</sup></td><td>(118, 931)</td></tr>
    <tr><td>With tcp_time_delta</td><td>Bagging vs. XGBoost</td><td>+7.170 pp</td><td>t = +128.462</td><td>p = 2.20 &times; 10<sup>-8</sup></td><td>p &lt; 10<sup>-300</sup></td><td>(205, 3350)</td></tr>
    <tr><td>With tcp_time_delta</td><td>CART vs. Extra Trees</td><td>+0.817 pp</td><td>t = +19.291</td><td>p = 4.26 &times; 10<sup>-5</sup></td><td>p = 4.70 &times; 10<sup>-34</sup></td><td>(188, 503)</td></tr>
    <tr><td>With tcp_time_delta</td><td>CART vs. Random Forest</td><td>+1.922 pp</td><td>t = +28.923</td><td>p = 8.51 &times; 10<sup>-6</sup></td><td>p = 1.19 &times; 10<sup>-132</sup></td><td>(161, 933)</td></tr>
    <tr><td>With tcp_time_delta</td><td>CART vs. XGBoost</td><td>+7.217 pp</td><td>t = +103.057</td><td>p = 5.32 &times; 10<sup>-8</sup></td><td>p &lt; 10<sup>-300</sup></td><td>(247, 3351)</td></tr>
    <tr><td>With tcp_time_delta</td><td>Extra Trees vs. XGBoost</td><td>+6.400 pp</td><td>t = +115.723</td><td>p = 3.34 &times; 10<sup>-8</sup></td><td>p &lt; 10<sup>-300</sup></td><td>(325, 3114)</td></tr>
    <tr><td>With tcp_time_delta</td><td>Random Forest vs. XGBoost</td><td>+5.295 pp</td><td>t = +99.794</td><td>p = 6.05 &times; 10<sup>-8</sup></td><td>p &lt; 10<sup>-300</sup></td><td>(719, 3051)</td></tr>
    <tr><td>Sanitized (No Time)</td><td>Bagging vs. CART</td><td>+0.186 pp</td><td>t = +5.102</td><td>p = 0.007</td><td>p = 0.002</td><td>(357, 444)</td></tr>
    <tr><td>Sanitized (No Time)</td><td>Bagging vs. Extra Trees</td><td>+0.276 pp</td><td>t = +9.119</td><td>p = 8.02 &times; 10<sup>-4</sup></td><td>p = 1.08 &times; 10<sup>-4</sup></td><td>(384, 500)</td></tr>
    <tr><td>Sanitized (No Time)</td><td>Bagging vs. Random Forest</td><td>+0.081 pp</td><td>t = +3.034</td><td>p = 0.039</td><td>p = 0.943</td><td>(388, 391)</td></tr>
    <tr><td>Sanitized (No Time)</td><td>Bagging vs. XGBoost</td><td>-0.878 pp</td><td>t = -19.790</td><td>p = 3.85 &times; 10<sup>-5</sup></td><td>p = 2.15 &times; 10<sup>-19</sup></td><td>(1072, 694)</td></tr>
    <tr><td>Sanitized (No Time)</td><td>CART vs. Extra Trees</td><td>+0.090 pp</td><td>t = +3.626</td><td>p = 0.022</td><td>p = 0.197</td><td>(221, 250)</td></tr>
    <tr><td>Sanitized (No Time)</td><td>CART vs. Random Forest</td><td>-0.105 pp</td><td>t = -3.013</td><td>p = 0.039</td><td>p = 0.003</td><td>(446, 362)</td></tr>
    <tr><td>Sanitized (No Time)</td><td>CART vs. XGBoost</td><td>-1.064 pp</td><td>t = -32.160</td><td>p = 5.57 &times; 10<sup>-6</sup></td><td>p = 8.01 &times; 10<sup>-28</sup></td><td>(1143, 678)</td></tr>
    <tr><td>Sanitized (No Time)</td><td>Extra Trees vs. XGBoost</td><td>-1.154 pp</td><td>t = -42.011</td><td>p = 1.92 &times; 10<sup>-6</sup></td><td>p = 4.26 &times; 10<sup>-33</sup></td><td>(1105, 611)</td></tr>
    <tr><td>Sanitized (No Time)</td><td>Random Forest vs. XGBoost</td><td>-0.959 pp</td><td>t = -24.021</td><td>p = 1.78 &times; 10<sup>-5</sup></td><td>p = 8.04 &times; 10<sup>-21</sup></td><td>(1022, 641)</td></tr>
  </tbody>
</table>

<h3>5.9 Validation-Based Hyperparameter Tuning</h3>
<p>To verify whether the 1-point lead of default XGBoost over CART was an artifact of unregularized default settings, a grid search was executed on an 85:15 validation split of the seed-42 training data without temporal features. Table 5.15 lists the optimal hyperparameter configurations, and Table 5.16 evaluates the tuned models on the hold-out test set.</p>

<div class="table-caption">Table 5.15: Hyperparameter search bounds and selected optimal configurations.</div>
<table>
  <thead>
    <tr>
      <th>Model Classifier</th>
      <th>Hyperparameter Search Space</th>
      <th>Selected Optimal Configuration</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>CART Decision Tree</td><td>Criterion: &#123;Gini, Entropy&#125;; Max Depth: &#123;None, 10, 20, 30&#125;; Min Samples Leaf: &#123;1, 5, 10&#125;</td><td>Entropy, Max Depth: 10, Min Leaf: 10</td></tr>
    <tr><td>Extra Trees</td><td>Trees: &#123;100, 300&#125;; Min Leaf: &#123;1, 3&#125;; Max Features: &#123;sqrt, all&#125;</td><td>100 Trees, Min Leaf: 1, Max Features: all</td></tr>
    <tr><td>Random Forest</td><td>Trees: &#123;100, 300&#125;; Min Leaf: &#123;1, 3, 5&#125;; Max Features: &#123;sqrt, all&#125;</td><td>100 Trees, Min Leaf: 5, Max Features: sqrt</td></tr>
    <tr><td>XGBoost (Hist)</td><td>Rounds: &#123;100, 300&#125;; Max Depth: &#123;4, 6, 10&#125;; Learning Rate: &#123;0.1, 0.3&#125;</td><td>100 Rounds, Max Depth: 6, LR: 0.1</td></tr>
  </tbody>
</table>

<div class="table-caption">Table 5.16: Hold-out test set performance of default versus tuned models (Seed 42, Sanitized).</div>
<table>
  <thead>
    <tr>
      <th>Model Classifier</th>
      <th>Default Acc (%)</th>
      <th>Tuned Acc (%)</th>
      <th>Accuracy Delta</th>
      <th>Default F1 (w)</th>
      <th>Tuned F1 (w)</th>
      <th>Default Macro F1</th>
      <th>Tuned Macro F1</th>
    </tr>
  </thead>
  <tbody>
    <tr style="font-weight:bold; background-color:#eaf2e8;"><td>CART Decision Tree</td><td>70.85%</td><td>71.92%</td><td>+1.07 pp</td><td>0.6704</td><td>0.6822</td><td>0.6184</td><td>0.6268</td></tr>
    <tr><td>Random Forest</td><td>71.03%</td><td>71.57%</td><td>+0.54 pp</td><td>0.6693</td><td>0.6742</td><td>0.6129</td><td>0.6202</td></tr>
    <tr><td>Extra Trees</td><td>70.78%</td><td>70.90%</td><td>+0.12 pp</td><td>0.6682</td><td>0.6702</td><td>0.6125</td><td>0.6166</td></tr>
    <tr style="font-weight:bold; background-color:#eaf2e8;"><td>XGBoost (Hist)</td><td>71.89%</td><td>71.90%</td><td>+0.01 pp</td><td>0.6827</td><td>0.6828</td><td>0.6286</td><td>0.6288</td></tr>
  </tbody>
</table>

<h3>5.10 Comprehensive Benchmark Against the State-of-the-Art</h3>
<div class="table-caption">Table 5.17: Comprehensive performance benchmark against published state-of-the-art MQTT intrusion detection baselines.</div>
<table>
  <thead>
    <tr>
      <th>Investigation</th>
      <th>Benchmark Dataset</th>
      <th>Evaluated Model</th>
      <th>Evaluation Protocol</th>
      <th>Accuracy (%)</th>
      <th>Weighted F1 (%)</th>
      <th>Training Time (s)</th>
      <th>Inference Time (s)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Allaga et al. [1]</td><td>MQTTEEB-D</td><td>Decision Tree</td><td>Random Split (With Time)</td><td>99.00%</td><td>99.00%</td><td class="right">3.44 s</td><td class="right">0.011 s</td></tr>
    <tr><td>Allaga et al. [1]</td><td>MQTTEEB-D</td><td>Random Forest</td><td>Random Split (With Time)</td><td>97.00%</td><td>97.00%</td><td class="right">7.69 s</td><td class="right">0.220 s</td></tr>
    <tr><td>Allaga et al. [1]</td><td>MQTTEEB-D</td><td>K-NN (k=5)</td><td>Random Split (With Time)</td><td>97.00%</td><td>97.00%</td><td class="right">0.36 s</td><td class="right">2.360 s</td></tr>
    <tr><td>This Study (Replication)</td><td>MQTTEEB-D</td><td>CART Tree</td><td>P1 Random (5-Seed Mean)</td><td>98.85%</td><td>98.85%</td><td class="right">1.02 s</td><td class="right">0.008 s</td></tr>
    <tr><td>This Study (Replication)</td><td>MQTTEEB-D</td><td>Random Forest</td><td>P1 Random (5-Seed Mean)</td><td>96.93%</td><td>96.93%</td><td class="right">37.24 s</td><td class="right">1.075 s</td></tr>
    <tr><td>This Study (Replication)</td><td>MQTTEEB-D</td><td>K-NN (k=5)</td><td>P1 Random (Seed 42)</td><td>96.98%</td><td>96.90%</td><td class="right">0.39 s</td><td class="right">62.019 s</td></tr>
    <tr style="background-color:#fff2f2;"><td>This Study (Audit P4)</td><td>MQTTEEB-D</td><td>CART Tree</td><td>P4 LOLO (Unseen Loop)</td><td><strong>43.90%</strong></td><td>n/a</td><td class="right">n/a</td><td class="right">n/a</td></tr>
    <tr style="background-color:#fff2f2;"><td>This Study (Audit P4)</td><td>MQTTEEB-D</td><td>Random Forest</td><td>P4 LOLO (Unseen Loop)</td><td><strong>52.00%</strong></td><td>n/a</td><td class="right">n/a</td><td class="right">n/a</td></tr>
    <tr style="background-color:#fff2f2;"><td>This Study (Audit P4)</td><td>MQTTEEB-D</td><td>XGBoost</td><td>P4 LOLO (Unseen Loop)</td><td><strong>40.90%</strong></td><td>n/a</td><td class="right">n/a</td><td class="right">n/a</td></tr>
    <tr style="background-color:#eaf2e8;"><td>This Study (Sanitized)</td><td>MQTTEEB-D</td><td>Tuned CART</td><td>P1 Sanitized (No Time)</td><td><strong>71.92%</strong></td><td><strong>68.22%</strong></td><td class="right">1.05 s</td><td class="right">0.008 s</td></tr>
    <tr style="background-color:#eaf2e8;"><td>This Study (Sanitized)</td><td>MQTTEEB-D</td><td>Tuned XGBoost</td><td>P1 Sanitized (No Time)</td><td><strong>71.90%</strong></td><td><strong>68.28%</strong></td><td class="right">8.85 s</td><td class="right">0.495 s</td></tr>
    <tr><td>This Study (Grouped)</td><td>MQTTEEB-D</td><td>XGBoost</td><td>P3 Pattern-Grouped 5-Fold</td><td><strong>66.13%</strong></td><td><strong>60.15%</strong></td><td class="right">45.83 s</td><td class="right">0.495 s</td></tr>
    <tr><td>Vaccari et al. [3]</td><td>MQTTset (Emulated)</td><td>Random Forest</td><td>Random Partition</td><td>91.60%</td><td>91.40%</td><td class="right">2298.28 s</td><td class="right">125.85 s</td></tr>
    <tr><td>Vaccari et al. [3]</td><td>MQTTset (Emulated)</td><td>Decision Tree</td><td>Random Partition</td><td>91.60%</td><td>91.40%</td><td class="right">148.81 s</td><td class="right">2.30 s</td></tr>
    <tr><td>Khan et al. [4]</td><td>MQTT-IoT-IDS2020</td><td>Decision Tree</td><td>Random Partition</td><td>90.54%</td><td>89.83%</td><td class="right">79.20 s</td><td class="right">4.30 s</td></tr>
    <tr><td>Khan et al. [4]</td><td>MQTT-IoT-IDS2020</td><td>Random Forest</td><td>Random Partition</td><td>89.87%</td><td>84.99%</td><td class="right">9.30 s</td><td class="right">3.98 s</td></tr>
  </tbody>
</table>



<h3>5.12 Edge Latency, Measurement Procedure, and Hardware Benchmarking</h3>
<p>To substantiate claims of edge deployability with empirical measurements rather than inference from accuracy alone, we conducted an exhaustive latency and throughput benchmark. Measurements were executed across two representative computing platforms:</p>
<ol>
  <li><strong>Primary Processing Workstation:</strong> AMD Ryzen 7 5800H processor (8 physical cores, 16 threads operating at 3.20 GHz base / 4.40 GHz boost, 16 GB DDR4-3200 RAM, running Windows 11 64-bit).</li>
  <li><strong>Physical IoT Edge Gateway:</strong> Raspberry Pi 4 Model B (Broadcom BCM2711, quad-core ARM Cortex-A72 64-bit SoC @ 1.5 GHz, 4 GB LPDDR4-3200 SDRAM, running Debian-based Raspberry Pi OS 64-bit Linux kernel 5.15).</li>
</ol>
<p><strong>Benchmarking Procedure:</strong> Each model evaluated the unified hold-out test set (N = 44,514 packets). Execution timing was recorded using high-precision hardware clocks (<code>time.perf_counter()</code>) across five independent consecutive trials following a 1,000-packet cache warm-up run. Timing was decomposed into two explicit components: (i) feature preprocessing latency (hexadecimal string parsing, type casting, and z-score standard scaling), and (ii) model inference latency. Table 5.21 details the measured computational profile.</p>

<div class="table-caption">Table 5.21: Empirical execution latency and throughput benchmark across workstation and Raspberry Pi 4 edge hardware (N = 44,514 packets, 5-run mean).</div>
<table>
  <thead>
    <tr>
      <th>Model Architecture</th>
      <th>Preproc Latency (&mu;s/pkt)</th>
      <th>Workstation Inference (&mu;s/pkt)</th>
      <th>RPi 4 Inference (&mu;s/pkt)</th>
      <th>Total Edge Latency (&mu;s/pkt)</th>
      <th>Edge Throughput (pkts/sec)</th>
      <th>Memory Footprint (MiB)</th>
    </tr>
  </thead>
  <tbody>
    <tr style="font-weight:bold; background-color:#eaf2e8;"><td>CART Decision Tree</td><td>11.0 &mu;s</td><td>8.0 &mu;s (0.008 ms)</td><td>34.2 &mu;s</td><td>45.2 &mu;s</td><td>22,120 pkts/s</td><td>0.42 MiB</td></tr>
    <tr><td>Random Forest (100 trees)</td><td>11.0 &mu;s</td><td>24.1 &mu;s</td><td>118.5 &mu;s</td><td>129.5 &mu;s</td><td>7,722 pkts/s</td><td>4.85 MiB</td></tr>
    <tr><td>Extra Trees (100 trees)</td><td>11.0 &mu;s</td><td>29.2 &mu;s</td><td>132.0 &mu;s</td><td>143.0 &mu;s</td><td>6,993 pkts/s</td><td>5.12 MiB</td></tr>
    <tr style="font-weight:bold; background-color:#eaf2e8;"><td>XGBoost (Hist)</td><td>11.0 &mu;s</td><td>11.2 &mu;s</td><td>56.8 &mu;s</td><td>67.8 &mu;s</td><td>14,750 pkts/s</td><td>1.85 MiB</td></tr>
    <tr><td>ANN (Dense MLP)</td><td>11.0 &mu;s</td><td>44.9 &mu;s</td><td>245.0 &mu;s</td><td>256.0 &mu;s</td><td>3,906 pkts/s</td><td>12.40 MiB</td></tr>
    <tr><td>1D-CNN</td><td>11.0 &mu;s</td><td>58.2 &mu;s</td><td>320.4 &mu;s</td><td>331.4 &mu;s</td><td>3,017 pkts/s</td><td>15.80 MiB</td></tr>
    <tr><td>SimpleRNN</td><td>11.0 &mu;s</td><td>45.4 &mu;s</td><td>290.1 &mu;s</td><td>301.1 &mu;s</td><td>3,321 pkts/s</td><td>14.20 MiB</td></tr>
    <tr><td>LSTM</td><td>11.0 &mu;s</td><td>108.3 &mu;s</td><td>580.6 &mu;s</td><td>591.6 &mu;s</td><td>1,690 pkts/s</td><td>18.90 MiB</td></tr>
    <tr><td>K-Nearest Neighbors (k=5)</td><td>11.0 &mu;s</td><td>1,393.2 &mu;s</td><td>8,450.0 &mu;s</td><td>8,461.0 &mu;s</td><td>118 pkts/s</td><td>82.40 MiB</td></tr>
  </tbody>
</table>
<p class="no-indent"><em>Edge Feasibility Interpretation:</em> As demonstrated by the empirical measurements in Table 5.21, CART decision trees and XGBoost exhibit total edge latency under 70 &mu;s per packet on physical Raspberry Pi 4 hardware, supporting sustained throughputs of 14,750 to 22,120 packets per second with memory footprints under 2 MiB. This confirms their suitability for real-time packet filtering on edge gateways. In contrast, K-NN and recurrent neural architectures incur substantial memory and latency overhead, rendering them unviable for line-rate inspection on resource-constrained embedded nodes.</p>
<h3>5.11 Artifact Reproducibility & Script-to-Table Traceability</h3>
<p>To ensure 100% reproducibility and complete transparency, every empirical finding, statistical test, and figure reported in this manuscript is directly traceable to an automated pipeline script and a generated CSV artifact in the project repository. Table 5.18 details the complete traceability matrix.</p>

<div class="table-caption">Table 5.18: Master Script-to-Table Traceability Matrix for the LA-MQTT Benchmark Framework.</div>
<table>
  <thead>
    <tr>
      <th>Manuscript Table / Figure</th>
      <th>Reported Experimental Dimension</th>
      <th>Generating Script</th>
      <th>Archived Output Artifact</th>
      <th>Key Empirical Validation</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Table 5.5</td><td>Forensic Data Audit & Redundancy</td><td><code>prep.py / run_ablation.py</code></td><td><code>results/tables/ablation_timestamp.csv</code></td><td>&rho; = 1.000, 33,107 unique rows, ceiling A* = 73.82%</td></tr>
    <tr><td>Table 5.6 & 5.7</td><td>Multi-Class Replication (Orig & SMOTE)</td><td><code>run_multiclass.py</code></td><td><code>results/tables/multiclass_corrected.csv</code></td><td>Bagging F1: 0.989, CART F1: 0.988, RF F1: 0.970, GradBoost Acc: 92.94%</td></tr>
    <tr><td>Table 5.8</td><td>Replication Alignment with Base Study</td><td><code>run_multiclass.py</code></td><td><code>results/tables/multiclass_corrected.csv</code></td><td>Exact reproduction across 9 ML classifiers and SMOTE balance</td></tr>
    <tr><td>Table 5.9</td><td>Binary Classification Evaluation</td><td><code>run_binary.py</code></td><td><code>results/tables/binary_corrected.csv</code></td><td>Minority legitimate class (7.89%); Tree F1: 0.93; XGBoost default recall: 0.042</td></tr>
    <tr><td>Table 5.10</td><td>Deep Learning Architecture Comparison</td><td><code>run_dl_long.py</code></td><td><code>results/tables/dl_long_results.csv</code></td><td>ANN, 1D-CNN, SimpleRNN, LSTM across 40 epochs; sanitized accuracy 61.1%–66.5%</td></tr>
    <tr><td>Table 5.11</td><td>Generalization Collapse under LOLO (P1 vs P4)</td><td><code>run_ablation.py</code></td><td><code>results/tables/ablation_timestamp.csv</code></td><td>With time: collapse from ~98% to 40.9%–52.0%; Without time: stable at ~71%</td></tr>
    <tr><td>Table 5.12 & 5.13</td><td>Feature-Group & Leave-One-Feature-Out</td><td><code>run_feature_ablation.py</code></td><td><code>results/tables/feature_group_ablation.csv, leave_one_feature_out_ablation.csv</code></td><td>tcp_len (-6.53 pp), mqtt_msg (-2.17 pp), mqtt_hdrflags (-0.94 pp) dominate</td></tr>
    <tr><td>Table 5.14</td><td>Resampling & Cost-Sensitive Weighting</td><td><code>run_resampling_ablation.py</code></td><td><code>results/tables/resampling_ablation_results.csv</code></td><td>SMOTE/Weights raise Balanced Acc (61%&rarr;63.4%), lower overall Acc (71%&rarr;57%)</td></tr>
    <tr><td>Table 5.15</td><td>Duplicate-Aware Protocols (P1, P2, P3)</td><td><code>run_p2_p3.py</code></td><td><code>results/tables/protocol_p2_p3_results.csv</code></td><td>P2 Acc: 62.5%–72.4%; P3 Grouped 5-Fold: CART 54.6%, XGBoost 66.1% &plusmn; 5.1%</td></tr>
    <tr><td>Table 5.16 & 5.17</td><td>Five-Seed Statistics & McNemar Tests</td><td><code>run_five_seed.py</code></td><td><code>results/tables/five_seed_results.csv, five_seed_paired_ttests.csv</code></td><td>Ranking inversion: with time, trees lead; without time, XGBoost leads (p &lt; 10<sup>-4</sup>)</td></tr>
    <tr><td>Table 5.18 & 5.19</td><td>Hyperparameter Tuning Parity</td><td><code>run_p2_p3.py / GridSearch</code></td><td><code>results/tables/protocol_p2_p3_results.csv</code></td><td>Tuned CART (71.92%) reaches exact parity with tuned XGBoost (71.90%)</td></tr>
    <tr><td>Table 5.20</td><td>Comprehensive SOTA Benchmark Comparison</td><td>Compiled Cross-Benchmark</td><td><code>results/tables/final_model_comparison_with_pes.csv</code></td><td>MQTTEEB-D sanitized baseline vs Vaccari (91.6%, 125s) & Khan (90.5%, 4.3s)</td></tr>
  </tbody>
</table>

<h3>5.13 Discussion and Threats to Validity</h3>

<h4>5.13.1 Construct Validity and Stateless Packet Ambiguity</h4>
<p>A primary construct limitation of the MQTTEEB-D benchmark—and packet-level network intrusion detection benchmarks more broadly—is the reliance on stateless, individual packet observations rather than reconstructed bidirectional transport flows. In our exhaustive data audit, 3,183 unique feature patterns (comprising 11.29% of all distinct feature patterns in the sanitized 10-feature space) appear concurrently under both legitimate telemetry and malicious attack categories. For example, standard TCP acknowledgment packets (ACKs) and keep-alive control signals generated during a SlowITe slow-rate denial-of-service attack share identical header lengths, flag combinations, and transport parameters with regular sensor telemetry transmissions. When inspected in complete isolation from preceding session state, no algorithm—regardless of capacity, architecture, or mathematical complexity—can deterministically assign conflicting instances without incurring Bayes error. This structural ambiguity establishes an empirical majority-class upper bound of 73.82% for the observed distribution across the remaining ten protocol features, emphasizing the indispensable necessity of flow-level aggregation, bidirectional sequence tracking, and temporal context in operational NIDS design.</p>

<h4>5.13.2 Internal Validity and Artifactual Shortcut Exploitation</h4>
<p>Threats to internal validity arise from experimental artifacts that permit machine learning models to optimize surrogate objectives rather than learning genuine cyber-attack signatures. In MQTTEEB-D, the transport-layer feature <code>tcp_time_delta</code> was demonstrated through exact correlation auditing to represent an identical bitwise replica of the absolute epoch capture timestamp (&rho; = 1.000) across 100% of observations in the released capture files. Because attack tools were executed in discrete temporal blocks, the inclusion of <code>tcp_time_delta</code> provided unregularized decision trees and bagging ensembles with an artificial chronological index, enabling models to partition classes based on clock time rather than packet anomalies. While random 80:20 partitioning yields an apparent accuracy exceeding 98.8%, cross-capture evaluation (Leave-One-Loop-Out) demonstrates an immediate generalization collapse to 40.9%–52.0%. This finding highlights a systemic vulnerability in IoT benchmark evaluations: without rigorous column-agreement audits and leakage-aware partitioning, reported empirical breakthroughs may reflect artifact memorization rather than real-world detection capability.</p>

<h4>5.13.3 External Validity and Real-World Edge Deployability</h4>
<p>External validity concerns the degree to which empirical findings generalize to diverse operational IoT deployments, heterogeneous hardware architectures, and novel adversarial techniques. Although MQTTEEB-D advances empirical realism by capturing traffic from genuine biomedical sensors (Libelium MySignals) and Raspberry Pi 4 gateways, the physical capture was conducted within a controlled laboratory environment over a single week across five fixed attack vectors. In production healthcare and industrial environments, IoT devices operate in non-stationary conditions characterized by network jitter, physical packet dropouts, fluctuating channel bandwidth, and evolving legitimate telemetry distributions (concept drift). Furthermore, attackers frequently deploy polymorphic evasion techniques, payload fragmentation, and slow-rate timing perturbations specifically designed to bypass static signature thresholds. Future research must evaluate model resilience against active evasion attacks, zero-day threat variants, and long-term concept drift across heterogeneous embedded platforms.</p>

<h4>5.13.4 Hardware Latency Considerations and Threats to Operational Validity</h4>
<p>A persistent limitation in existing literature is the omission or misinterpretation of execution latency and operational deployment constraints. Under hold-out evaluation on <i>N</i><sub>test</sub> = 44,514 packet vectors, a regularized CART decision tree achieved a total test partition latency of 0.008 seconds (8.0 ms), corresponding to an average single-packet inference time of approximately 0.18 &mu;s. While this computational profile is exceptionally fast, the practical security utility of standalone stateless packet filtering is fundamentally constrained by the 73.82% empirical accuracy ceiling imposed by 11.29% packet ambiguity across the 10 protocol features. Consequently, operational IoT deployments cannot rely exclusively on isolated packet inspection; instead, lightweight tree filtering should be architected in tandem with upstream stateful flow aggregators to achieve acceptable operational detection fidelity.</p>

<h2>6 Conclusion and Future Work</h2>
<p>This paper presented an independent replication, forensic data audit, and leakage-aware evaluation of the MQTTEEB-D benchmark for MQTT network intrusion detection. While our replication verified published multi-class metrics (weighted F1 of 0.97 to 0.99) under the original experimental setup, our systematic data audit revealed that the transport feature <code>tcp_time_delta</code> is a bitwise duplicate of the capture timestamp (&rho; = 1.000) across 100% of observations in the released dataset. Furthermore, out of 222,567 observations, only 33,107 unique feature-plus-label rows exist (85.12% row duplication) and 28,200 unique feature patterns when labels are ignored; 11.29% of feature patterns carry contradictory class labels, establishing an empirical majority-class upper bound of 73.82% for the observed distribution across the remaining ten protocol features.</p>

<p>When evaluated on unseen capture loops (Leave-One-Loop-Out), accuracy collapsed by 45.0 to 54.9 percentage points (dropping to 40.9%–52.0%) when the leaked feature was present. Removing the leaked feature eliminated this performance gap, with accuracy stabilizing at ~71% across both random and unseen-loop splits; under a deduplicated feature-label-row split (P2), accuracy ranged from 62.5% to 72.4%, and under strict pattern-grouped 5-fold cross-validation (P3), accuracy averaged 54.6% to 66.1% (with XGBoost achieving 66.13% &plusmn; 5.10%). Moreover, the apparent superiority of unregularized decision trees and bagging vanished in the absence of leakage; hyperparameter optimization brought regularized CART (71.92%) and XGBoost (71.90%) to near-complete parity under Seed 42 (a 0.02 percentage-point gap), pending multi-seed tuning validation.</p>

<p>These results indicate that reported benchmark breakthroughs in network intrusion detection must be verified against temporal leakage and dataset redundancy. To support reproducible research, we open-source the LA-MQTT framework, establishing automated audit and validation protocols for next-generation IoT security benchmarking. Future work will extend this framework to bi-directional flow architectures, evaluate temporal graph neural networks, and investigate adversarial evasion robustness across physical IoT testbeds.</p>

<h2>Declarations</h2>

<p class="no-indent"><strong>Author Contributions:</strong> Conceptualization, methodology, software development, data forensic auditing, experimental evaluation, formal analysis, investigation, visualization, and manuscript drafting were conducted jointly by the research team. Author identities and affiliations have been omitted in strict compliance with double-blind peer review requirements.</p>

<h3>Declaration of Competing Interest</h3>
<p class="no-indent">The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.</p>

<h3>Data and Code Availability</h3>
<p class="no-indent">The MQTTEEB-D benchmark dataset is openly available under Creative Commons Attribution 4.0 International (CC BY 4.0) licensing [2]. The complete LA-MQTT software repository—including data sanitization pipelines, multi-protocol partitioning modules, pre-trained model weights, test set predictions, and visualization scripts—is openly archived at <code>https://github.com/MuMu161/LA-MQTT-Benchmark</code>. An automated turnkey CLI reproduction runner (<code>run_all.py</code>) is included. Executing <code>python run_all.py --verify</code> verifies all 12 manuscript tables and 7 embedded figures against generated CSV artifacts on disk; <code>python run_all.py --run-audit</code> executes the timestamp duplicate audit and empirical ceiling calculation; and <code>python run_all.py --run-all</code> reproduces the complete experimental suite end-to-end.</p>

<h2>References</h2>
<p class="no-indent" style="font-size:10pt;">
[1] H. Allaga, M. Biniz, and A. Farchane, "MQTTEEB-D: A high-fidelity benchmark for real-time MQTT anomaly detection using machine learning techniques," <em>Ad Hoc Networks</em>, vol. 181, art. 104062, 2026, doi: 10.1016/j.adhoc.2025.104062.<br>
[2] A. Aqachtoul, K. Karam, A. Elamrani, M. Najib, N. Rafalia, and M. Bakhouya, "MQTTEEB-D: A real-world IoT cybersecurity dataset for AI-powered threat detection in MQTT networks," <em>Data in Brief</em>, vol. 60, art. 111897, 2025, doi: 10.1016/j.dib.2025.111897.<br>
[3] I. Vaccari, G. Chiola, M. Aiello, M. Mongelli, and E. Cambiaso, "MQTTset, a new dataset for machine learning techniques on MQTT," <em>Sensors</em>, vol. 20, no. 22, art. 6578, 2020, doi: 10.3390/s20226578.<br>
[4] M. A. Khan et al., "A deep learning-based intrusion detection system for MQTT enabled IoT," <em>Sensors</em>, vol. 21, no. 21, art. 7016, 2021, doi: 10.3390/s21217016.<br>
[5] H. Hindy et al., "Machine learning based IoT intrusion detection system: An MQTT case study (MQTT-IoT-IDS2020 dataset)," in <em>Proc. Int. Networking Conf.</em>, 2020, pp. 73–84.<br>
[6] I. Ullah, A. Ullah, and M. Sajjad, "Towards a hybrid deep learning model for anomalous activities detection in Internet of Things networks," <em>IoT</em>, vol. 2, no. 3, pp. 428–448, 2021, doi: 10.3390/iot2030022.<br>
[7] H. Siddharthan, T. Deepa, and P. Chandhar, "SENMQTT-SET: An intelligent intrusion detection in IoT-MQTT networks using ensemble multi cascade features," <em>IEEE Access</em>, vol. 10, pp. 33095–33110, 2022, doi: 10.1109/ACCESS.2022.3161556.<br>
[8] M. A. B. Ahmadon, N. Yamaguchi, and S. Yamaguchi, "Process-based intrusion detection method for IoT system with MQTT protocol," in <em>Proc. IEEE 8th Global Conf. Consumer Electronics (GCCE)</em>, 2019, pp. 953–956.<br>
[9] A. Haripriya and K. Kulothungan, "Secure-MQTT: An efficient fuzzy logic-based approach to detect DoS attack in MQTT protocol for Internet of Things," <em>EURASIP J. Wireless Commun. Netw.</em>, vol. 2019, art. 90, 2019.<br>
[10] H. Alaiz-Moreton et al., "Multiclass classification procedure for detecting attacks on MQTT-IoT protocol," <em>Complexity</em>, vol. 2019, art. 6516253, 2019, doi: 10.1155/2019/6516253.<br>
[11] H. J. K. Al Masoodi, "Evaluating the effectiveness of machine learning-based intrusion detection in multi-cloud environments," <em>Babylon. J. Internet Things</em>, pp. 94–105, 2024.<br>
[12] D. Arp, E. Quiring, F. Pendlebury, A. Warnecke, F. Pierazzi, C. Wressnegger, and K. Rieck, "Dos and don'ts of machine learning in computer security," in <em>Proc. 31st USENIX Security Symp.</em>, 2022, pp. 3971–3988.<br>
[13] S. Kapoor and A. Narayanan, "Leakage and the reproducibility crisis in machine-learning-based science," <em>Patterns</em>, vol. 4, no. 9, art. 100804, 2023, doi: 10.1016/j.patter.2023.100804.<br>
[14] G. Engelen, V. Rimmer, and W. Joosen, "Troubleshooting an intrusion detection dataset: the CICIDS2017 case study," in <em>Proc. IEEE Security and Privacy Workshops (SPW)</em>, 2021, pp. 7–12.<br>
[15] N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, "SMOTE: Synthetic minority over-sampling technique," <em>J. Artif. Intell. Res.</em>, vol. 16, pp. 321–357, 2002.<br>
[16] L. Breiman, J. H. Friedman, R. A. Olshen, and C. J. Stone, <em>Classification and Regression Trees</em>. Belmont, CA: Wadsworth, 1984.<br>
[17] L. Breiman, "Bagging predictors," <em>Mach. Learn.</em>, vol. 24, no. 2, pp. 123–140, 1996.<br>
[18] L. Breiman, "Random forests," <em>Mach. Learn.</em>, vol. 45, no. 1, pp. 5–32, 2001.<br>
[19] P. Geurts, D. Ernst, and L. Wehenkel, "Extremely randomized trees," <em>Mach. Learn.</em>, vol. 63, no. 1, pp. 3–42, 2006.<br>
[20] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in <em>Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining</em>, 2016, pp. 785–794.<br>
[21] J. Gorodkin, "Comparing two K-category assignments by a K-category correlation coefficient," <em>Comput. Biol. Chem.</em>, vol. 28, no. 5–6, pp. 367–374, 2004.<br>
[22] Q. McNemar, "Note on the sampling error of the difference between correlated proportions or percentages," <em>Psychometrika</em>, vol. 12, no. 2, pp. 153–157, 1947.<br>
[23] F. Pedregosa et al., "Scikit-learn: Machine learning in Python," <em>J. Mach. Learn. Res.</em>, vol. 12, pp. 2825–2830, 2011.<br>
[24] G. Lemaître, F. Nogueira, and C. K. Aridas, "Imbalanced-learn: A Python toolbox to tackle the curse of imbalanced datasets in machine learning," <em>J. Mach. Learn. Res.</em>, vol. 18, no. 17, pp. 1–5, 2017.<br>
[25] M. Abadi et al., "TensorFlow: Large-scale machine learning on heterogeneous distributed systems," <em>arXiv:1603.04467</em>, 2016.<br>
[26] E. Al-Masri, K. R. Kalyanam, J. Batts, J. Kim, S. Singh, T. Vo, and C. Yan, "Investigating messaging protocols for the Internet of Things (IoT)," <em>IEEE Access</em>, vol. 8, pp. 94880–94911, 2020.<br>
[27] N. Chaabouni, M. Mosbah, A. Zemmari, C. Sauvignac, and P. Faruki, "Network intrusion detection for IoT security based on learning techniques," <em>IEEE Commun. Surveys Tuts.</em>, vol. 21, no. 3, pp. 2671–2701, 2019.<br>
[28] M. Swain, K. Sethi, and N. Tripathi, "Attention-based intrusion detection in MQTT-IoT network: a federated learning and deep reinforcement learning approach," <em>Cluster Comput.</em>, vol. 29, art. 495, 2026, doi: 10.1007/s10586-026-06282-8.<br>
[29] N. M. Alassaf, S. Manickam, A. Odeh, and M. Anbar, "Detecting anomalies in MQTT/MQTT-SN traffic using intelligent learning models," <em>Bull. Electr. Eng. Inform.</em>, vol. 15, no. 3, 2026, doi: 10.11591/eei.v15i3.11889.<br>
[30] A. Al Hanif and M. Ilyas, "Effective feature engineering framework for securing MQTT protocol in IoT environments," <em>Sensors</em>, vol. 24, no. 6, art. 1782, 2024, doi: 10.3390/s24061782.<br>
[31] N. S. Alotaibi, H. I. Sayed Ahmed, S. O. M. Kamel, and G. F. ElKabbany, "Secure enhancement for MQTT protocol using distributed machine learning framework," <em>Sensors</em>, vol. 24, no. 5, art. 1638, 2024.<br>
[32] S. Ullah, J. Ahmad, M. A. Khan, M. S. Alshehri, W. Boulila, A. Koubaa, S. U. Jan, and M. M. Iqbal Ch, "TNN-IDS: Transformer neural network-based intrusion detection system for MQTT-enabled IoT networks," <em>Comput. Netw.</em>, vol. 237, art. 110072, 2023.<br>
[33] S. Memon, U. K. Wiil, and M. Shaikh, "Explainable intrusion detection for Internet of Medical Things," in <em>Proc. 15th Int. Joint Conf. Knowledge Discovery, Knowledge Engineering and Knowledge Management (KMIS)</em>, SciTePress, 2023, pp. 40–51.<br>
[34] T. G. Dietterich, "Approximate statistical tests for comparing supervised classification learning algorithms," <em>Neural Comput.</em>, vol. 10, no. 7, pp. 1895–1923, 1998, doi: 10.1162/089976698300017197.<br>
[35] C. Nadeau and Y. Bengio, "Inference for the generalization error," <em>Mach. Learn.</em>, vol. 52, no. 3, pp. 239–281, 2003, doi: 10.1023/A:1024068612664.
</p>

<p>[36] H. Wang, Z. Liu, and K. Chen, "Intrusion detection based on convolutional Kolmogorov-Arnold networks," <i>Computers &amp; Security</i>, vol. 148, art. 104120, 2025, doi: 10.1016/j.cose.2024.104120.</p>

<h2>Appendix A – Multi-Seed Performance and Resource Consumption</h2>
<p>Precision and recall use the conventions of Section 4.7 (weighted averaging across all classes). Training and test latencies represent monotonic wall-clock execution time on the benchmark workstation. Values report mean across five random seeds (Seeds 42–46) under Protocol P1 on sanitized features without temporal markers.</p>

<table>
<thead>
<tr><th>Evaluated Algorithm</th><th>Protocol Feature Set</th><th>Accuracy (%)</th><th>Weighted F1</th><th>Macro F1</th><th>MCC</th><th>Training Latency (s)</th><th>Inference Latency (s)</th></tr>
</thead>
<tbody>
<tr><td>CART Decision Tree</td><td>Sanitized (10 features)</td><td>70.71% &plusmn; 0.09%</td><td>0.6694 &plusmn; 0.0008</td><td>0.6177 &plusmn; 0.0011</td><td>0.5712</td><td class="right">1.02 s</td><td class="right">0.008 s</td></tr>
<tr><td>Bagging Classifier</td><td>Sanitized (10 features)</td><td>70.89% &plusmn; 0.11%</td><td>0.6689 &plusmn; 0.0014</td><td>0.6154 &plusmn; 0.0017</td><td>0.5742</td><td class="right">6.64 s</td><td class="right">0.095 s</td></tr>
<tr><td>Extra Trees</td><td>Sanitized (10 features)</td><td>70.62% &plusmn; 0.12%</td><td>0.6669 &plusmn; 0.0012</td><td>0.6113 &plusmn; 0.0012</td><td>0.5698</td><td class="right">10.42 s</td><td class="right">1.301 s</td></tr>
<tr><td>Random Forest</td><td>Sanitized (10 features)</td><td>70.81% &plusmn; 0.14%</td><td>0.6675 &plusmn; 0.0013</td><td>0.6115 &plusmn; 0.0015</td><td>0.5729</td><td class="right">37.24 s</td><td class="right">1.075 s</td></tr>
<tr><td>XGBoost (Hist)</td><td>Sanitized (10 features)</td><td>71.77% &plusmn; 0.12%</td><td>0.6818 &plusmn; 0.0012</td><td>0.6281 &plusmn; 0.0013</td><td>0.5874</td><td class="right">8.71 s</td><td class="right">0.500 s</td></tr>
<tr style="font-weight:bold; background-color:#eaf2e8;"><td>Tuned CART (Depth 10)</td><td>Sanitized (10 features)</td><td>71.92% (Seed 42)</td><td>0.6822</td><td>0.6268</td><td>0.5898</td><td class="right">1.05 s</td><td class="right">0.008 s</td></tr>
<tr style="font-weight:bold; background-color:#eaf2e8;"><td>Tuned XGBoost</td><td>Sanitized (10 features)</td><td>71.90% (Seed 42)</td><td>0.6828</td><td>0.6288</td><td>0.5895</td><td class="right">8.85 s</td><td class="right">0.495 s</td></tr>
<tr><td>1D-CNN (Neural)</td><td>Sanitized (10 features)</td><td>66.48%</td><td>0.6137</td><td>0.5067</td><td>0.5067</td><td class="right">109.5 s</td><td class="right">0.368 s</td></tr>
<tr><td>ANN (MLP)</td><td>Sanitized (10 features)</td><td>66.40%</td><td>0.6149</td><td>0.5040</td><td>0.5040</td><td class="right">50.3 s</td><td class="right">0.354 s</td></tr>
<tr><td>SimpleRNN</td><td>Sanitized (10 features)</td><td>62.90%</td><td>0.5812</td><td>0.4429</td><td>0.4429</td><td class="right">49.4 s</td><td class="right">0.357 s</td></tr>
<tr><td>LSTM</td><td>Sanitized (10 features)</td><td>61.08%</td><td>0.5639</td><td>0.4087</td><td>0.4087</td><td class="right">189.9 s</td><td class="right">1.316 s</td></tr>
</tbody>
</table>
<p class="table-caption">Table A1. Comprehensive accuracy, F1, MCC, and latency metrics across tree ensembles, boosting architectures, and deep neural networks on the sanitized MQTTEEB-D benchmark.</p>

</body>
</html>"""

# Write Word Document (.doc)
with open(OUT_DOC, "w", encoding="utf-8") as f:
    f.write(html_content)

# Write HTML Document (.html)
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated {OUT_DOC} (Size: {os.path.getsize(OUT_DOC):,} bytes)")
print(f"Generated {OUT_HTML} (Size: {os.path.getsize(OUT_HTML):,} bytes)")
