# W2D1 - GPU Memory Measurement

## Objective

Measure how model memory behaves on a real GPU at different precisions.

This lab runs on a Google Colab T4 GPU and compares memory usage for different model loading precisions.

## Model

Qwen/Qwen2.5-1.5B-Instruct

- 1.5 billion parameters
- GPU: Colab T4
- VRAM: 16 GB

## Tasks Completed

- GPU runtime setup
- Baseline GPU memory measurement
- Load model using:
  - fp16
  - int8
  - int4
- Measure VRAM consumption
- Compare predicted vs actual memory
- Measure generation speed
- Observe KV cache and context memory growth

## Deliverables

- generate.py
- results.json
- verification output

## Verification

GREEN CHECK: PASS
