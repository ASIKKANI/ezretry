# Future Project Idea: `sft-prep`

`sft-prep` is a utility library designed to optimize, standardize, and debug datasets for Supervised Fine-Tuning (SFT) of Large Language Models.

---

## 🛠️ Core Modules

### 1. `sft_prep.dataset` (Dataset Standardization)
Converts raw open-source dataset formats into standardized ChatML or OpenAI message formats.
* **Supported inputs:** Alpaca, ShareGPT, custom flat JSON.
* **Output:** Standardized message list format compatible with Hugging Face tokenizers.

### 2. `sft_prep.collators` (Sequence Packing)
Concatenates multiple conversational sequences end-to-end into a single tensor block of length `max_seq_len` to eliminate pad tokens (`[PAD]`).
* **Benefit:** Speeds up GPU training by 2x to 5x.
* **Features:** Built-in loss-masking helper to set prompt labels to `-100`.

### 3. `sft_prep.debug` (Token-Level Loss Visualizer)
A debugging utility to compute cross-entropy loss for each individual token and print color-coded text in the CLI.
* **Benefit:** Helps identify mislabeled dataset samples, syntax errors, or outlier sequences that cause training spikes.

---

## 📂 Proposed File Structure

```text
sft-prep/
├── pyproject.toml              # PyPI package configurations
├── README.md                   # Setup and usage guidelines
├── sft_prep/
│   ├── __init__.py
│   ├── dataset.py              # AlpacaToChatML, ShareGPTToChatML, etc.
│   ├── collators.py            # SequencePackingCollator
│   └── debug.py                # TokenLossVisualizer
└── tests/                      # Unit tests
```
