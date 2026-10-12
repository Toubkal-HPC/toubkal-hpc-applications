#!/bin/bash

#SBATCH --job-name=abaqus_example
#SBATCH --output=abaqus_output_%A.out
#SBATCH --error=abaqus_error_%A.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:20:00

ml load cpu_cclake/abaqus/2025

# 1 MPI TASK, with 4 THREADS 
abaqus job=example input=example.inp cpus=4 interactive
