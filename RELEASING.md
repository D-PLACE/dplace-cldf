# Releasing dplace-cldf

1. Release all consituent datasets and phylogenies, compiled against the latest Glottolog release.
2. Run
   ```shell
   cldfbench download cldfbench_dplace.py
   ```

```shell
cldfbench makecldf cldfbench_dplace.py --glottolog-version v4.8
```

```shell
cldf validate cldf
pytest
```

```shell
cldfbench cldfreadme cldfbench_dplace.py
cldfbench readme cldfbench_dplace.py
cldfbench zenodo --communities dplace cldfbench_dplace.py
```

```shell
cldfbench cldfviz.map cldf --pacific-centered --format png --width 20 --output map.png --with-ocean --language-properties Contribution_ID --language-filters '{"type":"society"}'
```

```shell
cldferd --format compact.svg cldf > erd.svg
```

FIXME: adapt to new data layout!

1. Check out a local clone of dplace-data to a release tag.
2. Run `dplace cldf` as follows:
   ```shell script
   dplace --repos ../dplace-data/ cldf ../../glottolog/glottolog v3.3 --cldf-repos ../dplace-cldf/
   ```
   Notes:
   - The Glottolog version tag should be the one used to compile the dplace-data
     release. It can be looked up in https://github.com/D-PLACE/dplace-data/blob/master/phylogenies/index.csv
   - If the data contains value with undefined `Code_ID`, this code ID can be ignored - i.e. removed in the CLDF data - passing the `--fix-code-id` flag.
3. Update `.zenodo.json`.
4. Commit, tag and push the changes.
5. Create a release on GitHub, thereby triggering archiving with Zenodo.
6. Update the release description on GitHub with the DOI.
