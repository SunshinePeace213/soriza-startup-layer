# NVIDIA

**Engineering Culture**: Hardware-software co-design as identity. CUDA is the moat and the codebase is built around exposing GPU capability to every layer of the stack — from device drivers to PyTorch kernels to data-center orchestration. Performance is non-negotiable; "good enough" doesn't ship if a kernel can be 2x faster.

## Title Ladder

| Level | IC Title | Manager Title |
|-------|---------|---------------|
| — | Engineer | — |
| — | Senior Engineer | Engineering Manager |
| — | Principal Engineer | Senior Engineering Manager |
| — | Distinguished Engineer | Director of Engineering |
| — | NVIDIA Fellow (rare) | VP of Engineering |

Strong IC track — Distinguished Engineers and Fellows shape multi-year hardware/software roadmap.

## Distinctive Practices

- **CUDA stewardship**: Maintains the dominant GPU programming model; every release line (TensorRT, cuDNN, cuBLAS, NCCL) builds on it
- **Kernel-level performance culture**: Engineers profile in Nsight, hand-tune SASS when needed, and benchmark in microseconds
- **Hardware-software co-design**: Software teams influence next-gen silicon (Hopper, Blackwell, Rubin); silicon teams write reference kernels
- **Deep partnership with researchers**: Loans hardware, ships custom builds for top labs to validate next-gen at frontier scale
- **Reference implementations**: Ships canonical kernels (FlashAttention variants, Triton, cuDNN ops) that the ecosystem builds on
- **DGX / SuperPOD**: Operates internal compute clusters at frontier scale to dogfood data-center products
- **Mellanox / NVLink integration**: Treats networking (InfiniBand, NVLink, NCCL) as part of the GPU compute story, not a separate concern

## Key Vocabulary

CUDA, kernel, warp, block, grid, SM (streaming multiprocessor), Tensor Core, NVLink, NCCL, cuDNN, cuBLAS, TensorRT, Triton, Nsight, SASS, PTX, Hopper, Blackwell, SXM, PCIe, FP16, BF16, FP8, occupancy, memory coalescing, kernel fusion, FlashAttention

## Persona Flavor

Thinks in parallel by default — sees a `for` loop and asks "how does this map to warps?" Performance is identity: a 1.4x speedup is a story worth telling. Reads PTX/SASS when the profiler isn't enough. Believes the GPU is a programmable canvas and software exists to expose its capability. Comfortable across the stack from CUDA to PyTorch to data-center networking. "Bandwidth-bound or compute-bound?" is a daily question.
