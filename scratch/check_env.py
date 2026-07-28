"""AML-103 environment check.

Confirms torch is installed, MPS (Apple Silicon GPU) is usable, and shows what
moving tensors between devices actually costs. Run it whenever the environment
feels wrong:

    .venv/bin/python scratch/check_env.py
"""

import platform
import time

import torch


def device_report() -> torch.device:
    print(f"python        {platform.python_version()}")
    print(f"machine       {platform.machine()}")
    print(f"torch         {torch.__version__}")
    print(f"mps built     {torch.backends.mps.is_built()}")
    print(f"mps available {torch.backends.mps.is_available()}")

    if not torch.backends.mps.is_available():
        print("\nMPS unavailable, falling back to CPU. Training will be slow.")
        return torch.device("cpu")

    return torch.device("mps")


def smoke_test(device: torch.device) -> None:
    """Prove a tensor lives on the device and that arithmetic works there."""
    x = torch.arange(6, dtype=torch.float32, device=device).reshape(2, 3)
    print(f"\ntensor on {x.device}:\n{x}")
    print(f"x @ x.T =\n{x @ x.T}")


def benchmark(device: torch.device, n: int = 2048, iters: int = 20) -> None:
    """Compare a big matmul on CPU vs the GPU, and time the transfer itself.

    The transfer number is the point. It is why the training loop in AML-213
    keeps everything resident on one device instead of moving data per step.
    """
    if device.type == "cpu":
        return

    a_cpu = torch.randn(n, n)
    b_cpu = torch.randn(n, n)

    def timed(fn, warmup=3):
        for _ in range(warmup):
            fn()
        if device.type == "mps":
            torch.mps.synchronize()
        start = time.perf_counter()
        for _ in range(iters):
            fn()
        if device.type == "mps":
            torch.mps.synchronize()
        return (time.perf_counter() - start) / iters

    cpu_s = timed(lambda: a_cpu @ b_cpu)

    a_dev, b_dev = a_cpu.to(device), b_cpu.to(device)
    dev_s = timed(lambda: a_dev @ b_dev)

    # Round trip: host -> device -> host, which is the cost you pay if you are
    # careless about where your data lives.
    transfer_s = timed(lambda: a_cpu.to(device).cpu())

    print(f"\n{n}x{n} matmul, mean of {iters} runs")
    print(f"  cpu            {cpu_s * 1e3:8.2f} ms")
    print(f"  {device.type:<14} {dev_s * 1e3:8.2f} ms  ({cpu_s / dev_s:.1f}x faster)")
    print(f"  host<->{device.type} copy {transfer_s * 1e3:8.2f} ms  "
          f"({transfer_s / dev_s:.1f}x the cost of the matmul itself)")


if __name__ == "__main__":
    dev = device_report()
    smoke_test(dev)
    benchmark(dev)
    print("\nAML-103 OK" if torch.backends.mps.is_available() else "\nAML-103 DEGRADED (cpu only)")
