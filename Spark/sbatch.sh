#!/bin/bash
#
#SBATCH --job-name="spark-pi-example"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8           #number of CPU cores
#SBATCH --mem=20G                    #total RAM 
#SBATCH --output=slurm_%j.out
#SBATCH --error=slurm_%j.err


ml load Spark/3.5.0-foss-2023a

spark-submit --master 'local[8]' \
    $SPARK_HOME/examples/src/main/python/pi.py 10
