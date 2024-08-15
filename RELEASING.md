# Releasing dplace-cldf

1. Release all consituent datasets and phylogenies, compiled against the latest Glottolog release.
2. Run
   ```shell
   cldfbench download cldfbench_dplace.py
   ```

```shell
cldfbench makecldf cldfbench_dplace.py --glottolog-version v5.0
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

4. Edit `CHANGELOG.md`.
5. Commit, tag and push the changes.
6. Create a release on GitHub, thereby triggering archiving with Zenodo.
7. Update the release description on GitHub with the DOI.
