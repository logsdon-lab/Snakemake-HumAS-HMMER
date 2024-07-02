# Snakemake HumAS-HMMER
[![CI](https://github.com/koisland/Smk-HumAS-HMMER/actions/workflows/main.yml/badge.svg)](https://github.com/koisland/Smk-HumAS-HMMER/actions/workflows/main.yml)

This is a port of the following:
* https://github.com/fedorrik/HumAS-HMMER_for_AnVIL/blob/main/hmmer-run.sh
* https://github.com/fedorrik/HumAS-HMMER_for_AnVIL/blob/main/hmmer-run_SF.sh

### Input
* Input directory or list of fasta files.

### Output
1. Alpha-satellite higher order repeat (HOR) BED file
2. Alpha-satellite HOR suprachromosomal families BED file.

### Usage

Clone the repository.
```bash
git clone git@github.com:logsdon-lab/Snakemake-HumAS-HMMER.git
cd Snakemake-HumAS-HMMER
```

Modify `config.yaml` as needed.
```yaml
# Input directory
input_dir: "test/"
# Output directory
output_dir: "test/"
# Optional workflow directories.
logs_dir: "logs/humas_hmmer"
benchmarks_dir: "benchmarks/humas_hmmer"
# Hidden markov model. Should coincide with the rule of choice: SF or AS-HOR.
model: "data/AS-SFs-hmmer3.0.290621.hmm"
# nhmmer threads and memory.
threads: 12
mem: 4
```

Then specify either `humas_hmmer_as_hor` or `humas_hmmer_sf` when running the workflow.
```bash
snakemake -c 12 --config output_dir=test2 --configfile config/config.yaml -np humas_hmmer_as_hor
```
* `humas_hmmer_as_hor` annotates alpha-satellite higher order repeats in the input sequence.
    * This is the default.
* `humas_hmmer_sf` annotates alpha-satellite HOR suprachromosomal families in the input sequence.

### Module
To include this workflow as a module.

```python
module HumAS_HMMER:
    snakefile:
        github(
            "koisland/Smk-HumAS-HMMER",
            path="workflow/Snakefile",
            branch="main"
        )
    config: config

use rule * from HumAS_HMMER as test_*
```

Then, using checkpoints, pass in an input dir with `.fa` files.
```python
import os

checkpoint create_dir_with_fa_files:
    # Create a directory with .fa files.
    ...

    output:
        directory("output")


def humas_hmmer_outputs(wc):
    fa_file_dir = checkpoints.create_dir_with_fa_files.get(**wc).output
    fnames = glob_wildcards(os.path.join(fa_file_dir, "{fname}.fa")).fname
    return {
        "overlaps": expand(
            rules.test_filter_hmm_res_overlaps_as_hor.output, fname=fnames
        ),
        "final": expand(rules.test_filter_final_hmm_res_as_hor.output, fname=fnames),
    }

rule run_humas_hmmer_for_anvil:
    input:
        unpack(humas_hmmer_outputs),
    output:
        temp(touch("/tmp/humas_hmmer.done")),
```
