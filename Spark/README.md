# Apache Spark Example Run

This example demonstrates how to run a simple Apache Spark workload on a single compute node using Spark local mode.

The job uses:

```text id="6m5cu1"
Spark 3.5.0
1 node
8 CPU cores
20 GB RAM
```

Submit the job with:

```bash id="3squ5r"
sbatch sbatch.sh
```

The example runs Spark’s bundled Python Pi estimation program with:

```bash id="ku2zqm"
spark-submit --master 'local[8]' \
    $SPARK_HOME/examples/src/main/python/pi.py 10
```

With `local[8]`, Spark runs as a single local application process on the allocated node and can execute up to **8 tasks concurrently**.

This mode is suitable for single-node execution. If the workload requires **multiple Spark executors/workers across multiple nodes**, local mode is not sufficient. In that case, a Spark cluster deployment is required, with a **Spark master and one or more workers**, and the application should be submitted to that cluster instead of using `local[...]`.


