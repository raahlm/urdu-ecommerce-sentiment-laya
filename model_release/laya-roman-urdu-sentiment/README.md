# LAYA — Roman Urdu E-commerce Sentiment

This directory contains a fine-tuned LAYA checkpoint developed for research
on Pakistani e-commerce reviews, including Roman Urdu and multilingual text.

## Model files

- `model.safetensors`: fine-tuned model weights (tracked with Git LFS).
- `encoder/config.json`: encoder architecture configuration.
- `tokenizer/`: tokenizer files.
- `rl_agent_config.json`: LAYA agent configuration.

## Training configuration

- Base encoder: `jhu-clsp/mmBERT-base`
- Fine-tuning: 4 epochs
- Distributed training: 2 GPUs
- Micro-batch size: 8 per GPU
- Gradient accumulation: 4
- Effective batch size: 64
- Maximum sequence length: 256
- Random seed: 13

## Data and evaluation

The training pipeline used machine-assisted silver annotations. These labels
are not independently human-verified ground truth. Agreement with these labels
should not be interpreted as equivalent to accuracy against human judgments.

Evaluate the model on independently human-annotated data before relying on
its predictions for consequential decisions.

## Base model and licensing

The base encoder is `jhu-clsp/mmBERT-base`. Check the base model's license and
retain any required notices before redistributing this checkpoint.

## Reproducibility

The configuration files describe the model architecture and training setup.
The original training data and local training artifacts are not included in
this directory.
