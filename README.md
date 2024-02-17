# Snakemake HumAS-HMMER
This is a port of the following:
* https://github.com/fedorrik/HumAS-HMMER_for_AnVIL/blob/main/hmmer-run.sh
* https://github.com/fedorrik/HumAS-HMMER_for_AnVIL/blob/main/hmmer-run_SF.sh

### Usage
```bash
snakemake -np --configfile config/config.yaml
```

### Module
To include this workflow.
```python
module HumAS_HMMER:
    snakefile:
        github(
            "koisland/Smk-HumAS-HMMER",
            path="workflow/Snakefile",
            branch="main"
        )
    config: config

use rule * from HumAS_HMMER as *
```