# D-PLACE aggregated dataset

[![CLDF validation](https://github.com/d-place/dplace-cldf/workflows/CLDF-validation/badge.svg)](https://github.com/d-place/dplace-cldf/actions?query=workflow%3ACLDF-validation)

## How to cite

If you use these data please cite
- the original source
  > Kathryn R. Kirby, Russell D. Gray, Simon J. Greenhill, Fiona M. Jordan, Stephanie Gomes-Ng, Hans-Jörg Bibiko, Damián E. Blasi, Carlos A. Botero, Claire Bowern, Carol R. Ember, Dan Leehr, Bobbi S. Low, Joe McCarter, William Divale, and Michael C. Gavin. (2016). D-PLACE: A Global Database of Cultural, Linguistic and Environmental Diversity. PLoS ONE, 11(7): e0158391. doi:10.1371/journal.pone.0158391.
- the derived dataset using the DOI of the [particular released version](../../releases/) you were using

## Description


This dataset is licensed under a CC-BY-NC-4.0 license

Available online at https://d-place.org




![](map.png)




The D-PLACE CLDF dataset aggregates data from
- individual [D-PLACE datasets](https://zenodo.org/communities/phlorest),
- [Phlorest phylogenies](https://zenodo.org/communities/phlorest) and
- [Glottolog](https://glottolog.org) classification trees.

It supersedes the dataset formerly curated at
[D-PLACE/dplace-data](https://github.com/D-PLACE/dplace-data). Thus, for earlier releases of
aggregated D-PLACE data, refer to https://zenodo.org/doi/10.5281/zenodo.596376


### Data model

The tables and columns in the D-PLACE CLDF dataset are described at [cldf/README.md](cldf).
The relations between the tables are depicted in the entity-relationship diagram below. Note that
this diagram uses CLDF terms - i.e. the terms used as `dc:conformsTo` and `propertyUrl`s properties
in the [CLDF metadata](cldf/StructureDataset-metadata.json) - to refer to tables and columns.

![](erd.svg)


### D-PLACE Datasets

| title | version | DOI |
|:---------------------------------------------------------------------------------------------------------------------------------|:----------|:-------------------------------------------------------------------|
| D-PLACE dataset derived from Binford 2001 'Constructing Frames of Reference' | v3.2 | [10.5281/zenodo.17580172](https://doi.org/10.5281/zenodo.17580172) |
| D-PLACE dataset derived from Robert L. Carneiro's Dataset (4th Edition) | v1.0.1 | [10.5281/zenodo.17607789](https://doi.org/10.5281/zenodo.17607789) |
| D-PLACE dataset derived from Robert L. Carneiro's Dataset (6th edition) | v1.0.1 | [10.5281/zenodo.17607723](https://doi.org/10.5281/zenodo.17607723) |
| D-PLACE dataset derived from Bertolo et al. 2023 'Cross-cultural music corpus: The Expanded Natural History of Song Discography' | v3.2 | [10.5281/zenodo.17600888](https://doi.org/10.5281/zenodo.17600888) |
| D-PLACE dataset derived from Murdock et al. 1999 'Ethnographic Atlas' | v3.2.1 | [10.5281/zenodo.17602181](https://doi.org/10.5281/zenodo.17602181) |
| D-PLACE dataset derived from Lima-Ribeiro et al. 2015 'ecoClimate' | v3.2 | [10.5281/zenodo.17601193](https://doi.org/10.5281/zenodo.17601193) |
| D-PLACE dataset derived from 'Global Multi-resolution Terrain Elevation Data 2010' | v3.2 | [10.5281/zenodo.17601586](https://doi.org/10.5281/zenodo.17601586) |
| D-PLACE dataset derived from Wessel and Smith 2015 'Global Self-consistent, Hierarchical, High-resolution Geography Database' | v3.2 | [10.5281/zenodo.17601634](https://doi.org/10.5281/zenodo.17601634) |
| D-PLACE dataset derived from Jenkins et al. 2013 'Global patterns of terrestrial vertebrate diversity and conservation' | v3.2 | [10.5281/zenodo.17601675](https://doi.org/10.5281/zenodo.17601675) |
| D-PLACE dataset derived from Kreft and Jetz 2007 'Global patterns and determinants of vascular plant diversity' | v3.2 | [10.5281/zenodo.17601737](https://doi.org/10.5281/zenodo.17601737) |
| D-PLACE dataset derived from NASA TERRA/MODIS 'Net Primary Productivity' | v3.2 | [10.5281/zenodo.17601800](https://doi.org/10.5281/zenodo.17601800) |
| D-PLACE dataset derived from Murdock and White 1969 'Standard Cross-Cultural Sample' | v3.2 | [10.5281/zenodo.17601873](https://doi.org/10.5281/zenodo.17601873) |
| D-PLACE dataset derived from Olson et al. 2001 'Terrestrial Ecoregions of the World' | v3.2 | [10.5281/zenodo.17601927](https://doi.org/10.5281/zenodo.17601927) |
| D-PLACE dataset derived from Jorgensen 1980 'Western Indians' | v3.2 | [10.5281/zenodo.17602055](https://doi.org/10.5281/zenodo.17602055) |

### Phlorest Phylogenies

| title | version | DOI |
|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------|:-------------------------------------------------------------------|
| Phlorest phylogeny derived from Atkinson 2006 'From Species to Languages: a phylogenetic approach to human prehistory' | v1.3 | [10.5281/zenodo.17581426](https://doi.org/10.5281/zenodo.17581426) |
| Phlorest phylogeny derived from Birchall et al. 2016 'A combined comparative and phylogenetic analysis of the Chapacuran language family' | v1.2 | [10.5281/zenodo.17581525](https://doi.org/10.5281/zenodo.17581525) |
| Phlorest phylogeny derived from Bouckaert et al. 2012 'Mapping the Origins and Expansion of the Indo-European Language Family' | v1.2 | [10.5281/zenodo.17581594](https://doi.org/10.5281/zenodo.17581594) |
| Phlorest phylogeny derived from Bouckaert et al. 2018 'The origin and expansion of Pama–Nyungan languages across Australia' | v1.2 | [10.5281/zenodo.17581679](https://doi.org/10.5281/zenodo.17581679) |
| Phlorest phylogeny derived from Bowern & Atkinson 2012 'Computational phylogenetics and the internal structure of Pama-Nyungan' | v1.2 | [10.5281/zenodo.17582392](https://doi.org/10.5281/zenodo.17582392) |
| Phlorest phylogeny derived from Chacon & List 2015 'Improved computational models of sound change shed light on the history of the Tukanoan languages' | v1.2 | [10.5281/zenodo.17582630](https://doi.org/10.5281/zenodo.17582630) |
| Phlorest phylogeny derived from Chang et al. 2015 'Ancestry-constrained phylogenetic analysis supports the Indo-European steppe hypothesis' | v1.2 | [10.5281/zenodo.17583531](https://doi.org/10.5281/zenodo.17583531) |
| Phlorest phylogeny derived from De Filippo et al. 2012 'Bringing together linguistic and genetic evidence to test the Bantu expansion' | v1.2 | [10.5281/zenodo.17583636](https://doi.org/10.5281/zenodo.17583636) |
| Phlorest phylogeny derived from Dunn et al. 2011 'Evolved structure of language shows lineage-specific trends in word-order universals' | v1.2 | [10.5281/zenodo.17583660](https://doi.org/10.5281/zenodo.17583660) |
| Phlorest phylogeny derived from Gray et al. 2009 'Language phylogenies reveal expansion pulses and pauses in Pacific settlement' | v1.2 | [10.5281/zenodo.17583742](https://doi.org/10.5281/zenodo.17583742) |
| Phlorest phylogeny derived from Greenhill 2015 'TransNewGuinea.org: An Online Database of New Guinea Languages' | v1.2 | [10.5281/zenodo.17583895](https://doi.org/10.5281/zenodo.17583895) |
| Phlorest phylogeny derived from Greenhill, Haynie et al. 2023 'Uto-Aztecan (Greenhill, Haynie et al.)' | v1.0 | [10.5281/zenodo.17572679](https://doi.org/10.5281/zenodo.17572679) |
| Phlorest phylogeny derived from Grollemund et al. 2015 'Bantu expansion shows habitat alters the route and pace of human dispersals' | v1.2 | [10.5281/zenodo.17583936](https://doi.org/10.5281/zenodo.17583936) |
| Phlorest phylogeny derived from Hartmann & Walkden 2024 'The strength of the phylogenetic signal in syntactic data' | v1.0 | [10.5281/zenodo.17578198](https://doi.org/10.5281/zenodo.17578198) |
| Phlorest phylogeny derived from Holden et al. 2005 'Comparison of Maximum Parsimony and Bayesian Bantu Language trees' | v1.0 | [10.5281/zenodo.17578733](https://doi.org/10.5281/zenodo.17578733) |
| Phlorest phylogeny derived from Honkola et al. 2013 'Cultural and climatic changes shape the evolutionary history of the Uralic languages' | v1.2 | [10.5281/zenodo.17587191](https://doi.org/10.5281/zenodo.17587191) |
| Phlorest phylogeny derived from Hruschka et al. 2015 'Detecting regular sound changes in linguistics as events of concerted evolution' | v1.2 | [10.5281/zenodo.17587592](https://doi.org/10.5281/zenodo.17587592) |
| Phlorest phylogeny derived from Kitchen et al. 2009 'Bayesian phylogenetic analysis of Semitic languages identifies an Early Bronze Age origin of Semitic in the Near East' | v1.2 | [10.5281/zenodo.17588546](https://doi.org/10.5281/zenodo.17588546) |
| Phlorest phylogeny derived from Kolipakam et al. 2018 'A Bayesian phylogenetic study of the Dravidian language family' | v1.2 | [10.5281/zenodo.17588770](https://doi.org/10.5281/zenodo.17588770) |
| Phlorest phylogeny derived from Lee 2015 'A Sketch of Language History in the Korean Peninsula' | v1.2 | [10.5281/zenodo.17588865](https://doi.org/10.5281/zenodo.17588865) |
| Phlorest phylogeny derived from Lee & Hasegawa 2011 'Bayesian phylogenetic analysis supports an agricultural origin of Japonic languages' | v1.2 | [10.5281/zenodo.17588983](https://doi.org/10.5281/zenodo.17588983) |
| Phlorest phylogeny derived from Lee & Hasegawa 2013 'Evolution of the Ainu Language in Space and Time' | v1.2 | [10.5281/zenodo.17589029](https://doi.org/10.5281/zenodo.17589029) |
| Phlorest phylogeny derived from Michael et al. 2015 'A Bayesian Phylogenetic Classification of Tupi-Guarani' | v1.1 | [10.5281/zenodo.17578947](https://doi.org/10.5281/zenodo.17578947) |
| Phlorest phylogeny derived from Rexová et al. 2006 'Cladistic analysis of Bantu languages: a new tree based on combined lexical and grammatical data' | v1.0 | [10.5281/zenodo.17579490](https://doi.org/10.5281/zenodo.17579490) |
| Phlorest phylogeny derived from Robinson and Holton 2012 'Internal Classification of the Alor-Pantar Language Family Using Computational Methods Applied to the Lexicon' | v1.2 | [10.5281/zenodo.17590954](https://doi.org/10.5281/zenodo.17590954) |
| Phlorest phylogeny derived from Sagart et al. 2019 'Dated language phylogenies shed light on the ancestry of Sino-Tibetan' | v1.2 | [10.5281/zenodo.17591022](https://doi.org/10.5281/zenodo.17591022) |
| Phlorest phylogeny derived from Sicoli & Holton 2014 'Linguistic phylogenies support back-migration from Beringia to Asia' | v1.2 | [10.5281/zenodo.17591308](https://doi.org/10.5281/zenodo.17591308) |
| Phlorest phylogeny derived from Walker & Ribeiro 2011 'Bayesian phylogeography of the Arawak expansion in lowland South America' | v1.2 | [10.5281/zenodo.17591444](https://doi.org/10.5281/zenodo.17591444) |
| Phlorest phylogeny derived from Zhang et al 2019 'Phylogenetic evidence for Sino-Tibetan origin in northern China in the Late Neolithic' | v1.2 | [10.5281/zenodo.17591786](https://doi.org/10.5281/zenodo.17591786) |






## CLDF Datasets

The following CLDF datasets are available in [cldf](cldf):

- CLDF [StructureDataset](https://github.com/cldf/cldf/tree/master/modules/StructureDataset) at [cldf/StructureDataset-metadata.json](cldf/StructureDataset-metadata.json)