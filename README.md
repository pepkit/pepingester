# pepingester

`pepingester` is a small command line tool that helps you load up a database of PEPs. It uses [`looper`](https://looper.databio.org/en/latest/) to handle job submission and requires a PEP of PEPs (a POP) that points to a sample table which holds information about each PEP to be uploaded. An example sample table might look like:

| sample_name                                                                     | namespace | project_name | type | location                     |
|---------------------------------------------------------------------------------|-----------|--------------|------|------------------------------|
| demo-biocproject                                                                | demo      | biocproject  | path | /path/to/project_config.yaml |
| demo-piface,demo,piface,path,../pephub/examples/demo/piface/project_config.yaml | demo      | piface       | path | /path/to/project_config.yaml |
| geo-gse12345678                                                                 | geo       | gse12345678  | geo  | gse12345678                  |