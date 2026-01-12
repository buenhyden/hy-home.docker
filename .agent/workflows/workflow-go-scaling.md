---
description: Workflow for analyzing and improving Go backend scalability
---

1. **Baseline Benchmarking**

    Establish current performance metrics.

    // turbo

    ```bash
    # Run existing benchmarks
    go test -bench=. ./...
    ```

    Use `hey` or `wrk` for HTTP load testing:

    ```bash
    hey -n 1000 -c 100 http://localhost:8080/api/heavy-endpoint
    ```

2. **Profiling (Identify Bottlenecks)**

    Use `pprof` to find CPU or Memory spikes.

    ```bash
    # Get CPU profile
    go tool pprof http://localhost:8080/debug/pprof/profile?seconds=30
    ```

    ```bash
    # Get Heap (Memory) profile
    go tool pprof http://localhost:8080/debug/pprof/heap
    ```

3. **Database Optimization**

    Check for N+1 queries and connection pooling.

    **Check**:
    - Is `MaxOpenConns` set?
    - Are indexes used? (Use `EXPLAIN ANALYZE`)

    **Code Pattern (Batch Insert)**:

    ```go
    // Bad: N inserts
    for _, item := range items {
        db.Create(&item)
    }

    // Good: Batch insert
    db.CreateInBatches(items, 100)
    ```

4. **Concurrency Implementation**

    Use Goroutines safely for independent tasks.

    **Pattern: Worker Pool**:

    ```go
    func worker(id int, jobs <-chan int, results chan<- int) {
        for j := range jobs {
            results <- process(j)
        }
    }

    func main() {
        jobs := make(chan int, 100)
        results := make(chan int, 100)

        // Start 3 workers
        for w := 1; w <= 3; w++ {
            go worker(w, jobs, results)
        }
    }
    ```

5. **Caching Strategy**

    Implement Redis for high-read data.

    ```go
    val, err := rdb.Get(ctx, "key").Result()
    if err == redis.Nil {
        // Cache miss: Load from DB and set cache
        val = loadFromDB()
        rdb.Set(ctx, "key", val, 10*time.Minute)
    }
    ```

6. **Verification**

    Re-run benchmarks to verify improvement.

    // turbo

    ```bash
    go test -bench=. -benchmem
    ```
