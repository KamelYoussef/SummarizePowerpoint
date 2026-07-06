import torch
import time

def benchmark_gpu_block(func, *args, **kwargs):
    # 1. Clear cache and reset max memory stats
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    
    # 2. Warm up the GPU (Crucial for Whisper/CTranslate2 to load libraries)
    # We execute it once before timing so compilation/loading overhead isn't counted
    try:
        func(*args, **kwargs)
    except Exception as e:
        print(f"Warmup failed, but continuing: {e}")
    
    # 3. Synchronize and Start Timer
    torch.cuda.synchronize()
    start_time = time.perf_counter()
    
    # 4. Run the actual benchmarked workload
    result = func(*args, **kwargs)
    
    # 5. Synchronize and Stop Timer
    torch.cuda.synchronize()
    end_time = time.perf_counter()
    
    # 6. Gather Memory Statistics
    elapsed_time = end_time - start_time
    peak_mem_bytes = torch.cuda.max_memory_allocated()
    curr_mem_bytes = torch.cuda.memory_allocated()
    
    # Convert bytes to Megabytes
    peak_mem_mb = peak_mem_bytes / (1024 ** 2)
    curr_mem_mb = curr_mem_bytes / (1024 ** 2)
    
    print("================ BENCHMARK RESULTS ================")
    print(f"Execution Time:    {elapsed_time:.4f} seconds")
    print(f"Peak GPU Memory:   {peak_mem_mb:.2f} MB")
    print(f"Current GPU Memory: {curr_mem_mb:.2f} MB")
    print("===================================================")
    
    return result
