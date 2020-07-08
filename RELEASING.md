# Releasing dplace-cldf

dplace-cldf is derived from released versions on dplace-data. Thus, releasing
dplace-cldf is done as follows:

1. Check out a local clone of dplace-data to a release tag.
2. Run `dplace cldf` as follows:
   ```shell script
   dplace --repos ../dplace-data/ cldf ../../glottolog/glottolog v3.3 --cldf_repos ../dplace-cldf/
   ```
   Notes:
   - The Glottolog version tag should be the one used to compile the dplace-data
     release. It can be looked up in https://github.com/D-PLACE/dplace-data/blob/master/phylogenies/index.csv
   - If the data contains value with undefined `Code_ID`, this code ID can be ignored - i.e. removed in the CLDF data - passing the `--fix-code-id` flag.
3. Update `.zenodo.json`.
4. Commit, tag and push the changes.
5. Create a release on GitHub, thereby triggering archiving with Zenodo.
6. Update the release description on GitHub with the DOI.

