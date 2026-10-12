# Abaqus Example Run

This example demonstrates how to run a simple Abaqus finite element case on the CPU partition.

The example uses the `example.inp` input file, which defines a simple tetrahedral element with an elastic steel material.

The job uses:

```text
Abaqus 2025
1 MPI task
4 CPU cores
```

Submit the job with:

```bash
sbatch sbatch.sh
```

The calculation is launched with:

```bash
abaqus job=example input=example.inp cpus=4 interactive
```

The required Abaqus module is loaded automatically inside the submission script:

```bash
cpu_cclake/abaqus/2025
```

Make sure `example.inp` is present in the submission directory before launching the job.
