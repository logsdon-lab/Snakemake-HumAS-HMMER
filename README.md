# Snakemake HumAS-HMMER
[![CI](https://github.com/koisland/Smk-HumAS-HMMER/actions/workflows/main.yml/badge.svg)](https://github.com/koisland/Smk-HumAS-HMMER/actions/workflows/main.yml)

This is a port of the following:
* https://github.com/fedorrik/HumAS-HMMER_for_AnVIL/blob/main/hmmer-run.sh
* https://github.com/fedorrik/HumAS-HMMER_for_AnVIL/blob/main/hmmer-run_SF.sh

### Usage
Modify `config.yaml` as needed.

```yaml
input_dir: "test/"
output_dir: "test/"
model: "data/AS-SFs-hmmer3.0.290621.hmm"
threads: 12
```

```bash
snakemake -np -c 12 --configfile config/config.yaml
```

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
