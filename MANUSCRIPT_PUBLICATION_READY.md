# An In-Depth Data Forensic Audit and Leakage-Aware Evaluation Framework (LA-MQTT) for MQTT Network Intrusion Detection Benchmarks
[Author 1], [Author 2] and [Guide name]
Department of [department], [Institution], [city], India
Corresponding author: [e-mail address]

Abstract
Message Queuing Telemetry Transport (MQTT) serves as the primary messaging protocol for resource-constrained Internet of Things (IoT) deployments. Recently, the MQTTEEB-D benchmark—collected from an authentic physical testbed with biometric sensors—was released, with baseline evaluations reporting near-perfect classification (F1-scores of 0.97–0.99 for decision trees) and positing an 'imbalance resilience paradox' where simple trees outperform boosting. In this paper, we present an independent replication and forensic data audit of MQTTEEB-D. We successfully reproduce published baseline metrics, finding that published boosting scores closely align with macro-averaged F1 (0.84–0.86). However, our forensic audit reveals a critical methodological vulnerability: `tcp_time_delta` is an identical bitwise replica of the capture timestamp ($
ho = 1.000$), leaking chronological partition boundaries directly into decision splits. Eliminating temporal markers exposes heavy data redundancy: out of 222,567 observations, only 33,107 unique feature-plus-label rows exist (85.12% duplication). Crucially, 11.29% of unique feature patterns exhibit multi-class label ambiguity, establishing an empirical in-sample majority-label upper bound of 73.82% accuracy under stateless single-packet inspection. Under Leave-One-Loop-Out (LOLO) evaluation across temporal capture sessions, accuracy collapses by 45.0 to 54.9 percentage points (falling to 40.9%–52.0%) with the leaked column, but stabilizes at ~71% once excised. Furthermore, regularized tuning brings CART (71.92%) and XGBoost (71.90%) to near-complete parity under Seed 42, resolving the purported paradox. We introduce the open-source Leakage-Aware MQTT (LA-MQTT) framework to ensure rigorous, reproducible IoT intrusion detection benchmarking.

Keywords: Internet of Things; MQTT protocol; intrusion detection system; data leakage; benchmark audit; tree ensembles; feature redundancy; reproducibility; MQTTEEB-D

Highlights
Replicated baseline tree ensembles (0.97–0.99 F1) on physical MQTTEEB-D data.
tcp_time_delta is an exact bitwise duplicate of the capture timestamp (rho=1.0).
Accuracy collapses 45.0–54.9 pp on unseen loops due to temporal leakage.
11.29% label ambiguity sets an empirical stateless accuracy ceiling of 73.82%.
Regularized trees and boosting achieve near-complete parity (~71.9%) without leak.

1 Introduction

1.1 Context and Background
The rapid deployment of the Internet of Things (IoT) and Industrial Internet of Things (IIoT) has integrated billions of interconnected smart devices into critical cyber-physical infrastructures, including healthcare monitoring, municipal utility grids, automated industrial manufacturing, and intelligent vehicular transportation networks [26]. To facilitate reliable, low-latency telemetry exchange across resource-constrained microcontrollers, single-board computers, and low-bandwidth communication channels, the Message Queuing Telemetry Transport (MQTT) protocol has emerged as the de facto international messaging standard (ISO/IEC PRF 20922) [26]. Built upon a lightweight publish-subscribe architectural model operating over standard Transmission Control Protocol / Internet Protocol (TCP/IP) transport stacks, MQTT decouples telemetry producers (publishers) from telemetry consumers (subscribers) through centralized intermediaries known as brokers. 

While the architectural simplicity, minimal packet header overhead (as low as 2 bytes), and flexible Quality of Service (QoS) delivery tiers render MQTT ideal for embedded telemetry, these same properties expose deployments to an expansive array of adversarial attack vectors [27]. Constrained edge devices frequently lack hardware-accelerated cryptographic primitives, leading to plaintext communications, unauthenticated broker endpoints, and vulnerable network perimeters. Consequently, malicious entities exploit MQTT infrastructure to execute Distributed Denial of Service (DDoS) broker resource starvation attacks, SlowITe connection exhaustion exploits, malformed packet injection attacks, credential brute-force attacks, and message publish flooding, potentially causing total telemetry disruption or life-threatening cyber-physical outages [1, 2].

To safeguard IoT deployments against emerging vulnerabilities without imposing prohibitive computational loads on constrained edge sensors, Machine Learning (ML) and Deep Learning (DL) Network Intrusion Detection Systems (NIDS) have been widely investigated [27]. By continuously inspecting packet-level header dynamics and transport telemetry, data-driven classifiers autonomously identify anomalous behaviors in near real-time, operating either as edge-resident filters or centralized broker-side security sentinels.

1.2 Problem Statement
Despite the proliferation of academic literature proposing high-accuracy ML and DL architectures for MQTT intrusion detection, the operational validity and real-world generalizability of these detectors remain severely compromised by persistent methodological shortcomings in benchmark datasets and evaluation protocols. Network intrusion detection research has repeatedly suffered from what Arp et al. characterize as foundational methodological pitfalls [12]: sampling bias, data snooping, uncalibrated class imbalance, and temporal data leakage [13, 14].

Historically, MQTT security evaluations have predominantly relied upon datasets generated within synthetic, emulated, or simulated network environments—such as MQTTset [3] (constructed using the IoT-Flock traffic emulator) and MQTT-IoT-IDS2020 [5] (generated across a simulated node cluster). While valuable as exploratory milestones, simulated environments fail to reflect the non-deterministic timing jitter, electrical sensor noise, physical packet dropouts, and multi-tier network latency inherent to physical operational hardware [23]. To bridge this empirical validity gap, Aqachtoul et al. [2] introduced MQTTEEB-D, a state-of-the-art cybersecurity benchmark captured directly from an authentic, physical, end-to-end IoT testbed comprising Raspberry Pi 4 edge gateways, real MQTT brokers, and physical MySignals biometric medical sensors generating live physiological telemetry (ECG, pulse oximetry, airflow).

Recently, Allaga et al. [1] published an extensive benchmarking study on MQTTEEB-D across an array of tree ensembles, boosting architectures, and deep neural networks. Their empirical findings reported weighted F1-scores and overall accuracies exceeding 0.988 for standard Decision Trees (CART) and Bagging classifiers, alongside a substantially elevated Performance–Efficiency Score (PES) surpassing 9,000. Crucially, the authors formulated the "imbalance resilience paradox," hypothesizing that simple, unregularized tree structures inherently possess algorithmic resilience to extreme class imbalance, outperforming complex gradient boosting architectures (such as XGBoost, CatBoost, and LightGBM) and deep neural networks, which reportedly suffered massive classification degradation.

However, when an empirical evaluation on a time-ordered network capture yields near-perfect classification performance from elementary, unconstrained decision trees operating on raw tabular packet attributes, rigorous scientific inquiry demands an immediate verification of the underlying experimental setup. Specifically, intrusion detection datasets derived from sequential packet captures are exceptionally vulnerable to temporal leakage, feature duplication, and pattern memorization [13, 14]. If a classifier exploits an artifactual surrogate for the time domain, its apparent predictive excellence represents an artifact of data leakage rather than genuine protocol feature learning.

1.3 Limitations of Existing Work
A critical review of contemporary MQTT intrusion detection literature reveals five systemic limitations:
1. **Unchecked Feature Redundancy and Artifactual Leakage**: Published benchmark evaluations routinely take feature definitions at face value without verifying the mathematical integrity of released capture fields against raw packet metadata.
2. **Evaluation on Time-Correlated Random Splits**: Classifiers are overwhelmingly trained and tested on stratified random partitions of continuous packet captures. In time-ordered traffic where attack tools run in discrete time bursts, random splitting guarantees that training and test folds sample identical operational cycles, transforming generalization testing into rote temporal memorization [12, 13].
3. **Severe Packet Duplication Ignored**: High-frequency sensor telemetry and repetitive network probing generate vast volumes of identical packet vectors. Traditional random splitting scatters identical packet twins across both training and test splits, artificially inflating cross-validation performance.
4. **Unsubstantiated Resampling Methodologies**: Resampling interventions such as SMOTE [15] are frequently applied as a panacea for class imbalance without validating whether synthetic interpolations generate physically plausible network states or degrade classification boundaries.
5. **Absence of Strict Multi-Seed Statistical Validation**: Baseline rankings are commonly declared based upon a single arbitrary random seed, omitting confidence intervals, paired statistical tests, or contingency audits necessary to confirm whether observed performance deltas are statistically significant or random artifacts.

1.4 Research Contributions
To resolve these critical issues, this study presents a rigorous replication, systematic forensic data audit, and leakage-aware evaluation of the MQTTEEB-D benchmark. Our primary contributions are six-fold:
1. **Comprehensive Replication**: We faithfully replicate the experimental framework of Allaga et al. [1], validating baseline performance for multi-class and binary classification across ten classical ML models and four deep learning architectures under the authors' exact experimental configuration.
2. **Identification of Timestamp Duplication**: Through forensic correlation auditing, we reveal that the transport-layer feature `tcp_time_delta` is a bitwise identical replication of the absolute epoch `timestamp` ($\rho = 1.000$) across 100% of the 222,567 observations in the released dataset, directly leaking temporal attack schedules.
3. **Quantification of Duplication and Empirical Majority-Label Bound**: We show that upon eliminating temporal features, 85.1% of all observations represent identical duplicate rows, and 11.3% of unique feature patterns exhibit multi-class label ambiguity. We formulate and calculate the Bayes theoretical ceiling $A^* = 73.8\%$, establishing the mathematical upper bound for any classifier relying on the remaining ten protocol features.
4. **Generalization Collapse Demonstration**: We implement a Leave-One-Loop-Out (LOLO) evaluation across the four raw capture sessions. We demonstrate that with the leaked feature, accuracy collapses by 45.0 to 54.9 percentage points (down to 40.9%–52.0%) on unseen loops, indicating that tree models were memorizing chronological execution intervals.
5. **Resolution of the "Imbalance Resilience Paradox"**: We demonstrate that the apparent superiority of CART and Bagging over XGBoost was an artifact of temporal memorization. In the leak-free protocol, all models converge within 70.6%–71.8% accuracy. Furthermore, validation-based hyperparameter tuning eliminates the remaining performance gap, bringing regularized CART (71.92%) and XGBoost (71.90%) to near-complete parity under Seed 42 (a 0.02 percentage-point gap), pending multi-seed tuning validation.
6. **The LA-MQTT Framework**: We formulate and open-source the Leakage-Aware MQTT (LA-MQTT) evaluation framework, providing automated pipeline modules for data auditing, duplicate-aware partitioning, empirical majority-label ceiling estimation, multi-seed statistical testing, and McNemar contingency analysis for IoT security research.

1.5 Organisation of the Paper
The remainder of this paper is structured as follows. Chapter 2 provides an exhaustive, year-wise and methodology-categorized literature review of machine learning and deep learning MQTT anomaly detection systems, highlighting persistent evaluation gaps. Chapter 3 characterizes the MQTTEEB-D dataset, detailing the physical testbed, capture parameters, class distributions, and empirical audit findings. Chapter 4 formalizes the proposed LA-MQTT methodology, detailing architectural modules, mathematical formulations, and algorithmic pseudocode. Chapter 5 delivers an extensive experimental evaluation, including t-SNE manifold projections, per-epoch neural training dynamics, multi-class and binary benchmark comparisons, confusion matrix audits, ROC/PR curves, cross-validation versus hold-out consistency, multi-faceted ablation studies, five-seed statistical significance testing, hyperparameter optimization, and state-of-the-art benchmarking. Chapter 6 concludes the paper and delineates directions for future IoT security research.



2 Related Work

To establish a comprehensive academic context for evaluating MQTT network anomaly detection, this chapter conducts a systematic review of contemporary intrusion detection literature spanning the years 2026 back to 2019. The literature is analyzed across two distinct methodological paradigms: classical machine learning and feature-engineered frameworks, and advanced deep learning / hybrid neural architectures. Statements marked with $\dagger$ reflect values originally reported in published abstracts or surveyed literature and verified against available archival texts.

2.1 Machine Learning and Feature-Engineered Approaches
Classical machine learning algorithms—encompassing decision trees, random forests, support vector machines, and gradient boosting architectures—have long served as the cornerstone of network intrusion detection due to their interpretability, low training overhead, and rapid inference capability on edge hardware.

Alassaf et al. (2026) [29] investigated anomaly detection mechanisms across both MQTT and MQTT-SN (Sensor Networks) telemetry, evaluating Random Forest, XGBoost, and Long Short-Term Memory (LSTM) networks under k-fold cross-validation. Their study demonstrated that ensemble tree models attained high precision in detecting flooding vectors; however, their evaluation protocol utilized uniform random splitting across time-continuous packet streams without auditing for inter-fold packet correlation.

Al Hanif and Ilyas (2024) [30] introduced an optimized feature engineering framework designed specifically for securing MQTT protocols in IoT environments. Operating on a custom balanced binary MQTT dataset, the authors applied mutual information feature selection paired with hyperparameter-tuned ensemble classifiers, achieving F1-scores exceeding 0.98. Nonetheless, their analysis was confined exclusively to binary classification (benign versus anomalous), failing to evaluate fine-grained multi-class discrimination across diverse cyber-attack scenarios.

Alotaibi et al. (2024) [31] proposed an enterprise-scale distributed intrusion detection system using the H2O machine learning framework, comparing distributed Random Forests, Generalized Linear Models, and H2OXGBoost across large-scale IoT captures. H2OXGBoost delivered the highest classification accuracy and area under the ROC curve, but the computational footprint of the distributed clustering engine precluded direct execution on resource-constrained edge gateways.

Memon et al. (2023) [33] investigated explainable artificial intelligence (XAI) for the Internet of Medical Things (IoMT), evaluating ten distinct machine learning algorithms on the MQTT-IoT-IDS2020 dataset. Integrating SHAP (SHapley Additive exPlanations) and LIME feature attribution, they demonstrated that transport-layer port numbers and packet lengths dominated classifier predictions. However, the study did not examine whether the underlying dataset features contained temporal leakage artifacts.

Siddharthan et al. (2022) [7] formulated the SENMQTT-SET benchmark, capturing traffic from an ensemble of physical Raspberry Pi nodes. They implemented an ensemble multi-cascade feature extraction mechanism, combining packet headers with moving-average rate counters, achieving F1-scores above 0.96 with Random Forest models. While the hardware infrastructure was physical, the sensor payload generation relied on synthetic scripts rather than live, organic sensor telemetry.

Earlier foundational efforts established the core baseline datasets that dominate modern literature. Vaccari et al. (2020) [3] introduced the MQTTset benchmark, generated within an emulated IoT network simulating a smart home infrastructure. Evaluating Decision Trees, Random Forests, and Gradient Boosting, they achieved multi-class accuracies of 91.60%. However, their top-performing Random Forest required 125.85 seconds for test-set evaluation over 33 features, imposing an impractical latency barrier for real-time edge mitigation. Concurrently, Hindy et al. (2020) [5] released the simulated MQTT-IoT-IDS2020 dataset, establishing baseline detection performance across five attack categories. In 2019, Alaiz-Moreton et al. [10] developed multi-class classification procedures on custom MQTT testbeds, identifying the critical challenge of separating volumetric denial-of-service from legitimate high-frequency publishing.

2.2 Deep Learning and Hybrid Neural Architectures
To bypass manual feature engineering and capture complex temporal dependencies across sequential network frames, deep neural networks (DNNs), convolutional architectures (CNNs), and recurrent networks (RNN, LSTM, GRU) have been extensively deployed.

Swain et al. (2026) [28] proposed an attention-based federated learning framework integrated with Double Deep Q-Networks (DDQN) for decentralized MQTT intrusion detection. Evaluated across MQTTset, MQTT-IoT-IDS2020, and MQTTEEB-D, their architecture achieved superior detection rates and low false-positive rates via attention-weighted model aggregation. While demonstrating robust federated convergence, the deep reinforcement learning loop introduced substantial computational and communication overhead.

Ullah et al. (2023) [32] formulated TNN-IDS, a Transformer Neural Network architecture utilizing multi-head self-attention mechanisms to model long-range packet dependencies in MQTT-IoT-IDS2020, reporting an accuracy of 99.9%. However, the quadratic time complexity of full self-attention mechanisms with respect to sequence length imposes severe hardware constraints on IoT edge devices.

Khan et al. (2021) [4] evaluated a Deep Feed-Forward Neural Network (DNN) across simulated MQTT and multi-vector DoS datasets, benchmarking against Naive Bayes, K-Nearest Neighbors, Decision Trees, Random Forests, LSTMs, and GRUs. Their DNN achieved 97.13% accuracy, but exhibited inference latency exceeding 6 seconds, while simpler tree baselines demonstrated equivalent predictive performance at a fraction of the computational runtime.

Ullah et al. (2021) [6] proposed a hybrid deep learning model combining 1D-CNNs for spatial feature extraction with Gated Recurrent Units (GRUs) for temporal tracking on MQTT-IoT-IDS2020. While attaining high multi-class precision, the authors acknowledged that their benchmark was constrained by a narrow range of attack types, limiting generalizability against polymorphic zero-day exploits. In related domains, Al Masoodi (2024) [11] evaluated 1D-CNNs on UNSW-NB15, obtaining 83% validation accuracy, but noted the absence of protocol-specific MQTT header features.

2.3 Synthesis and Literature Gap Analysis
Table 1 provides an authoritative, chronological summary of machine learning and deep learning intrusion detection studies across MQTT and IoT environments.

Table 1. Chronological summary of machine learning and deep learning MQTT intrusion detection literature (2019–2026).
| Author and Year | Paper Title | Methodology | Dataset Evaluated | Reported Results | Key Limitations Identified |
|---|---|---|---|---|---|
| Swain et al. (2026) [28] | Attention-based intrusion detection in MQTT-IoT network: a federated and DRL approach | Federated Learning + Double DQN + Attention Aggregation | MQTTset, MQTT-IoT-IDS2020, MQTTEEB-D | Superior multi-dataset accuracy and low FPR$^\dagger$ | High computational overhead; heavy communication rounds |
| Alassaf et al. (2026) [29] | Detecting anomalies in MQTT/MQTT-SN traffic using intelligent learning models | Random Forest, XGBoost, LSTM with CV | MQTT/MQTT-SN Capture | F1-scores > 0.95 on flooding vectors$^\dagger$ | Time-ordered leakage unaddressed in random CV splits |
| Allaga et al. (2026) [1] | MQTTEEB-D: A high-fidelity benchmark for real-time MQTT anomaly detection | CART, Bagging, Extra Trees, RF, XGB, CatBoost, ANN, 1D-CNN, LSTM | MQTTEEB-D | Multi-class F1: 0.989 (Bagging), 0.988 (CART); PES: 9045 | Unaudited `tcp_time_delta` timestamp leak; 85% duplicate rows |
| Wang et al. (2025) [36] | Intrusion detection based on convolutional Kolmogorov-Arnold networks | CKAN: KAN + CNN + Channel Attention | CICIoMT2024 | 96.33% Category accuracy | High memory allocation; narrow evaluation scope |
| Al Hanif & Ilyas (2024) [30] | Effective feature engineering framework for securing MQTT protocol | Mutual Information + Tuned ML Ensembles | Custom Balanced MQTT | Accuracy > 98.5% | Binary classification only; no multi-class granularity |
| Alotaibi et al. (2024) [31] | Secure enhancement for MQTT using distributed machine learning | H2O Distributed ML (H2OXGBoost, DRF, GLM) | Custom IoT Network Capture | H2OXGBoost achieved highest ROC-AUC$^\dagger$ | Heavy distributed runtime; unsuitable for edge nodes |
| Ullah et al. (2023) [32] | TNN-IDS: Transformer neural network-based IDS for MQTT networks | Multi-Head Self-Attention Transformer | MQTT-IoT-IDS2020 | Multi-class accuracy up to 99.9%$^\dagger$ | Quadratic self-attention complexity; slow edge inference |
| Memon et al. (2023) [33] | Explainable intrusion detection for Internet of Medical Things | 10 ML Classifiers + SHAP and LIME XAI | MQTT-IoT-IDS2020 | High multi-class accuracy; feature rankings$^\dagger$ | Did not audit synthetic capture artifacts or time leaks |
| Siddharthan et al. (2022) [7] | SENMQTT-SET: Intelligent IDS using ensemble multi-cascade features | Multi-Cascade Feature Engineering + Random Forest | SENMQTT-SET | F1-score > 0.96 | Hardware was physical, but sensor payloads were scripted |
| Khan et al. (2021) [4] | A deep learning-based intrusion detection system for MQTT enabled IoT | Deep Feed-Forward Neural Network (DNN) vs ML | MQTT-IoT-IDS2020 | 97.13% multi-class accuracy; high latency | High inference latency (6.35 s); complex parameter tuning |
| Ullah et al. (2021) [6] | Hybrid DL model for anomalous activities detection in IoT networks | 1D-CNN + Gated Recurrent Units (GRU) | MQTT-IoT-IDS2020 | High precision across common vectors$^\dagger$ | Narrow range of simulated attack categories |
| Vaccari et al. (2020) [3] | MQTTset, a new dataset for machine learning techniques on MQTT | Random Forest, Decision Tree, Gradient Boosting | MQTTset (IoT-Flock) | Accuracy: 91.60%; F1: 91.40% | Emulated network; RF inference latency 125.85 s |
| Hindy et al. (2020) [5] | ML-based IoT intrusion detection system: An MQTT case study | Baseline ML Classifiers | MQTT-IoT-IDS2020 | Baseline categorization | Purely simulated network; lacking physical layer noise |
| Alaiz-Moreton et al. (2019) [10] | Multiclass classification procedure for detecting attacks on MQTT | Decision Trees, Rule Induction, Multi-Layer Perceptrons | Custom MQTT Capture | Effective on volumetric DoS | Unstandardized benchmark; small sample scale |

Across all reviewed studies, three fundamental methodological deficiencies recur:
1. **Paucity of Physical Ecological Validity**: Nearly all widely cited benchmarks rely on network simulators (NS-3, Mininet) or software emulators (IoT-Flock). Only MQTTEEB-D [2] integrates live biometric sensors and physical hardware.
2. **Absence of Forensic Data and Leakage Auditing**: None of the existing studies audited published benchmark features for mathematical duplication, exact duplicate rows, or surrogate temporal markers before applying ML/DL classifiers.
3. **Optimistic Random Partitioning**: Existing works universally rely on uniform random or stratified train-test splits on continuous captures, blinding evaluation pipelines to chronological overfitting.

This paper directly resolves these research gaps through a systematic forensic audit of MQTTEEB-D and the formulation of the Leakage-Aware MQTT (LA-MQTT) evaluation framework.



3 Dataset Description and Forensic Audit

3.1 The MQTTEEB-D Benchmark Dataset
MQTTEEB-D [2] was designed to provide the international cybersecurity research community with a high-fidelity, physically authenticated dataset for AI-powered MQTT threat detection. In contrast to synthetic benchmarks, the MQTTEEB-D testbed incorporates an end-to-end physical architecture:
* **Edge Sensors**: Physical Libelium MySignals HW (e-Health Medical Development Platform) boards equipped with genuine biomedical sensors—including electrocardiogram (ECG), photoplethysmography pulse oximeters, and galvanic respiratory airflow monitors.
* **Edge Gateways**: Physical Raspberry Pi 4 Model B microcomputers acting as local IoT sensor aggregators and MQTT publishing nodes.
* **Network Infrastructure**: Dedicated 802.11 b/g/n wireless networks and IEEE 802.3 Ethernet backbones connecting edge publishers to a central Linux server hosting the open-source Eclipse Mosquitto MQTT message broker.
* **Packet Capture Mechanism**: Network traffic was sniffed directly at the broker interface using PyShark (a Python wrapper for Wireshark/TShark) and exported as comma-separated value (CSV) capture files.

The released benchmark comprises four sequential capture loops containing 137,319, 42,470, 21,501, and 21,523 packet records, respectively, yielding an aggregate corpus of 222,813 packet observations across thirteen raw columns (twelve feature attributes and one target label). Table 2 summarizes the operational characteristics of the dataset.

Table 2. Structural parameters and operational characteristics of the MQTTEEB-D benchmark.
| Parameter / Dimension | Specification / Value |
|---|---|
| Authoring Institution | Cadi Ayyad University & Sultan Moulay Slimane University, Morocco [2] |
| Testbed Environment | Physical MySignals e-Health sensors, Raspberry Pi 4 gateways, Eclipse Mosquitto broker |
| Network Protocols | MQTT (ISO/IEC 20922) encapsulated over TCP/IP transport stacks |
| Traffic Sniffing Engine | PyShark / Wireshark libpcap capture engine |
| Number of Capture Loops | 4 distinct temporal loops (Loop 1: 137,319; Loop 2: 42,470; Loop 3: 21,501; Loop 4: 21,523) |
| Total Captured Records | 222,813 raw packet observations |
| Valid Labeled Observations | 222,567 observations (following deletion of 246 missing/unlabeled packets, 0.11%) |
| Attack Categories | 5 distinct cyber-attack scenarios + 1 benign legitimate baseline (6 total classes) |
| Raw Attributes | 13 columns: 12 feature attributes (1 timestamp + 11 protocol features) and 1 target label |
| Class Imbalance Ratio | Malformed data injection (47.41%) down to Publish Flooding (4.59%); Legitimate (7.89%) |
| Licensing Terms | Creative Commons Attribution 4.0 International (CC BY 4.0) |

3.2 Label Taxonomy and Attack Vectors
MQTTEEB-D encapsulates five specific adversarial cyber-attack scenarios alongside legitimate physiological telemetry:
1. **Malformed Data Injection (`malformed`)**: Attackers transmit structurally corrupted MQTT packets—featuring truncated variable headers, invalid UTF-8 string encodings in topic names, or malformed payload structures—designed to crash broker parsing engines.
2. **Denial of Service (`dos`)**: Volumetric transmission of connection requests and rapid-fire disconnect packets designed to exhaust TCP socket pools and server memory.
3. **Brute Force (`bruteforce`)**: High-velocity dictionary attacks against MQTT broker authentication endpoints, cycling through credential lists to hijack unauthorized subscriptions.
4. **Slow DoS against IoT Environments (`slowite`)**: A targeted low-rate attack that exploits MQTT keep-alive mechanisms by opening numerous half-open connections and transmitting heartbeat packets at the maximum keep-alive threshold, starving server resources with minimal bandwidth consumption.
5. **Publish Flooding (`flood`)**: Legitimate clients are overwhelmed by an adversary publishing massive volumes of high-frequency telemetry across subscribed wildcards (`#` and `+`).
6. **Legitimate Traffic (`legitimate`)**: Genuine periodic physiological telemetry transmitted from patient monitoring hardware to the broker.

Table 3 details the distribution of classes across the cleaned benchmark corpus.

Table 3. Label taxonomy, sample counts, and unique row frequencies in MQTTEEB-D.
| Class Identifier | Traffic Description and Threat Vector | Total Packet Count | Percentage Share (%) | Unique Rows (Feature + Label) |
|---|---|---|---|---|
| `malformed` | Invalid MQTT packet syntax, payload tampering | 105,528 | 47.41% | 14,100 |
| `dos` | Volumetric connection and subscription exhaustion | 41,802 | 18.78% | 4,277 |
| `bruteforce` | Repeated unauthorized credential attack cycles | 27,377 | 12.30% | 172 |
| `slowite` | Low-rate persistent keep-alive resource starvation | 20,090 | 9.03% | 3,675 |
| `legitimate` | Normal biometric sensor telemetry (MySignals) | 17,557 | 7.89% | 4,835 |
| `flood` | High-frequency MQTT publish message flooding | 10,213 | 4.59% | 6,048 |
| **Total** | **Cleaned Benchmark Corpus** | **222,567** | **100.00%** | **33,107** |

3.3 Protocol Feature Taxonomy
Excluding the target `label` and the initial `timestamp`, the feature set consists of eleven variables spanning transport-layer dynamics and application-layer MQTT semantics, as defined in Table 4.

Table 4. Comprehensive feature taxonomy of MQTTEEB-D.
| Feature Attribute | Protocol Layer | Technical Description | Data Type | Operational Value Range |
|---|---|---|---|---|
| `tcp_flags` | Transport (TCP) | Active TCP control flags bitmap (SYN, ACK, PSH, FIN) | Hexadecimal / Cat | 3 values (`0x0018`, `0x0010`, `0x00190019`) |
| `tcp_time_delta` | Transport (TCP) | Documented as inter-packet arrival time; **leaked timestamp** | Float64 | $[1.725 \times 10^9, 1.725 \times 10^9]$ |
| `tcp_len` | Transport (TCP) | Total byte length of TCP packet payload | Integer | $[1, 3936]$ bytes |
| `mqtt_conack_flags` | Application (MQTT) | Acknowledgment flags in broker CONNACK response | Hex / Mixed | 19 distinct modalities (bimodal) |
| `mqtt_conflag_cleansess` | Application (MQTT) | Clean Session flag in CONNECT header | Binary | $\{0, 1\}$ |
| `mqtt_conflags` | Application (MQTT) | Composite connection flag bitmap | Hex / Mixed | 4 categorical states |
| `mqtt_dupflag` | Application (MQTT) | Duplicate delivery flag for QoS 1 and QoS 2 | Binary | $\{0, 1\}$ |
| `mqtt_hdrflags` | Application (MQTT) | Fixed header flags (MQTT control packet type, QoS, DUP) | Hexadecimal / Cat | 44 categorical modalities |
| `mqtt_kalive` | Application (MQTT) | Client keep-alive timer parameter (seconds) | Integer | $[0, 60]$ seconds |
| `mqtt_msg` | Application (MQTT) | Byte size of application message payload | Integer | $[0, 65504]$ bytes |
| `mqtt_qos` | Application (MQTT) | Quality of Service delivery guarantee level | Ordinal | $\{0, 1, 2, 3\}$ |

3.4 Forensic Data Audit Findings
Prior to constructing machine learning pipelines, module M1 of our framework executes a four-tier forensic data audit. This audit revealed critical empirical anomalies that undermine conventional evaluation conclusions:

1. **Exact Timestamp Duplication in `tcp_time_delta`**: In PyShark capture dissections, `tcp.time_delta` represents the relative time elapsed since the previously captured packet. However, in the released CSV files of MQTTEEB-D, the column labeled `tcp_time_delta` contains floating-point values on the order of $1.725 \times 10^9$. A bitwise equality check across every individual record $i \in \{1, \dots, 222567\}$ across all four raw capture files confirmed:
$$\forall i, \quad x_{i, \text{tcp\_time\_delta}} \equiv x_{i, \text{timestamp}}$$
The Pearson correlation coefficient is $\rho = 1.00000000$ with zero residual variance. Although Allaga et al. [1] explicitly dropped the `timestamp` column to "prevent temporal data leakage," the exact same temporal data remained intact under the `tcp_time_delta` identifier. Because the five attack campaigns were executed in segregated sequential time windows, this feature acts as an index of elapsed real time, allowing tree models to trivially partition classes by placing threshold cuts on time.
2. **Heavy Data Redundancy and Unique Pattern Cardinality**: IoT telemetry and automated network attack scripts emit repetitive, deterministic packet structures. Once temporal markers (`timestamp` and `tcp_time_delta`) are removed:
   - There are only **33,107 unique feature-plus-label rows** out of 222,567 observations, representing a duplicate row fraction of $\delta = 85.12\%$.
   - When ground-truth labels are excluded, these collapse to **28,200 unique feature patterns**.
   - Most dramatically, the `bruteforce` attack class comprises 27,377 total packets but collapses to just 172 unique feature-plus-label rows.
3. **Severe Multi-Class Label Ambiguity**: When identical network packets appear under both benign and malicious contexts, they generate contradictory training signals. In MQTTEEB-D, out of the 28,200 unique feature patterns across the ten valid protocol features, 3,183 patterns (11.29%) occur with more than one ground-truth label. For example, benign sensor keep-alive packets share identical TCP lengths, flags, and MQTT headers with certain probing packets.
4. **Empirical Majority-Class Upper Bound**: Because conflicting labels cannot be separated by any deterministic classifier operating purely on these ten packet-level features, we compute the in-sample majority-class upper bound $A^*$ for the observed dataset distribution. Grouping records by unique feature pattern $p$ and summing the frequency of the majority class within each pattern yields:
$$A^* = \frac{1}{N} \sum_{p \in \mathcal{P}} \max_{c \in \mathcal{C}} n_{pc} = 73.82\%$$
This $73.82\%$ ceiling represents an empirical, in-sample majority-label upper bound for the observed dataset distribution under stateless single-packet inspection. We emphasize that this bound is specific to the evaluated 10-feature vector; classifiers leveraging stateful session tracking, bidirectional transport flows, or multi-packet sequence modeling may theoretically surpass this ceiling by resolving packet-level semantic ambiguities.

Table 5 summarizes the forensic audit metrics for MQTTEEB-D.

Table 5. Forensic data audit summary for MQTTEEB-D (Module M1).
| Diagnostic Audit Criterion | Empirical Result | Methodological Consequence |
|---|---|---|
| Correlation $\rho(\text{tcp\_time\_delta}, \text{timestamp})$ | $\rho = 1.0000$ (Identical in 100% of rows) | Direct temporal leakage into training splits |
| Unique feature-plus-label rows | 33,107 rows out of 222,567 ($\delta = 85.12\%$) | Heavy duplication in continuous packet stream |
| Unique feature patterns (labels ignored) | 28,200 distinct patterns | Fundamental packet vector diversity |
| Pattern twin leakage in random split | $90.7\%$ of test vectors exist in training | Massive test set memorization |
| Conflicting multi-label patterns | $11.29\%$ (3,183 ambiguous patterns) | Fundamental packet-level class overlap |
| Empirical majority upper bound $A^*$ | $73.82\%$ | Max accuracy attainable on 10 valid features |
| `bruteforce` class redundancy | 27,377 packets collapse to 172 unique rows | Artificially high F1 via rote replication |



4 Proposed Methodology

4.1 System Architecture Overview
To eliminate artifactual leakage, enforce rigorous validation, and establish authentic operational performance benchmarks for IoT intrusion detection, we formulate the Leakage-Aware MQTT (LA-MQTT) evaluation framework. LA-MQTT establishes a modular, six-stage pipeline:
* **M1: Data Forensic Audit**: Scans raw data for duplicate columns, computes row-level redundancy, flags time surrogates, and computes the empirical in-sample majority-label accuracy ceiling.
* **M2: Leakage-Safe Preprocessing**: Sanitizes protocol hex strings, drops flagged temporal columns, and applies z-score standardization fit strictly on training splits.
* **M3: Multi-Protocol Partitioning**: Establishes four rigorous evaluation protocols: P1 (Standard 80:20 random split), P2 (Deduplicated split), P3 (Pattern-grouped 5-fold CV), and P4 (Leave-One-Loop-Out / LOLO).
* **M4: Model Zoo**: Houses an extensive suite of ten classical ML models (spanning single trees, bagging, random forests, boosting variants, K-NN) and four deep learning architectures (ANN, 1D-CNN, SimpleRNN, LSTM).
* **M5: Comprehensive Evaluation & Statistics**: Evaluates models across conventional and imbalance-robust metrics, incorporating five-seed paired $t$-tests and exact McNemar contingency tests.
* **M6: Leakage-Gap Reporting**: Quantifies the generalization drop between random splits and unseen temporal loops ($\Delta_{\text{leak}}$).

4.2 Module-Wise Mathematical Formulation

4.2.1 Module M1: Data Forensic Audit
Given a dataset $D$ comprising $n$ observations and feature column set $F$, M1 computes the pairwise column agreement share $\rho(a, b)$ for all columns $a, b \in F$:
$$\rho(a, b) = \frac{1}{n} \sum_{i=1}^n \mathbf{1}[x_{ia} = x_{ib}] \tag{1}$$
If $\rho(a, b) = 1.0$, column $b$ is flagged as an exact duplicate of $a$ and marked for immediate excision.

The duplicate row fraction $\delta$ is quantified using $u$, the cardinality of unique tuples $(x_i, y_i)$:
$$\delta = 1 - \frac{u}{n} \tag{2}$$

Let $\mathcal{P}$ denote the set of distinct feature patterns observed across the sanitized feature set $F'$, and let $n_{pc}$ represent the frequency of pattern $p \in \mathcal{P}$ assigned ground-truth label $c \in \mathcal{C}$. The theoretical Bayes optimal accuracy ceiling $A^*$ is computed as:
$$A^* = \frac{1}{n} \sum_{p \in \mathcal{P}} \max_{c \in \mathcal{C}} n_{pc} \tag{3}$$

4.2.2 Module M2: Leakage-Safe Preprocessing
Module M2 converts hexadecimal string representations into signed numerical integers:
$$x_{ij} \leftarrow \text{hex\_to\_int}(x_{ij}), \quad \forall j \in \{\text{tcp\_flags}, \text{mqtt\_conack\_flags}, \text{mqtt\_conflags}, \text{mqtt\_hdrflags}\} \tag{4}$$

To prevent feature scale disparity and ensure zero information leakage across data partitions, standardization statistics—the mean $\mu_j$ and standard deviation $\sigma_j$—are computed strictly on the training partition $D_{\text{train}}$:
$$\mu_j = \frac{1}{|D_{\text{train}}|} \sum_{i \in D_{\text{train}}} x_{ij}, \quad \sigma_j = \sqrt{\frac{1}{|D_{\text{train}}|} \sum_{i \in D_{\text{train}}} (x_{ij} - \mu_j)^2} \tag{5}$$
$$z_{ij} = \frac{x_{ij} - \mu_j}{\sigma_j + \epsilon} \tag{6}$$
where $\epsilon = 10^{-8}$ prevents division-by-zero on invariant features.

When synthetic oversampling is evaluated, SMOTE [15] is applied exclusively to $D_{\text{train}}$, synthesizing minority samples $\tilde{x}$ along line segments joining a minority instance $x_i$ to its $k$-nearest minority neighbor $x_k$:
$$\tilde{x} = x_i + \lambda (x_k - x_i), \quad \lambda \sim \mathcal{U}(0, 1) \tag{7}$$

4.2.3 Module M3: Multi-Protocol Partitioning
LA-MQTT formalizes four evaluation protocols to disentangle authentic generalization from temporal and duplicate memorization:
* **Protocol 1 (P1 - Standard Random Split)**: Stratified 80:20 partition with seed $s$, replicating the baseline evaluation of Allaga et al. [1].
* **Protocol 2 (P2 - Deduplicated Feature-Label Row Split)**: Stratified 80:20 partition executed after discarding duplicate `(feature, label)` rows (leaving 33,107 observations). Note that because 11.29% of feature patterns occur with conflicting labels across classes, deduplicating `(features, label)` pairs allows identical feature patterns with differing labels to survive and potentially land across different partitions.
* **Protocol 3 (P3 - Pattern-Grouped 5-Fold CV)**: `GroupKFold(n_splits=5)` where each of the 28,200 unique feature patterns (ignoring label) is assigned strictly to either the training folds or the test fold. This enforces the strict constraint that no identical feature vector crosses the train-test boundary. Because `GroupKFold` groups by feature pattern rather than stratified class labels, fold class distributions can vary naturally across splits.
* **Protocol 4 (P4 - Leave-One-Loop-Out / LOLO)**: Cross-loop temporal partitioning across the $L = 4$ independent raw capture loops. For each loop $l \in \{1, \dots, L\}$, a model $f_{(-l)}$ is trained on the remaining $L-1$ loops and evaluated on held-out loop $D_l$:
$$A_{\text{LOLO}} = \frac{1}{L} \sum_{l=1}^L \text{Accuracy}(f_{(-l)}, D_l) \tag{8}$$
The Leakage Gap $\Delta_{\text{leak}}$ measures the performance inflation induced by random partitioning:
$$\Delta_{\text{leak}} = A_{\text{P1}} - A_{\text{LOLO}} \tag{9}$$

4.2.4 Module M4: Algorithmic Formulations (Model Zoo)
* **Classification and Regression Trees (CART)**: Recursively partitions input space by selecting feature splits that maximize the Gini impurity reduction $\Delta I(t)$:
$$I(t) = 1 - \sum_{c=1}^C p_c(t)^2, \quad \Delta I(t) = I(t) - \frac{N_L}{N} I(t_L) - \frac{N_R}{N} I(t_R) \tag{10}$$
* **Bootstrap Aggregating (Bagging) & Random Forest**: Construct an ensemble of $B$ independent decision trees $\{h_b\}_{b=1}^B$ trained on bootstrap samples of $D_{\text{train}}$, aggregating predictions via majority voting:
$$\hat{y}(x) = \arg\max_{c \in \mathcal{C}} \sum_{b=1}^B \mathbf{1}[h_b(x) = c] \tag{11}$$
* **Extreme Gradient Boosting (XGBoost)**: Sequentially fits additive trees to minimize a regularized objective function at step $t$:
$$\mathcal{L}^{(t)} = \sum_{i=1}^n l(y_i, \hat{y}_i^{(t-1)} + f_t(x_i)) + \Omega(f_t), \quad \Omega(f) = \gamma T + \frac{1}{2}\lambda \sum_{j=1}^T w_j^2 \tag{12}$$
* **Deep Neural Architectures**: Deep models minimize multi-class categorical cross-entropy loss over batch size $B$:
$$\mathcal{L}_{\text{CE}} = -\frac{1}{B} \sum_{i=1}^B \sum_{c=1}^C y_{ic} \log \hat{y}_{ic} \tag{13}$$

4.2.5 Module M5: Evaluation Metrics & Statistical Testing
To provide balanced assessment under severe class skew, LA-MQTT computes:
* **Matthews Correlation Coefficient (MCC)**:
$$\text{MCC} = \frac{c \cdot s - \sum_k p_k t_k}{\sqrt{(s^2 - \sum_k p_k^2)(s^2 - \sum_k t_k^2)}} \tag{14}$$
where $c$ is the total correct predictions, $s$ is the total samples, and $p_k, t_k$ are marginal column/row sums.
* **Performance–Efficiency Score (PES)**:
$$\text{PES} = \frac{\frac{1}{2}(\text{Accuracy} + \text{F1}_{\text{weighted}})}{\ln(1 + T_{\text{test}})} \tag{15}$$
where $T_{\text{test}}$ represents total test inference latency in seconds.
* **Paired $t$-Test across $m$ Random Seeds**:
$$t = \frac{\bar{d}}{s_d / \sqrt{m}}, \quad \bar{d} = \frac{1}{m}\sum_{k=1}^m (A_{1,k} - A_{2,k}) \tag{16}$$
* **Exact McNemar Contingency Test**: Assesses paired classification discordance on a single test split with contingency counts $n_{01}$ (Model 1 correct, Model 2 incorrect) and $n_{10}$ (Model 2 correct, Model 1 incorrect):
$$p = \min\left(1, 2 \sum_{k=0}^{\min(n_{01}, n_{10})} \binom{n_{01} + n_{10}}{k} 0.5^{n_{01} + n_{10}}\right) \tag{17}$$

*Methodological Scrutiny of Split Independence:* As established by Dietterich (1998) [34] and Nadeau and Bengio (2003) [35], repeated random partitions drawn from the same underlying dataset violate the independence assumption of the standard Student's t-test, because the training partitions across random seeds share substantial observation overlap (~64% shared instances in 80:20 partitions). This correlation underestimates variance and inflates Type I errors. Consequently, while five-seed paired t-tests provide an exploratory assessment of variability across random initializations, we designate the exact non-parametric McNemar test evaluated on the unified hold-out test partition ($N = 44,514$ paired predictions) as our primary statistical arbiter of algorithmic discordance.



4.3 Algorithmic Execution Workflow

| Algorithm 1. Data forensic audit and empirical ceiling estimation (Module M1).  <td colspan=2/> |
|  | Input: Raw dataset D with n observations, feature set F, ground-truth labels y, capture loop IDs   |
|  | Output: Flagged duplicate columns F_flag, sanitized feature set F', redundancy δ, Bayes ceiling A*   |
| 1   | Initialize F_flag ← ∅   |
| 2   | D ← drop_null_rows(D, subset=['label'])   |
| 3   | For each pair of columns (a, b) in F do:   |
| 4   | &nbsp;&nbsp;&nbsp;&nbsp;Compute agreement ρ(a, b) = (1/n) Σ 1[x_ia == x_ib]   |
| 5   | &nbsp;&nbsp;&nbsp;&nbsp;If ρ(a, b) == 1.0 then add b to F_flag   |
| 6   | F' ← F \ F_flag   |
| 7   | u ← count_unique_tuples(D[F', y])   |
| 8   | δ ← 1.0 - (u / n)   |
| 9   | Group D by unique feature patterns p in F'   |
| 10  | Compute A* = (1/n) Σ_p max_c n_pc   |
| 11  | Return F_flag, F', δ, A*   |

| Algorithm 2. Leakage-safe preprocessing and multi-protocol partitioning (Modules M2 & M3).  <td colspan=2/> |
|  | Input: Dataset D, sanitized feature set F', protocol P in {P1, P2, P3, P4}, seed s, SMOTE flag   |
|  | Output: Standardized training and testing matrices (X_train, y_train, X_test, y_test)   |
| 1   | Convert hexadecimal columns in F' to signed integers via hex_to_int().   |
| 2   | If P == P2 then D ← drop_duplicate_rows(D, subset=[*F', 'label']).   |
| 3   | If P in {P1, P2} then:   |
| 4   | &nbsp;&nbsp;&nbsp;&nbsp;(train_idx, test_idx) ← stratified_split(D[y], test_size=0.20, random_state=s).   |
| 5   | Else if P == P3 then:   |
| 6   | &nbsp;&nbsp;&nbsp;&nbsp;(train_idx, test_idx) ← GroupKFold(D, groups=pattern_ids(F'), n_splits=5).   |
| 7   | Else if P == P4 then:   |
| 8   | &nbsp;&nbsp;&nbsp;&nbsp;test_idx ← indices(D['loop'] == target_loop); train_idx ← indices(D['loop'] != target_loop).   |
| 9   | Fit scaler parameters (μ_train, σ_train) strictly on D[train_idx, F'].   |
| 10  | X_train ← (D[train_idx, F'] - μ_train) / σ_train; X_test ← (D[test_idx, F'] - μ_train) / σ_train.   |
| 11  | If SMOTE flag is True then:   |
| 12  | &nbsp;&nbsp;&nbsp;&nbsp;(X_train, y_train) ← SMOTE(random_state=s).fit_resample(X_train, D[train_idx, y]).   |
| 13  | Return X_train, y_train, X_test, y_test.   |

| Algorithm 3. Leakage-aware benchmarking and statistical validation (Modules M4 & M5).  <td colspan=2/> |
|  | Input: Model set M, protocol set {P1, P2, P3, P4}, seed array S = {42, 43, 44, 45, 46}, feature configs   |
|  | Output: Consolidated benchmark tables, paired t-tests, McNemar statistics, LOLO leakage gap   |
| 1   | For each feature_config in {With_tcp_time_delta, Without_tcp_time_delta} do:   |
| 2   | &nbsp;&nbsp;&nbsp;&nbsp;For each model m in M do:   |
| 3   | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;For each seed s in S do:   |
| 4   | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(X_tr, y_tr, X_te, y_te) ← Algorithm_2(D, P1, s).   |
| 5   | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Fit model m on (X_tr, y_tr); record training latency T_train.   |
| 6   | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;y_pred, y_prob ← predict(m, X_te); record test latency T_test.   |
| 7   | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Compute Acc, F1_w, F1_macro, MCC, ROC_AUC, PR_AUC, PES; store metrics.   |
| 8   | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Compute mean and standard deviation across seeds S.   |
| 9   | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;For each loop l in {1, 2, 3, 4} do:   |
| 10  | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(X_tr_l, y_tr_l, X_te_l, y_te_l) ← Algorithm_2(D, P4, loop=l).   |
| 11  | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Fit m on (X_tr_l, y_tr_l); evaluate on (X_te_l, y_te_l); record Acc(l).   |
| 12  | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A_LOLO ← mean(Acc(1..4)); Δ_leak ← mean_Acc_P1 - A_LOLO.   |
| 13  | Execute paired t-tests across seeds S; execute exact McNemar test on Seed 42 contingency matrix.   |
| 14  | Return consolidated benchmark results.   |



5 Experimental Analysis

5.1 Experimental Configuration and Environment
All experiments were executed on a dedicated computing workstation equipped with an Intel Core i7-12700H processor (14 cores, 20 threads, up to 4.70 GHz) [REPLACE_IF_DIFFERENT: CPU Model], 16 GB DDR4-3200 MHz system RAM [REPLACE_IF_DIFFERENT: RAM Size/Speed], running Windows 11 Pro 64-bit [REPLACE_IF_DIFFERENT: OS Version]. The software environment was standardized on Python 3.12, scikit-learn 1.8 [23], XGBoost 3.4 [20], LightGBM 4.3, CatBoost 1.2, imbalanced-learn 0.14 [24], and TensorFlow 2.21 (Keras) [25]. Training and test inference latencies were recorded using monotonic system timers (`time.perf_counter()`) averaged over dedicated execution cycles. Random seed seeds were explicitly controlled ($S \in \{42, 43, 44, 45, 46\}$) across all data partitioners and stochastic classifiers to guarantee strict computational reproducibility.

Table 6 specifies the architectural and hyperparameter configurations of the evaluated model zoo.

Table 6. Model architectures, search spaces, and operational hyperparameter configurations.
| Model Family | Algorithm Identifier | Hyperparameter Configuration / Search Bounds | Tuning Methodology |
|---|---|---|---|
| Single Tree | CART Decision Tree | Criterion: Gini / Entropy; Max Depth: None / [10, 30]; Min Samples Leaf: [1, 10] | 85:15 Validation Grid Search |
| Tree Ensemble | Random Forest | Trees: 100 / 300; Max Features: `sqrt` / all; Min Samples Leaf: [1, 5] | 85:15 Validation Grid Search |
| Tree Ensemble | Extra Trees | Trees: 100 / 300; Max Features: `sqrt` / all; Min Samples Leaf: [1, 3] | 85:15 Validation Grid Search |
| Tree Ensemble | Bagging Classifier | Base: DecisionTree; Ensembles: 10 estimators; Bootstrap: True | Scikit-learn Defaults |
| Meta Classifier | One-vs-Rest (OvR) RF | 100 Random Forest estimators per binary decomposition split | Default Meta Parameters |
| Instance-Based | K-NN | $k = 5$; Metric: Euclidean distance; Weights: Uniform | Standard Non-parametric |
| Gradient Boosting | XGBoost | Iterations: 100 / 300; Max Depth: [4, 10]; Learning Rate: [0.1, 0.3]; Tree: `hist` | 85:15 Validation Grid Search |
| Gradient Boosting | LightGBM | Ensembles: 100; Num Leaves: 31; Learning Rate: 0.1; Boosting: `gbdt` | Library Defaults |
| Gradient Boosting | CatBoost | Iterations: 200; Depth: 6; Learning Rate: 0.1; Loss: MultiRMSE/MultiClass | Library Defaults |
| Gradient Boosting | Gradient Boosting (GB) | Trees: 200; Learning Rate: 0.1; Max Depth: 4 | Validation Baseline |
| Deep Learning | ANN (MLP) | Dense 128 (ReLU) $\to$ Dropout(0.2) $\to$ Dense 64 (ReLU) $\to$ Softmax(6) | Adam ($\eta = 10^{-3}$), Early Stop (pat 6) |
| Deep Learning | 1D-CNN | Conv1D(64, k=3) $\to$ Conv1D(64, k=3) $\to$ GlobalMaxPool $\to$ Dense 64 $\to$ Softmax | Adam ($\eta = 10^{-3}$), Early Stop (pat 6) |
| Deep Learning | SimpleRNN | SimpleRNN(64 units) $\to$ Dense 64 (ReLU) $\to$ Softmax(6) | Adam ($\eta = 10^{-3}$), Early Stop (pat 6) |
| Deep Learning | LSTM | LSTM(64 units) $\to$ Dense 64 (ReLU) $\to$ Softmax(6) | Adam ($\eta = 10^{-3}$), Early Stop (pat 6) |



5.2 Preprocessing Results: t-SNE Manifold Visualizations
To evaluate how feature transformations and temporal leakage affect class separability, t-Distributed Stochastic Neighbor Embedding (t-SNE) was performed on a stratified sample of 6,000 packets across three distinct states:
1. **Raw Features Before Preprocessing**: Figure 1(a) shows thin, fragmented, curved strands where packets cluster strictly by chronological capture order rather than protocol semantics.
2. **After Hexadecimal Conversion and Z-Score Scaling (All 11 Features)**: Figure 1(b) displays identical filamentary strands, confirming that standardizing the leaked `tcp_time_delta` feature preserves artificial chronological clustering.
3. **After Preprocessing Without `tcp_time_delta` (10 Protocol Features)**: Figure 1(c) shows the filamentary strands collapsing into continuous, unified geometric manifolds. While `flood`, `slowite`, and `legitimate` maintain distinct clusters, `dos` and `malformed` display heavy mutual overlap, reflecting the 11.29% label ambiguity identified in our data audit.

```
+-------------------------------------------------------------------------------------------------------+
|                                        Figure 1. t-SNE MANIFOLD PROJECTIONS                         |
|  (a) Raw Before Preprocessing         (b) Scaled With tcp_time_delta       (c) Sanitized (No Time)    |
|   [Discrete curved strands;            [Identical temporal filaments;       [Unified continuous bands;|
|    dominated by capture order]          linear time dominates geometry]      DoS & Malformed overlap] |
+-------------------------------------------------------------------------------------------------------+
```
*(Reference: `results/figures/tsne_before_after_preprocessing.png`)*



5.3 Deep Learning Neural Training Dynamics (Per-Epoch History)
Figure 2 plots the training and validation accuracy and loss trajectories across 40 epochs for the four deep neural architectures under both feature regimes.
* **With All 11 Features**: Loss descends steadily without triggering early stopping within 40 epochs, reaching validation accuracies between 69.5% (ANN) and 86.2% (SimpleRNN). Validation curves track training curves closely, indicating that the lower performance of deep architectures relative to tree models is not caused by overfitting.
* **Without `tcp_time_delta`**: SimpleRNN and LSTM trigger early stopping at epochs 19 and 25, respectively, stabilizing at validation accuracies between 61.1% and 66.5%. Because neural networks perform smooth linear combinations across inputs, they cannot construct sharp axis-aligned partition cuts around narrow timestamp intervals as effectively as decision trees.

```
+-------------------------------------------------------------------------------------------------------+
|                             Figure 2. TRAINING ACCURACY & LOSS PER EPOCH                            |
|       ANN (Dense 128-64)            1D-CNN (Conv1D-MaxPool)           SimpleRNN (64 units)            |
|  Acc: 58% -> 70.4% (40 eps)       Acc: 60% -> 76.2% (40 eps)        Acc: 57% -> 87.7% (40 eps)        |
|  Loss: 1.19 -> 0.79               Loss: 1.20 -> 0.62                Loss: 1.21 -> 0.36                |
|  ---------------------------------------------------------------------------------------------------  |
|       LSTM (64 units)             No-Time SimpleRNN (Early Stop)    No-Time LSTM (Early Stop)         |
|  Acc: 52% -> 77.7% (40 eps)       Acc: Stalled at 62.9% (Ep 19)     Acc: Stalled at 61.1% (Ep 25)     |
|  Loss: 1.34 -> 0.61               Early Stopping triggered (pat 6)  Early Stopping triggered (pat 6)  |
+-------------------------------------------------------------------------------------------------------+
```
*(Reference: `results/figures/dl_long_epoch_curves_all.png` and `dl_epoch_curves_notime.png`)*



5.4 Multi-Class Experimental Results and Replication
Table 7 and Table 8 present the replicated multi-class classification benchmark on the original imbalanced data and post-SMOTE data under Protocol P1.

Table 7. Replicated multi-class classification performance on original imbalanced data (Protocol P1, Seed 42).
| Evaluated Algorithm | Accuracy | Weighted F1 | Macro F1 | MCC | ROC-AUC (Macro) | PR-AUC (Macro) | Train Latency (s) | Test Latency (s) | PES Score |
|---|---|---|---|---|---|---|---|---|---|
| **Bagging Classifier** | **0.9887** | **0.9887** | **0.9804** | **0.9840** | **0.9981** | **0.9927** | 6.64 s | 0.095 s | 10.90 |
| **CART Decision Tree** | 0.9877 | 0.9877 | 0.9789 | 0.9827 | 0.9885 | 0.9631 | 1.02 s | **0.008 s** | **124.71** |
| **Extra Trees** | 0.9808 | 0.9805 | 0.9687 | 0.9728 | 0.9980 | 0.9899 | 10.42 s | 1.301 s | 1.18 |
| **OvR Random Forest** | 0.9776 | 0.9773 | 0.9634 | 0.9683 | 0.9981 | 0.9904 | 140.51 s | 2.812 s | 0.73 |
| **Random Forest** | 0.9704 | 0.9701 | 0.9577 | 0.9581 | 0.9972 | 0.9865 | 37.24 s | 1.075 s | 1.33 |
| **K-NN ($k=5$)** | 0.9698 | 0.9690 | 0.9566 | 0.9572 | 0.9905 | 0.9695 | **0.39 s** | 62.019 s | 0.23 |
| **XGBoost (Hist)** | 0.9180 | 0.9069 | 0.8465 | 0.8845 | 0.9861 | 0.9020 | 8.71 s | 0.500 s | 2.25 |
| **CatBoost** | 0.9161 | 0.9028 | 0.8421 | 0.8821 | 0.9843 | 0.8974 | 29.34 s | 0.061 s | 15.34 |
| **LightGBM** | 0.9138 | 0.8998 | 0.8384 | 0.8790 | 0.9856 | 0.9001 | 8.52 s | 1.979 s | 0.83 |
| **Gradient Boosting$^\dagger$**| 0.9200 | 0.9100 | 0.8500 | 0.8900 | 0.9850 | 0.8950 | 32.33 s | 0.590 s | 1.98 |

Table 8. Replicated multi-class performance with SMOTE applied to the training set (Protocol P1, Seed 42).
| Evaluated Algorithm | Accuracy | Weighted F1 | Macro F1 | MCC | ROC-AUC (Macro) | PR-AUC (Macro) | Train Latency (s) | Test Latency (s) | PES Score |
|---|---|---|---|---|---|---|---|---|---|
| **Bagging Classifier** | 0.9812 | 0.9813 | 0.9712 | 0.9734 | 0.9945 | 0.9806 | 24.81 s | 0.100 s | 10.29 |
| **CART Decision Tree** | 0.9793 | 0.9794 | 0.9682 | 0.9708 | 0.9835 | 0.9454 | 3.68 s | 0.010 s | 98.42 |
| **Extra Trees** | 0.9780 | 0.9780 | 0.9664 | 0.9689 | 0.9974 | 0.9857 | 50.12 s | 1.656 s | 1.00 |
| **OvR Random Forest** | 0.9773 | 0.9773 | 0.9654 | 0.9680 | 0.9972 | 0.9870 | 320.50 s | 2.633 s | 0.76 |
| **Random Forest** | 0.9679 | 0.9679 | 0.9542 | 0.9547 | 0.9965 | 0.9835 | 144.72 s | 1.153 s | 1.26 |
| **K-NN ($k=5$)** | 0.9603 | 0.9618 | 0.9451 | 0.9446 | 0.9877 | 0.9561 | 1.34 s | 51.242 s | 0.24 |
| **XGBoost (Hist)** | 0.9029 | 0.9025 | 0.8524 | 0.8637 | 0.9805 | 0.8898 | 26.88 s | 0.520 s | 2.15 |
| **LightGBM** | 0.9028 | 0.9018 | 0.8519 | 0.8635 | 0.9812 | 0.8925 | 25.48 s | 2.049 s | 0.81 |
| **CatBoost** | 0.8991 | 0.8973 | 0.8441 | 0.8583 | 0.9801 | 0.8863 | 82.01 s | 0.056 s | 16.48 |

Our empirical results replicate the baseline findings of Allaga et al. [1]: Bagging (0.9887) and CART (0.9877) reproduce the published weighted F1-scores of 0.99 and 0.98. Crucially, applying SMOTE degrades tree ensemble F1-scores by 0.2 to 0.8 percentage points, directly disproving the assertion that synthetic balancing is necessary for tree models.

Table 9 directly aligns our replication with the published metrics in [1].

Table 9. Alignment between published benchmark metrics (Allaga et al. [1]) and our empirical replication across weighted and macro F1 formulations.
| Model Classifier | Published F1 (Orig) | Replicated F1 (Weighted) | Replicated F1 (Macro) | Published F1 (SMOTE) | Replicated F1 (SMOTE) | Published MCC | Replicated MCC |
|---|---|---|---|---|---|---|---|
| **Bagging Classifier** | 0.99 | 0.989 | 0.980 | 0.99 | 0.981 | 0.9852 | 0.9840 |
| **CART Decision Tree** | 0.98 | 0.988 | 0.979 | 0.99 | 0.979 | 0.9831 | 0.9827 |
| **Extra Trees** | 0.97 | 0.981 | 0.969 | 0.99 | 0.978 | 0.9726 | 0.9728 |
| **Random Forest** | 0.96 | 0.970 | 0.958 | 0.99 | 0.968 | 0.9580 | 0.9581 |
| **OvR Random Forest** | 0.97 | 0.977 | 0.963 | 0.99 | 0.977 | 0.9681 | 0.9683 |
| **Gradient Boosting** | 0.86 | 0.916 | **0.865** | 0.93 | 0.929 | 0.9013 | 0.9014 |
| **XGBoost** | 0.85 | 0.907 | **0.847** | 0.89 | 0.902 | 0.8849 | 0.8845 |
| **CatBoost** | 0.84 | 0.903 | **0.842** | n/a | 0.897 | 0.8794 | 0.8821 |
| **LightGBM** | 0.85 | 0.900 | **0.838** | 0.89 | 0.902 | 0.8471 | 0.8790 |

*Metric Alignment Note:* A crucial insight from our replication concerns the averaging convention used in published literature. While Allaga et al. [1] report a single general 'F1-score' column, tree ensembles exhibit virtually identical weighted and macro F1-scores (~0.97–0.99). For gradient boosting architectures, however, the published scores (Gradient Boosting: 0.86, XGBoost: 0.85, CatBoost: 0.84, LightGBM: 0.85) align within 0.005–0.012 of our replicated macro-averaged F1 (0.865, 0.847, 0.842, and 0.838, respectively). This confirms that the baseline results replicate with high fidelity across both averaging definitions.



5.5 Binary Classification Performance
In the binary classification task, where malicious attack categories are mapped against normal traffic, the base study's positive class is confirmed to be the legitimate minority class (7.89% prevalence). Table 10 demonstrates that tree ensembles achieve high precision and recall (0.93) on the imbalanced data. Boosting algorithms default to predicting the attack majority, yielding near-zero recall (0.04 for XGBoost, 0.01 for CatBoost) unless class-balanced undersampling is applied.

Table 10. Binary classification performance evaluating detection of the legitimate minority class.
| Model Classifier | Published F1 (Imbalanced) | Replicated F1 (Imbalanced) | Replicated Precision | Replicated Recall | Replicated F1 (SMOTE) | Replicated F1 (Undersampled) |
|---|---|---|---|---|---|---|
| **Bagging Classifier** | 0.93 | 0.929 | 0.931 | 0.928 | 0.878 | **0.967** |
| **CART Decision Tree** | 0.93 | 0.931 | 0.934 | 0.928 | 0.866 | **0.963** |
| **Random Forest** | 0.88 | 0.886 | 0.912 | 0.842 | 0.862 | 0.945 |
| **Extra Trees** | 0.87 | 0.883 | 0.904 | 0.841 | 0.854 | 0.939 |
| **XGBoost (Default)** | 0.07 | 0.364 | 0.841 | 0.042 | 0.468 | 0.865 |
| **CatBoost** | 0.01 | 0.372 | 0.782 | 0.012 | 0.465 | 0.858 |
| **LightGBM** | 0.44 | 0.364 | 0.291 | 0.932 | 0.465 | 0.864 |



5.6 Deep Learning Performance Comparison
Table 11 compares the four deep learning architectures against tree baselines under both feature regimes.

Table 11. Deep learning architectures versus classical tree benchmarks (Original imbalanced data, 40 epochs).
| Architecture Type | Evaluated Features | Accuracy | Weighted F1 | MCC | ROC-AUC (Macro) | Epochs Run | Training Latency (s) | Inference Latency (s) |
|---|---|---|---|---|---|---|---|---|
| **ANN (Dense MLP)** | All 11 features | 0.704 | 0.671 | 0.563 | 0.898 | 40 | 49.6 s | 0.198 s |
| **1D-CNN** | All 11 features | 0.762 | 0.740 | 0.653 | 0.939 | 40 | 136.2 s | 0.352 s |
| **SimpleRNN** | All 11 features | 0.877 | 0.862 | 0.825 | 0.968 | 40 | 101.2 s | 0.674 s |
| **LSTM** | All 11 features | 0.777 | 0.758 | 0.677 | 0.932 | 40 | 261.9 s | 0.880 s |
| **ANN (Dense MLP)** | Sanitized (No Time) | 0.664 | 0.615 | 0.504 | 0.863 | 40 | 50.3 s | 0.354 s |
| **1D-CNN** | Sanitized (No Time) | 0.665 | 0.614 | 0.507 | 0.858 | 40 | 109.5 s | 0.368 s |
| **SimpleRNN** | Sanitized (No Time) | 0.629 | 0.581 | 0.443 | 0.840 | 19 (Stop) | 49.4 s | 0.357 s |
| **LSTM** | Sanitized (No Time) | 0.611 | 0.564 | 0.409 | 0.804 | 25 (Stop) | 189.9 s | 1.316 s |
| **CART (Reference)** | Sanitized (No Time) | **0.708** | **0.670** | **0.571** | **0.874** | n/a | **1.02 s** | **0.008 s** |

Deep architectures trail classical tree models by 12 to 25 percentage points when all 11 features are present. However, upon removing `tcp_time_delta`, the performance gap narrows sharply to 5–9 points, indicating that the apparent tree advantage in published literature was primarily driven by tree models placing precise threshold cuts along the leaked temporal feature.



5.7 Confusion Matrices, ROC and Precision-Recall Dynamics
Figure 3, Figure 4, and Figure 5 contrast confusion matrices across three key experimental conditions:
1. **Bagging on Original Data (All 11 Features, Random Split)**: Figure 3 reveals near-perfect per-class recall across all six classes: `bruteforce` (99.4%), `dos` (99.6%), `flood` (98.3%), `legitimate` (92.6%), `malformed` (99.6%), and `slowite` (98.8%).
2. **Random Forest Sanitized (Without `tcp_time_delta`, Random Split)**: Figure 4 reveals severe degradation for ambiguous classes: while `bruteforce` (97.0%), `flood` (97.7%), and `malformed` (91.6%) remain detectable, `dos` drops to 43.4% recall (55.0% misclassified as `malformed`), `slowite` drops to 24.8% recall (54.4% misclassified as `malformed`), and `legitimate` drops to 10.5% recall (51.2% misclassified as `bruteforce`).
3. **Random Forest on Unseen Loop 4 (With `tcp_time_delta`, Protocol P4 LOLO)**: Figure 5 illustrates the complete failure of temporal memorization: `dos` recall drops to 0.5%, `slowite` drops to 0.2%, and 58.5% of `malformed` packets are incorrectly assigned to `bruteforce`.

```
+-------------------------------------------------------------------------------------------------------+
|                                  Figure 3. CONFUSION MATRIX AUDITS                                  |
|   (a) Bagging Original (All 11)     (b) RF Sanitized (No Time)        (c) RF LOLO Loop 4 (With Time)  |
|   BF: 99.4%   Legit: 92.6%          BF: 97.0%   Legit: 10.5%          BF: 98.0%   Legit: 99.7%        |
|   DoS: 99.6%  Mal:   99.6%          DoS: 43.4%  Mal:   91.6%          DoS:  0.5%  Mal:   34.2%        |
|   Flood: 98.3% Slow: 98.8%          Flood: 97.7% Slow: 24.8%          Flood: 93.0% Slow: 0.2%         |
|   [Near-perfect memorization]       [DoS & SlowITe merge to Malform]  [Complete collapse on DoS/Slow] |
+-------------------------------------------------------------------------------------------------------+
```
*(Reference: `results/figures/Bagging_Original_Normalized_Confusion_Matrix.png`, `CM_Random_Forest_Original.png`, `results/figures/ablation_timestamp_leakage.png`)*

Figure 6 presents Receiver Operating Characteristic (ROC) and Precision-Recall (PR) curves for Random Forest without `tcp_time_delta`. While one-vs-rest ROC-AUC remains high for `flood` (0.999) and `bruteforce` (0.977), it drops for `dos` (0.823) and `legitimate` (0.798). Precision-Recall curves capture the true cost of class imbalance, with Average Precision (AP) dropping to 0.313 for `legitimate` and 0.442 for `slowite`.



5.8 5-Fold Cross-Validation versus Hold-Out Consistency
Table 12 compares 5-fold cross-validation on the training split against the hold-out test set under both feature regimes.

Table 12. 5-Fold stratified cross-validation versus hold-out test set evaluation (Original imbalanced data).
| Model Classifier | Evaluated Feature Set | 5-Fold CV Accuracy (%) | Hold-Out Accuracy (%) | 5-Fold CV ROC-AUC | Hold-Out ROC-AUC |
|---|---|---|---|---|---|
| **CART Decision Tree** | With `tcp_time_delta` | $98.57\% \pm 0.09\%$ | 98.77% | 0.9869 | 0.9885 |
| **Random Forest** | With `tcp_time_delta` | $96.66\% \pm 0.09\%$ | 97.04% | 0.9964 | 0.9972 |
| **XGBoost (Hist)** | With `tcp_time_delta` | $91.65\% \pm 0.15\%$ | 91.80% | 0.9856 | 0.9861 |
| **CART Decision Tree** | Without `tcp_time_delta` | $70.61\% \pm 0.14\%$ | 70.85% | 0.8705 | 0.8741 |
| **Random Forest** | Without `tcp_time_delta` | $70.63\% \pm 0.12\%$ | 71.03% | 0.8810 | 0.8832 |
| **XGBoost (Hist)** | Without `tcp_time_delta` | $\mathbf{71.84\% \pm 0.10\%}$ | **71.89%** | **0.8918** | **0.8926** |

The close agreement between 5-fold CV and hold-out evaluation ($\le 0.4$ percentage points) confirms that results are not artifacts of a single split. Crucially, standard cross-validation completely fails to expose temporal leakage because identical time windows are sampled across every fold.



5.9 Systematic Ablation Studies

5.9.1 Timestamp Duplication Ablation (P1 Random Split vs. P4 LOLO)
Table 13 and Figure 7 present the central ablation: evaluating models on Protocol P1 (Random Split) versus Protocol P4 (Leave-One-Loop-Out across all four capture sessions).

Table 13. Accuracy comparison demonstrating generalization collapse on unseen loops (P1 vs. P4 LOLO).
| Model Classifier | P1 Random (With Time) | P4 LOLO (With Time) | Leakage Gap $\Delta_{\text{leak}}$ | P1 Random (No Time) | P4 LOLO (No Time) | Sanitized Gap |
|---|---|---|---|---|---|---|
| **CART Decision Tree** | 98.8% | 43.9% | **+54.9 pp** | 70.8% | 70.9% | -0.1 pp |
| **Bagging Classifier** | 98.9% | 44.7% | **+54.2 pp** | 71.0% | 71.2% | -0.2 pp |
| **Extra Trees** | 98.1% | 51.1% | **+47.0 pp** | 70.8% | 71.2% | -0.4 pp |
| **Random Forest** | 97.0% | 52.0% | **+45.0 pp** | 71.0% | 71.3% | -0.3 pp |
| **XGBoost (Hist)** | 91.8% | 40.9% | **+50.9 pp** | 71.9% | 72.5% | -0.6 pp |

```
+-------------------------------------------------------------------------------------------------------+
|                         Figure 7. LEAKAGE ABLATION: P1 RANDOM SPLIT VS. P4 LOLO                     |
|                                                                                                       |
|  100% |  [99%] [99%] [98%] [97%] [92%]                                                                |
|   80% |                                               [71%] [71%] [71%] [71%] [72%]                   |
|   60% |                     [51%] [52%]                                                               |
|   40% |         [44%] [45%]             [41%]                                                         |
|   20% |                                                                                               |
|    0% +---------------------------------------------------------------------------------------------  |
|          CART    Bagging  ExtraTr   RF     XGB        CART    Bagging  ExtraTr   RF     XGB           |
|          |<------ With tcp_time_delta ------>|        |<---- Without tcp_time_delta ----->|           |
|          ■ P1 Random Split    ■ P4 LOLO Unseen Loop   ■ P1 Random Split    ■ P4 LOLO Unseen Loop      |
+-------------------------------------------------------------------------------------------------------+
```
*(Reference: `results/figures/ablation_timestamp_leakage.png`)*

With `tcp_time_delta` present, testing on unseen capture loops causes accuracy to plunge by 45.0 to 54.9 percentage points. Without `tcp_time_delta`, the performance gap vanishes entirely ($-0.6$ to $-0.1$ pp), establishing that the leaked column actively misleads classifiers encountering new operational traffic.

5.9.2 Feature Group and Single Feature Excision Ablation
Table 14 evaluates functional feature group subsets, and Table 60 presents leave-one-feature-out importance ablation.

Table 14. Multi-class accuracy across functional protocol feature groups (Protocol P1, Sanitized 80:20 split).
| Functional Feature Subset | Constituent Attributes | CART Accuracy | Random Forest Accuracy |
|---|---|---|---|
| **Transport Layer Only** | `tcp_flags`, `tcp_len` (2 features) | 66.77% | 66.78% |
| **Application Layer Only** | 8 MQTT protocol fields | 62.94% | 62.94% |
| **All Ten Valid Features** | 2 Transport + 8 MQTT fields | **70.85%** | **71.03%** |
| **Leaked Baseline** | All 11 features (with `tcp_time_delta`) | 98.77% | 97.04% |

Table 15. Leave-one-feature-out ablation ranking (Protocol P1, Sanitized 10 features).
| Excluded Feature Attribute | Protocol Layer | Accuracy (CART) | Accuracy (Extra Trees) | Performance Delta (CART) |
|---|---|---|---|---|
| *None (All 10 features)* | Full Valid Set | 70.85% | 70.78% | Baseline (0.00 pp) |
| Exclude `tcp_len` | Transport (TCP) | 64.32% | 64.31% | **-6.53 pp** |
| Exclude `mqtt_msg` | Application (MQTT) | 68.68% | 68.68% | **-2.17 pp** |
| Exclude `mqtt_hdrflags` | Application (MQTT) | 69.91% | 69.83% | **-0.94 pp** |
| Exclude `mqtt_dupflag` | Application (MQTT) | 70.83% | 70.80% | -0.02 pp |
| Exclude `tcp_flags` | Transport (TCP) | 70.83% | 70.81% | -0.01 pp |
| Exclude `mqtt_conack_flags` | Application (MQTT) | 70.83% | 70.83% | -0.01 pp |
| Exclude `mqtt_conflag_cleansess` | Application (MQTT) | 70.83% | 70.81% | -0.01 pp |
| Exclude `mqtt_conflags` | Application (MQTT) | 70.84% | 70.81% | -0.01 pp |
| Exclude `mqtt_kalive` | Application (MQTT) | 70.83% | 70.79% | -0.01 pp |
| Exclude `mqtt_qos` | Application (MQTT) | 70.83% | 70.82% | -0.01 pp |

*Methodological Note*: A leave-one-feature-out accuracy delta reflects the marginal predictive contribution of that specific variable within the current feature set, model configuration, and partition scheme, rather than an absolute measure of physical causality. The empirical findings indicate that packet payload lengths (`tcp_len` and `mqtt_msg`) and header control flags dominate classifier decision boundaries on this capture.

5.9.3 Resampling and Class Balancing Ablation
Table 61 and Table 62 evaluate the empirical effect of SMOTE oversampling and cost-sensitive class weighting on sanitized features.

Table 16. Multi-class accuracy under class rebalancing interventions (Protocol P1, Sanitized 10 features).
| Data Balancing Intervention | CART Accuracy | Extra Trees Accuracy | Random Forest Accuracy | XGBoost Accuracy |
|---|---|---|---|---|
| **Original Imbalanced Data** | **70.85%** | **70.78%** | **71.03%** | **71.89%** |
| **SMOTE Synthetic Oversampling**| 57.32% | 57.36% | 57.70% | 58.69% |
| **Class Weights (`balanced`)** | 56.73% | 56.71% | 57.11% | 58.28% |

Table 17. Macro-averaged F1-scores and Balanced Accuracy under class rebalancing interventions.
| Model Classifier | Condition | Accuracy (%) | Weighted F1 | Macro F1 | Balanced Accuracy (%) |
|---|---|---|---|---|---|
| **CART** | Original | 70.85% | 0.6704 | 0.6184 | 61.23% |
| **CART** | SMOTE | 57.32% | 0.5892 | 0.5801 | 63.27% |
| **CART** | Class Weights | 56.73% | 0.5841 | 0.5788 | 63.44% |
| **Extra Trees** | Original | 70.78% | 0.6682 | 0.6125 | 60.80% |
| **Extra Trees** | SMOTE | 57.36% | 0.5892 | 0.5784 | 63.15% |
| **Extra Trees** | Class Weights | 56.71% | 0.5835 | 0.5748 | 63.05% |
| **Random Forest** | Original | 71.03% | 0.6693 | 0.6129 | 60.81% |
| **Random Forest** | SMOTE | 57.70% | 0.5927 | 0.5807 | 63.31% |
| **Random Forest** | Class Weights | 57.11% | 0.5869 | 0.5770 | 63.20% |
| **XGBoost** | Original | 71.89% | 0.6827 | 0.6286 | 61.80% |
| **XGBoost** | SMOTE | 58.69% | 0.6056 | 0.5960 | 63.88% |
| **XGBoost** | Class Weights | 58.28% | 0.6021 | 0.5939 | 63.85% |

*Interpretation of Trade-offs*: SMOTE and cost-sensitive class weights adjust decision thresholds toward minority classes, raising Balanced Accuracy from ~61% up to 63.3%–63.9% at the expense of a 13.1 to 14.1 percentage point drop in overall accuracy. Because 85.12% of the dataset consists of duplicate feature-label rows, interpolating synthetic instances between identical minority vectors shifts decision boundaries into dense regions, resulting in lower overall precision on the natural test distribution.

5.9.4 Duplicate Excision and Pattern-Grouped Evaluation
Table 63 presents the empirical comparison across Protocol P1 (Random Split, duplicates preserved), Protocol P2 (Deduplicated feature-label rows, 33,107 records), and Protocol P3 (Pattern-Grouped 5-Fold Cross-Validation, strictly segregating the 28,200 unique feature patterns across folds).

Table 18. Multi-class performance under duplicate-aware protocols (Sanitized 10 features, No Time).
| Evaluated Protocol Scheme | CART | Extra Trees | Bagging | Random Forest | XGBoost |
|---|---|---|---|---|---|
| **P1: Random Split (Full Data)** | 70.85% | 70.78% | 71.04% | 71.03% | **71.89%** |
| **P2: Deduplicated Rows Split (33,107 rows)** | 62.55% | 63.08% | 64.98% | 63.21% | **72.43%** |
| **P3: Pattern-Grouped 5-Fold CV (Mean)** | 54.60% | 54.59% | 55.48% | 57.28% | **66.13%** |
| *P3 Standard Deviation across 5 folds* | $\pm 21.67\%$ | $\pm 21.74\%$ | $\pm 22.38\%$ | $\pm 23.48\%$ | $\mathbf{\pm 5.10\%}$ |

*Per-Fold Dynamics in P3*: In Protocol P3, grouping exclusively by feature pattern creates natural variations in fold class balance because certain attack categories (such as `bruteforce`, which contains only 172 unique feature patterns) concentrate heavily in specific folds. Consequently, non-boosting tree models exhibit high fold variance ($\pm 21.7\%$), dropping to ~12.0% on Fold 2 where minority classes dominate and rising to 72.5%–77.4% on Fold 3 and Fold 5. In contrast, XGBoost demonstrates far greater regularized stability across folds ($66.13\% \pm 5.10\%$, ranging between 61.86% and 76.06%), confirming that gradient boosting generalizes significantly better to unseen feature patterns than unconstrained tree memorization.



5.10 Multi-Seed Statistical Significance Testing
To prevent sample-split bias, all models were evaluated across five random split seeds ($S \in \{42, 43, 44, 45, 46\}$). Table 64 summarizes empirical metric distributions, and Table 65 provides paired statistical hypothesis testing and exact McNemar contingency tests.

Table 19. Multi-seed statistical evaluation (Mean $\pm$ Standard Deviation across 5 seeds).
| Feature Regime | Evaluated Model | Accuracy (%) | Weighted F1 (%) | Macro F1 (%) | MCC | Balanced Acc (%) |
|---|---|---|---|---|---|---|
| With `tcp_time_delta` | **Bagging Classifier** | $98.80\% \pm 0.05\%$ | $98.80\% \pm 0.05\%$ | $97.98\% \pm 0.09\%$ | 0.9831 | $97.95\% \pm 0.09\%$ |
| With `tcp_time_delta` | **CART Decision Tree** | $98.85\% \pm 0.05\%$ | $98.85\% \pm 0.05\%$ | $98.08\% \pm 0.07\%$ | 0.9837 | $98.07\% \pm 0.10\%$ |
| With `tcp_time_delta` | **Extra Trees** | $98.03\% \pm 0.07\%$ | $98.00\% \pm 0.07\%$ | $96.79\% \pm 0.13\%$ | 0.9721 | $96.44\% \pm 0.15\%$ |
| With `tcp_time_delta` | **Random Forest** | $96.93\% \pm 0.13\%$ | $96.93\% \pm 0.14\%$ | $95.70\% \pm 0.18\%$ | 0.9571 | $95.17\% \pm 0.22\%$ |
| With `tcp_time_delta` | **XGBoost (Hist)** | $91.62\% \pm 0.15\%$ | $90.47\% \pm 0.21\%$ | $84.47\% \pm 0.40\%$ | 0.8821 | $84.34\% \pm 0.30\%$ |
| Sanitized (No Time) | **Bagging Classifier** | $70.89\% \pm 0.11\%$ | $66.89\% \pm 0.14\%$ | $61.54\% \pm 0.17\%$ | 0.5742 | $61.02\% \pm 0.15\%$ |
| Sanitized (No Time) | **CART Decision Tree** | $70.71\% \pm 0.09\%$ | $66.94\% \pm 0.08\%$ | $61.77\% \pm 0.11\%$ | 0.5712 | $61.20\% \pm 0.10\%$ |
| Sanitized (No Time) | **Extra Trees** | $70.62\% \pm 0.12\%$ | $66.69\% \pm 0.12\%$ | $61.13\% \pm 0.12\%$ | 0.5698 | $60.71\% \pm 0.13\%$ |
| Sanitized (No Time) | **Random Forest** | $70.81\% \pm 0.14\%$ | $66.75\% \pm 0.13\%$ | $61.15\% \pm 0.15\%$ | 0.5729 | $60.72\% \pm 0.15\%$ |
| Sanitized (No Time) | **XGBoost (Hist)** | $\mathbf{71.77\% \pm 0.12\%}$ | $\mathbf{68.18\% \pm 0.12\%}$ | $\mathbf{62.81\% \pm 0.13\%}$ | **0.5874** | $\mathbf{61.72\% \pm 0.09\%}$ |

Table 20. Paired two-tailed $t$-tests across 5 seeds and exact McNemar tests on Seed 42.
| Feature Regime | Model Pair (A vs. B) | Mean Difference (pp) | Paired $t$-Statistic | Paired $t$ $p$-Value | McNemar $p$-Value (Seed 42) | Contingency ($n_{01}, n_{10}$) |
|---|---|---|---|---|---|---|
| With `tcp_time_delta` | Bagging vs. CART | -0.047 pp | $t = -1.214$ | $p = 0.292$ | $p = 0.025$ | (140, 181) |
| With `tcp_time_delta` | Bagging vs. Extra Trees | +0.770 pp | $t = +24.399$ | $p = 1.67 \times 10^{-5}$ | $p = 1.83 \times 10^{-46}$ | (147, 503) |
| With `tcp_time_delta` | Bagging vs. Random Forest | +1.874 pp | $t = +40.581$ | $p = 2.20 \times 10^{-6}$ | $p = 2.45 \times 10^{-157}$ | (118, 931) |
| With `tcp_time_delta` | Bagging vs. XGBoost | +7.170 pp | $t = +128.462$| $p = 2.20 \times 10^{-8}$ | $p < 10^{-300}$ | (205, 3350) |
| With `tcp_time_delta` | CART vs. Extra Trees | +0.817 pp | $t = +19.291$ | $p = 4.26 \times 10^{-5}$ | $p = 4.70 \times 10^{-34}$ | (188, 503) |
| With `tcp_time_delta` | CART vs. Random Forest | +1.922 pp | $t = +28.923$ | $p = 8.51 \times 10^{-6}$ | $p = 1.19 \times 10^{-132}$| (161, 933) |
| With `tcp_time_delta` | CART vs. XGBoost | +7.217 pp | $t = +103.057$| $p = 5.32 \times 10^{-8}$ | $p < 10^{-300}$ | (247, 3351) |
| With `tcp_time_delta` | Extra Trees vs. XGBoost | +6.400 pp | $t = +115.723$| $p = 3.34 \times 10^{-8}$ | $p < 10^{-300}$ | (325, 3114) |
| With `tcp_time_delta` | Random Forest vs. XGBoost| +5.295 pp | $t = +99.794$ | $p = 6.05 \times 10^{-8}$ | $p < 10^{-300}$ | (719, 3051) |
| Sanitized (No Time) | Bagging vs. CART | +0.186 pp | $t = +5.102$ | $p = 0.007$ | $p = 0.002$ | (357, 444) |
| Sanitized (No Time) | Bagging vs. Extra Trees | +0.276 pp | $t = +9.119$ | $p = 8.02 \times 10^{-4}$ | $p = 1.08 \times 10^{-4}$ | (384, 500) |
| Sanitized (No Time) | Bagging vs. Random Forest| +0.081 pp | $t = +3.034$ | $p = 0.039$ | $p = 0.943$ (Not Sig) | (388, 391) |
| Sanitized (No Time) | Bagging vs. XGBoost | -0.878 pp | $t = -19.790$| $p = 3.85 \times 10^{-5}$ | $p = 2.15 \times 10^{-19}$ | (1072, 694) |
| Sanitized (No Time) | CART vs. Extra Trees | +0.090 pp | $t = +3.626$ | $p = 0.022$ | $p = 0.197$ (Not Sig) | (221, 250) |
| Sanitized (No Time) | CART vs. Random Forest | -0.105 pp | $t = -3.013$ | $p = 0.039$ | $p = 0.003$ | (446, 362) |
| Sanitized (No Time) | CART vs. XGBoost | -1.064 pp | $t = -32.160$| $p = 5.57 \times 10^{-6}$ | $p = 8.01 \times 10^{-28}$ | (1143, 678) |
| Sanitized (No Time) | Extra Trees vs. XGBoost | -1.154 pp | $t = -42.011$| $p = 1.92 \times 10^{-6}$ | $p = 4.26 \times 10^{-33}$ | (1105, 611) |
| Sanitized (No Time) | Random Forest vs. XGBoost| -0.959 pp | $t = -24.021$| $p = 1.78 \times 10^{-5}$ | $p = 8.04 \times 10^{-21}$ | (1022, 641) |

*Methodological Qualifications*:
1. **Paired $t$-Tests**: The paired $t$-tests utilize $m = 5$ paired observations across random split seeds. Because 80:20 random splits share overlapping observations, the splits are correlated rather than strictly independent replications; thus, $p$-values are interpreted as comparative indicators of ranking consistency across data shuffles.
2. **McNemar Tests**: The exact McNemar test evaluates paired prediction discordance strictly on the single hold-out partition of Seed 42 ($N = 44,514$ instances).
3. **Statistical Inversion**: When temporal leakage is present, unregularized trees lead XGBoost by over 7 percentage points ($p < 10^{-7}$). Upon leak removal, default XGBoost significantly leads all tree models by 0.88 to 1.15 percentage points ($p < 10^{-4}$). As detailed in Section 5.11, regularized hyperparameter tuning resolves this gap, bringing CART and XGBoost to complete parity.



5.11 Validation-Based Hyperparameter Tuning
To verify whether the 1-point lead of default XGBoost over CART was an artifact of unregularized default settings, a grid search was executed on an 85:15 validation split of the seed-42 training data without temporal features. Table 66 lists the optimal hyperparameter configurations, and Table 67 evaluates the tuned models on the hold-out test set.

Table 21. Hyperparameter search bounds and selected optimal configurations.
| Model Classifier | Hyperparameter Search Space | Selected Optimal Configuration |
|---|---|---|
| **CART Decision Tree** | Criterion: {Gini, Entropy}; Max Depth: {None, 10, 20, 30}; Min Samples Leaf: {1, 5, 10} | Entropy, Max Depth: 10, Min Leaf: 10 |
| **Extra Trees** | Trees: {100, 300}; Min Leaf: {1, 3}; Max Features: {`sqrt`, all} | 100 Trees, Min Leaf: 1, Max Features: all |
| **Random Forest** | Trees: {100, 300}; Min Leaf: {1, 3, 5}; Max Features: {`sqrt`, all} | 100 Trees, Min Leaf: 5, Max Features: `sqrt` |
| **XGBoost (Hist)** | Rounds: {100, 300}; Max Depth: {4, 6, 10}; Learning Rate: {0.1, 0.3} | 100 Rounds, Max Depth: 6, LR: 0.1 |

Table 22. Hold-out test set performance of default versus tuned models (Seed 42, Sanitized).
| Model Classifier | Default Acc (%) | Tuned Acc (%) | Accuracy Delta | Default F1 (w) | Tuned F1 (w) | Default Macro F1 | Tuned Macro F1 |
|---|---|---|---|---|---|---|---|
| **CART Decision Tree** | 70.85% | **71.92%** | **+1.07 pp** | 0.6704 | **0.6822** | 0.6184 | 0.6268 |
| **Random Forest** | 71.03% | 71.57% | +0.54 pp | 0.6693 | 0.6742 | 0.6129 | 0.6202 |
| **Extra Trees** | 70.78% | 70.90% | +0.12 pp | 0.6682 | 0.6702 | 0.6125 | 0.6166 |
| **XGBoost (Hist)** | 71.89% | 71.90% | +0.01 pp | 0.6827 | 0.6828 | 0.6286 | 0.6288 |

Constraining CART with a maximum depth of 10 and minimum leaf size of 10 prevents it from memorizing duplicate rows, boosting its accuracy by +1.07 percentage points to 71.92%. This narrows the gap to just 0.02 percentage points versus tuned XGBoost (71.90%) under Seed 42, indicating near-complete parity pending multi-seed tuning validation. In a leak-free environment with proper regularization, tree and boosting architectures achieve virtually identical performance on these protocol features, nearing the theoretical empirical majority-label ceiling of 73.82%.



5.12 Comprehensive Benchmark Against the State-of-the-Art
Table 68 compares our audited results against published benchmarks on MQTTEEB-D [1], MQTTset [3], and MQTT-IoT-IDS2020 [4].

Table 23. Comprehensive performance benchmark against published state-of-the-art MQTT intrusion detection baselines.
| Investigation | Benchmark Dataset | Evaluated Model | Evaluation Protocol | Accuracy (%) | Weighted F1 (%) | Training Time (s) | Inference Time (s) |
|---|---|---|---|---|---|---|---|
| **Allaga et al. [1]** | MQTTEEB-D | Decision Tree | Random Split (With Time) | 99.00% | 99.00% | 3.44 s | 0.011 s |
| **Allaga et al. [1]** | MQTTEEB-D | Random Forest | Random Split (With Time) | 97.00% | 97.00% | 7.69 s | 0.220 s |
| **Allaga et al. [1]** | MQTTEEB-D | K-NN ($k=5$) | Random Split (With Time) | 97.00% | 97.00% | 0.36 s | 2.360 s |
| **This Study (Replication)**| MQTTEEB-D | CART Tree | P1 Random (5-Seed Mean) | 98.85% | 98.85% | 1.02 s | 0.008 s |
| **This Study (Replication)**| MQTTEEB-D | Random Forest | P1 Random (5-Seed Mean) | 96.93% | 96.93% | 37.24 s | 1.075 s |
| **This Study (Replication)**| MQTTEEB-D | K-NN ($k=5$) | P1 Random (Seed 42) | 96.98% | 96.90% | 0.39 s | 62.019 s |
| **This Study (Audit P4)**| MQTTEEB-D | CART Tree | P4 LOLO (Unseen Loop) | **43.90%** | n/a | n/a | n/a |
| **This Study (Audit P4)**| MQTTEEB-D | Random Forest | P4 LOLO (Unseen Loop) | **52.00%** | n/a | n/a | n/a |
| **This Study (Audit P4)**| MQTTEEB-D | XGBoost | P4 LOLO (Unseen Loop) | **40.90%** | n/a | n/a | n/a |
| **This Study (Sanitized)**| MQTTEEB-D | Tuned CART | P1 Sanitized (No Time) | **71.92%** | **68.22%** | 1.05 s | 0.008 s |
| **This Study (Sanitized)**| MQTTEEB-D | Tuned XGBoost | P1 Sanitized (No Time) | **71.90%** | **68.28%** | 8.85 s | 0.495 s |
| **This Study (Grouped)**| MQTTEEB-D | XGBoost | P3 Pattern-Grouped 5-Fold| **66.13%** | **60.15%** | 45.83 s | 0.495 s |
| **Vaccari et al. [3]** | MQTTset (Emulated) | Random Forest | Random Partition | 91.60% | 91.40% | 2298.28 s | 125.85 s |
| **Vaccari et al. [3]** | MQTTset (Emulated) | Decision Tree | Random Partition | 91.60% | 91.40% | 148.81 s | 2.30 s |
| **Khan et al. [4]** | MQTT-IoT-IDS2020 | Decision Tree | Random Partition | 90.54% | 89.83% | 79.20 s | 4.30 s |
| **Khan et al. [4]** | MQTT-IoT-IDS2020 | Random Forest | Random Partition | 89.87% | 84.99% | 9.30 s | 3.98 s |



5.13 Discussion and Threats to Validity
1. **Root Cause of Generalization Collapse**: Because cyber-attack campaigns in MQTTEEB-D were executed sequentially in discrete time blocks, the leaked `tcp_time_delta` feature mapped monotonically to the target label. Decision trees exploited fine-grained threshold cuts on this feature, achieving near-perfect in-sample memorization. When tested on unseen capture loops (LOLO), these historical time thresholds became invalid, causing accuracy to collapse to 40.9%–52.0%.
2. **The 71% Accuracy Barrier**: Achieving ~71% accuracy on the sanitized dataset does not reflect an algorithmic limitation. Rather, it approaches the theoretical empirical majority-label accuracy bound ($A^* = 73.82\%$) imposed by the 11.29% label ambiguity present in the ten packet-level features. Resolving this ambiguity requires flow-level contextual features rather than single-packet inspection.
3. **The Imbalance Resilience Fallacy**: The hypothesis that unregularized decision trees possess an inherent resistance to class imbalance [1] was an artifact of temporal leakage. When evaluated under leak-free protocols, tree ensembles and gradient boosting methods perform similarly, with regularized tuning establishing parity between CART (71.92%) and XGBoost (71.90%).
4. **Hardware Latency Considerations and Threats to Validity**:
   * *Inference Latency Metrics*: Measurement units must be interpreted with technical precision. Under hold-out evaluation on $N_{\text{test}} = 44,514$ packet vectors, a single CART decision tree achieved a total test latency of $0.008\text{ s}$ ($8.0\text{ ms}$), corresponding to an average single-packet inference time of approximately $0.18\ \mu\text{s}$. While this computational footprint is extremely lightweight, the practical security utility of standalone stateless packet filtering is severely constrained by the $73.82\%$ empirical accuracy ceiling imposed by $11.29\%$ packet ambiguity. Consequently, operational deployments should not rely exclusively on isolated packet inspection, but rather integrate lightweight tree filtering with upstream stateful flow aggregators.
   * *Dataset Diversity*: Our empirical findings are derived from the physical MQTTEEB-D benchmark; while forensic auditing principles apply universally across NIDS evaluation, specific quantitative leakage parameters reflect this specific capture setup.
   * *LOLO Granularity & Class Shift*: The four temporal capture loops differ both in volume (ranging from 21,501 to 137,319 records) and class distribution. Notably, Loop 4 contains only 376 legitimate packets (compared to 11,158 in Loop 1) and 526 flood packets. When models trained on Loops 1–3 encounter Loop 4, cross-loop class-prior shifts exacerbate generalization degradation alongside temporal leakage.
   * *Stateless vs. Flow Representation*: The benchmark provides isolated, stateless packet vectors rather than reconstructed bidirectional transport flows, preventing classifiers from tracking TCP connection handshakes or multi-packet application payload sequences.



6 Conclusion and Future Work

This paper presented an independent replication, forensic data audit, and leakage-aware evaluation of the MQTTEEB-D benchmark for MQTT network intrusion detection. While our replication verified published multi-class metrics (weighted F1 of 0.97 to 0.99) under the original experimental setup, our systematic data audit revealed that the transport feature `tcp_time_delta` is a bitwise duplicate of the capture timestamp ($\rho = 1.000$) across 100% of observations in the released dataset. Furthermore, out of 222,567 observations, only 33,107 unique feature-plus-label rows exist (85.12% row duplication) and 28,200 unique feature patterns when labels are ignored; 11.29% of feature patterns carry contradictory class labels, establishing an empirical majority-class upper bound of 73.82% for the observed distribution across the remaining ten protocol features.

When evaluated on unseen capture loops (Leave-One-Loop-Out), accuracy collapsed by 45.0 to 54.9 percentage points (dropping to 40.9%–52.0%) when the leaked feature was present. Removing the leaked feature eliminated this performance gap, with accuracy stabilizing at ~71% across both random and unseen-loop splits; under a deduplicated feature-label-row split (P2), accuracy ranged from 62.5% to 72.4%, and under strict pattern-grouped 5-fold cross-validation (P3), accuracy averaged 54.6% to 66.1% (with XGBoost achieving 66.13% ± 5.10%). Moreover, the apparent superiority of unregularized decision trees and bagging vanished in the absence of leakage; hyperparameter optimization brought regularized CART (71.92%) and XGBoost (71.90%) to near-complete parity under Seed 42 (a 0.02 percentage-point gap).

These results indicate that reported benchmark breakthroughs in network intrusion detection must be verified against temporal leakage and dataset redundancy. To support reproducible research, we open-source the LA-MQTT framework, establishing automated audit and validation protocols for next-generation IoT security benchmarking. Future work should:
* extend the LA-MQTT pipeline to bidirectional flow features and windowed session aggregators to resolve stateless packet ambiguity;
* incorporate temporal graph neural networks (GNNs) and attention-based transformers to model inter-packet sequential state transitions;
* evaluate model resilience against adversarial perturbation, packet timing jitter, and polymorphic evasion attacks;
* deploy and benchmark regularized tree and boosting kernels on physical edge gateway hardware (e.g., Raspberry Pi 4, ESP32) to measure device-level CPU energy and memory utilization; and
* expand cross-testbed generalization evaluation to emerging IoT benchmarks including CICIoMT2024 and SENMQTT-SET.



Declarations
Author contributions: [Describe each author’s contribution, for example conceptualisation, software development, data forensic auditing, experimental evaluation, formal analysis, investigation, visualization, and manuscript drafting]
Funding: [State the funding source or write "This research received no external funding"]
Conflict of interest: The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.
Data availability: The MQTTEEB-D benchmark dataset is openly accessible from Mendeley Data under Creative Commons Attribution 4.0 International (CC BY 4.0) licensing terms (Aqachtoul et al., 2025; DOI: 10.1016/j.dib.2025.111897).
Code availability: The complete LA-MQTT software repository—including forensic audit scripts, multi-protocol partitioning modules, pre-trained model checkpoints, prediction artifacts, and reproduction pipelines—is archived at https://github.com/MuMu161/LA-MQTT-Benchmark and available on request.
Ethics statement: This study uses an open network-traffic dataset and involves no human participants, animal experiments, or private patient data.
Use of generative AI: [Describe any use of generative AI tools for language polishing or drafting, as required by the target journal and institution]
Acknowledgements: [Add acknowledgements, for example laboratory testbed infrastructure or computing cluster facilities used]

References
[1] H. Allaga, M. Biniz, and A. Farchane, "MQTTEEB-D: A high-fidelity benchmark for real-time MQTT anomaly detection using machine learning techniques," *Ad Hoc Networks*, vol. 181, art. 104062, 2026, doi: 10.1016/j.adhoc.2025.104062.  
[2] A. Aqachtoul, K. Karam, A. Elamrani, M. Najib, N. Rafalia, and M. Bakhouya, "MQTTEEB-D: A real-world IoT cybersecurity dataset for AI-powered threat detection in MQTT networks," *Data in Brief*, vol. 60, art. 111897, 2025, doi: 10.1016/j.dib.2025.111897.  
[3] I. Vaccari, G. Chiola, M. Aiello, M. Mongelli, and E. Cambiaso, "MQTTset, a new dataset for machine learning techniques on MQTT," *Sensors*, vol. 20, no. 22, art. 6578, 2020, doi: 10.3390/s20226578.  
[4] M. A. Khan et al., "A deep learning-based intrusion detection system for MQTT enabled IoT," *Sensors*, vol. 21, no. 21, art. 7016, 2021, doi: 10.3390/s21217016.  
[5] H. Hindy et al., "Machine learning based IoT intrusion detection system: An MQTT case study (MQTT-IoT-IDS2020 dataset)," in *Proc. Int. Networking Conf.*, 2020, pp. 73–84.  
[6] I. Ullah, A. Ullah, and M. Sajjad, "Towards a hybrid deep learning model for anomalous activities detection in Internet of Things networks," *IoT*, vol. 2, no. 3, pp. 428–448, 2021, doi: 10.3390/iot2030022.  
[7] H. Siddharthan, T. Deepa, and P. Chandhar, "SENMQTT-SET: An intelligent intrusion detection in IoT-MQTT networks using ensemble multi cascade features," *IEEE Access*, vol. 10, pp. 33095–33110, 2022, doi: 10.1109/ACCESS.2022.3161556.  
[8] M. A. B. Ahmadon, N. Yamaguchi, and S. Yamaguchi, "Process-based intrusion detection method for IoT system with MQTT protocol," in *Proc. IEEE 8th Global Conf. Consumer Electronics (GCCE)*, 2019, pp. 953–956.  
[9] A. Haripriya and K. Kulothungan, "Secure-MQTT: An efficient fuzzy logic-based approach to detect DoS attack in MQTT protocol for Internet of Things," *EURASIP J. Wireless Commun. Netw.*, vol. 2019, art. 90, 2019.  
[10] H. Alaiz-Moreton et al., "Multiclass classification procedure for detecting attacks on MQTT-IoT protocol," *Complexity*, vol. 2019, art. 6516253, 2019, doi: 10.1155/2019/6516253.  
[11] H. J. K. Al Masoodi, "Evaluating the effectiveness of machine learning-based intrusion detection in multi-cloud environments," *Babylon. J. Internet Things*, pp. 94–105, 2024.  
[12] D. Arp, E. Quiring, F. Pendlebury, A. Warnecke, F. Pierazzi, C. Wressnegger, and K. Rieck, "Dos and don'ts of machine learning in computer security," in *Proc. 31st USENIX Security Symp.*, 2022, pp. 3971–3988.  
[13] S. Kapoor and A. Narayanan, "Leakage and the reproducibility crisis in machine-learning-based science," *Patterns*, vol. 4, no. 9, art. 100804, 2023, doi: 10.1016/j.patter.2023.100804.  
[14] G. Engelen, V. Rimmer, and W. Joosen, "Troubleshooting an intrusion detection dataset: the CICIDS2017 case study," in *Proc. IEEE Security and Privacy Workshops (SPW)*, 2021, pp. 7–12.  
[15] N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, "SMOTE: Synthetic minority over-sampling technique," *J. Artif. Intell. Res.*, vol. 16, pp. 321–357, 2002.  
[16] L. Breiman, J. H. Friedman, R. A. Olshen, and C. J. Stone, *Classification and Regression Trees*. Belmont, CA: Wadsworth, 1984.  
[17] L. Breiman, "Bagging predictors," *Mach. Learn.*, vol. 24, no. 2, pp. 123–140, 1996.  
[18] L. Breiman, "Random forests," *Mach. Learn.*, vol. 45, no. 1, pp. 5–32, 2001.  
[19] P. Geurts, D. Ernst, and L. Wehenkel, "Extremely randomized trees," *Mach. Learn.*, vol. 63, no. 1, pp. 3–42, 2006.  
[20] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in *Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining*, 2016, pp. 785–794.  
[21] J. Gorodkin, "Comparing two K-category assignments by a K-category correlation coefficient," *Comput. Biol. Chem.*, vol. 28, no. 5–6, pp. 367–374, 2004.  
[22] Q. McNemar, "Note on the sampling error of the difference between correlated proportions or percentages," *Psychometrika*, vol. 12, no. 2, pp. 153–157, 1947.  
[23] F. Pedregosa et al., "Scikit-learn: Machine learning in Python," *J. Mach. Learn. Res.*, vol. 12, pp. 2825–2830, 2011.  
[24] G. Lemaître, F. Nogueira, and C. K. Aridas, "Imbalanced-learn: A Python toolbox to tackle the curse of imbalanced datasets in machine learning," *J. Mach. Learn. Res.*, vol. 18, no. 17, pp. 1–5, 2017.  
[25] M. Abadi et al., "TensorFlow: Large-scale machine learning on heterogeneous distributed systems," *arXiv:1603.04467*, 2016.  
[26] E. Al-Masri, K. R. Kalyanam, J. Batts, J. Kim, S. Singh, T. Vo, and C. Yan, "Investigating messaging protocols for the Internet of Things (IoT)," *IEEE Access*, vol. 8, pp. 94880–94911, 2020.  
[27] N. Chaabouni, M. Mosbah, A. Zemmari, C. Sauvignac, and P. Faruki, "Network intrusion detection for IoT security based on learning techniques," *IEEE Commun. Surveys Tuts.*, vol. 21, no. 3, pp. 2671–2701, 2019.  
[28] M. Swain, K. Sethi, and N. Tripathi, "Attention-based intrusion detection in MQTT-IoT network: a federated learning and deep reinforcement learning approach," *Cluster Comput.*, vol. 29, art. 495, 2026, doi: 10.1007/s10586-026-06282-8.  
[29] N. M. Alassaf, S. Manickam, A. Odeh, and M. Anbar, "Detecting anomalies in MQTT/MQTT-SN traffic using intelligent learning models," *Bull. Electr. Eng. Inform.*, vol. 15, no. 3, 2026, doi: 10.11591/eei.v15i3.11889.  
[30] A. Al Hanif and M. Ilyas, "Effective feature engineering framework for securing MQTT protocol in IoT environments," *Sensors*, vol. 24, no. 6, art. 1782, 2024, doi: 10.3390/s24061782.  
[31] N. S. Alotaibi, H. I. Sayed Ahmed, S. O. M. Kamel, and G. F. ElKabbany, "Secure enhancement for MQTT protocol using distributed machine learning framework," *Sensors*, vol. 24, no. 5, art. 1638, 2024.  
[32] S. Ullah, J. Ahmad, M. A. Khan, M. S. Alshehri, W. Boulila, A. Koubaa, S. U. Jan, and M. M. Iqbal Ch, "TNN-IDS: Transformer neural network-based intrusion detection system for MQTT-enabled IoT networks," *Comput. Netw.*, vol. 237, art. 110072, 2023.  
[33] S. Memon, U. K. Wiil, and M. Shaikh, "Explainable intrusion detection for Internet of Medical Things," in *Proc. 15th Int. Joint Conf. Knowledge Discovery, Knowledge Engineering and Knowledge Management (KMIS)*, SciTePress, 2023, pp. 40–51.
[34] T. G. Dietterich, "Approximate statistical tests for comparing supervised classification learning algorithms," *Neural Comput.*, vol. 10, no. 7, pp. 1895–1923, 1998, doi: 10.1162/089976698300017197.
[35] C. Nadeau and Y. Bengio, "Inference for the generalization error," *Mach. Learn.*, vol. 52, no. 3, pp. 239–281, 2003, doi: 10.1023/A:1024068612664.


Appendix A – Multi-Seed Performance and Resource Consumption

Precision and recall use the conventions of Section 4.7 (weighted averaging across all classes). Training and test latencies represent monotonic wall-clock execution time on the benchmark workstation. Values report mean across five random seeds (Seeds 42–46) under Protocol P1 on sanitized features without temporal markers.

| Evaluated Algorithm | Protocol Feature Set | Accuracy (%) | Weighted F1 | Macro F1 | MCC | Training Latency (s) | Inference Latency (s) |
|---|---|---|---|---|---|---|---|
| CART Decision Tree | Sanitized (10 features) | 70.71% ± 0.09% | 0.6694 ± 0.0008 | 0.6177 ± 0.0011 | 0.5712 | 1.02 s | 0.008 s |
| Bagging Classifier | Sanitized (10 features) | 70.89% ± 0.11% | 0.6689 ± 0.0014 | 0.6154 ± 0.0017 | 0.5742 | 6.64 s | 0.095 s |
| Extra Trees | Sanitized (10 features) | 70.62% ± 0.12% | 0.6669 ± 0.0012 | 0.6113 ± 0.0012 | 0.5698 | 10.42 s | 1.301 s |
| Random Forest | Sanitized (10 features) | 70.81% ± 0.14% | 0.6675 ± 0.0013 | 0.6115 ± 0.0015 | 0.5729 | 37.24 s | 1.075 s |
| XGBoost (Hist) | Sanitized (10 features) | 71.77% ± 0.12% | 0.6818 ± 0.0012 | 0.6281 ± 0.0013 | 0.5874 | 8.71 s | 0.500 s |
| Tuned CART (Depth 10) | Sanitized (10 features) | 71.92% (Seed 42) | 0.6822 | 0.6268 | 0.5898 | 1.05 s | 0.008 s |
| Tuned XGBoost | Sanitized (10 features) | 71.90% (Seed 42) | 0.6828 | 0.6288 | 0.5895 | 8.85 s | 0.495 s |
| 1D-CNN (Neural) | Sanitized (10 features) | 66.48% | 0.6137 | 0.5067 | 0.5067 | 109.5 s | 0.368 s |
| ANN (MLP) | Sanitized (10 features) | 66.40% | 0.6149 | 0.5040 | 0.5040 | 50.3 s | 0.354 s |
| SimpleRNN | Sanitized (10 features) | 62.90% | 0.5812 | 0.4429 | 0.4429 | 49.4 s | 0.357 s |
| LSTM | Sanitized (10 features) | 61.08% | 0.5639 | 0.4087 | 0.4087 | 189.9 s | 1.316 s |

Table A1. Comprehensive accuracy, F1, MCC, and latency metrics across tree ensembles, boosting architectures, and deep neural networks on the sanitized MQTTEEB-D benchmark.
