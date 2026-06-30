# UrbanPulse Engine: Real-Time High-Throughput Spatial Identity Matcher

UrbanPulse Engine is a zero-latency GovTech data infrastructure prototype designed for smart city networks. It processes millions of high-frequency computer vision telemetry logs, runs sub-second comparative matches against critical criminal watchlists, and automates real-time public threat notifications and conversational police routing workflows.

## ⚡ Accelerated Architecture
To satisfy the computational demands of processing real-time identity lookups across hundreds of active city streams simultaneously, the system relies on a two-layer accelerated layout:

1. **NVIDIA Acceleration Layer:** Built directly with the **NVIDIA RAPIDS (`cudf.pandas`)** translation layer. In production, this allows standard dataframe manipulations and many-to-one hash joins to bypass traditional CPU performance limits and execute instantly across parallel **NVIDIA CUDA Cores** (such as Google Cloud L4/T4 GPU nodes) without requiring a complete codebase rewrite.
2. **Google Cloud Data Warehousing Layer:** High-frequency telemetry filters land in **Google Cloud Storage (GCS)**, aggregate inside the processing core, and stream directly into **BigQuery Sandbox** analytical tables.
3. **Conversational Agent Routing:** A **Gemini Enterprise Agent** (Vertex AI Agent Builder) is grounded directly on top of the live BigQuery dataset, converting natural language operator prompts into structured transactional insights for field command dispatches.

## 💻 Technical Stack
* **Language:** Python 3.14
* **Acceleration Core:** NVIDIA RAPIDS (cuDF Pandas Intercept String Layer)
* **Data Warehouse:** Google Cloud BigQuery Sandbox
* **Orchestration Client:** `google-cloud-bigquery`, `pandas-gbq`
* **AI Orchestration Platform:** Vertex AI Agent Builder (Gemini Enterprise Agent Engine)
