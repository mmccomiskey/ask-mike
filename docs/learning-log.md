# Learning log

Running notes. One entry per ticket that taught me something. The rule from the
backlog applies: if I cannot explain it here in my own words, the ticket is not
done.

---

## AML-103 - Python environment

**Date:** 2026-07-28

Environment: Python 3.12.13, torch 2.13.0, arm64 (Apple Silicon), MPS
available. Verify anytime with `.venv/bin/python scratch/check_env.py`.

### Measured on this machine

2048x2048 matmul, mean of 20 runs:

| | time | note |
|---|---|---|
| cpu | 11.14 ms | |
| mps | 4.10 ms | 2.7x faster than cpu |
| host to mps and back | 1.22 ms | 0.3x the cost of the matmul itself |

### What the numbers mean

**The 2.7x is smaller than I expected.** Apple's unified memory means the GPU is
not a discrete card with its own VRAM across a PCIe bus, so the ceiling is lower
than the 10-50x you read about for NVIDIA. A 2048² matmul is also small enough
that launch overhead is a visible fraction of the total. The gap should widen
with bigger tensors, which is worth re-measuring once AML-216 sweeps model
sizes.

**The copy number is the one that matters.** Moving a 2048² float32 tensor
(16 MB) host to device and back costs 1.22 ms, roughly a third of what the
actual multiplication costs. So a training step that carelessly moves data
between devices spends a meaningful share of its time on memcpy rather than
math.

The practical consequence for AML-213: create the batch on the target device, or
move it once and keep it there. Never `.cpu()` inside the training loop just to
inspect something. The `estimate_loss()` function should be the only place that
pulls numbers back to the host, and only every N steps.

This is also, in miniature, why distributed training is hard. If a 16 MB copy
between two chips in the same package is this expensive relative to the compute,
then the same copy across a network between machines dominates completely. That
is the entire reason gradient-accumulation and sharding strategies exist.

### Open

- Re-measure the cpu/mps ratio at larger sizes during AML-216, and record where
  the gap stops widening.
