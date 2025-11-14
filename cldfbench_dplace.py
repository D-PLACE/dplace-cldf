import pathlib
import argparse
import functools
import itertools
import collections

from csvw import Datatype
from csvw.dsv import UnicodeWriter
from pycldf import Dataset as CLDFDataset, Source
from pycldf.trees import TreeTable
from cldfcatalog import Repository
from clldutils.path import git_describe
from clldutils.markup import add_markdown_text, Table
from cldfzenodo import API
from pydplace.dataset import DatasetWithSocieties, data_schema
from commonnexus import Nexus
from commonnexus.blocks.trees import Trees

OBSOLETE_CONTRIBUTIONS = {
    'D-PLACE': [
        'carneiro',  # Superseded by carneiro6
        'pulotu',  # Keep separate for the time being
    ],
    'phlorest': [],
}
README = """
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

{}

### Phlorest Phylogenies

{}
"""


def update(d, tag):
    repo = Repository(d)
    repo.update()
    repo.checkout(tag)


def glottolog_version(d):
    ds = CLDFDataset.from_metadata(
        d / 'cldf' / '{}-metadata.json'.format(
            'StructureDataset' if d.parent.name == 'datasets' else 'Generic'))
    for obj in ds.properties["prov:wasDerivedFrom"]:
        if obj["rdf:about"] == 'https://github.com/glottolog/glottolog':
            return obj['dc:created']


class Dataset(DatasetWithSocieties):
    dir = pathlib.Path(__file__).parent
    id = "dplace"

    def iter_contributions(self, args, type_=None):
        import re
        from cldfzenodo import API

        DSID_PATTERN = re.compile(
            r'files/(?P<org>(phlorest)|(D\-PLACE))/(?P<dsid>[a-z_\-0-9]+?)\-(?P<tag>v[0-9.]+)')
        clones = {
            'phlorest': {p.name: p for p in self.raw_dir.joinpath('phylogenies').iterdir()},
            'D-PLACE': {p.name: p for p in self.raw_dir.joinpath('datasets').iterdir()},
        }

        def iter_records():
            for rec in API.iter_records(community='dplace'):
                m = DSID_PATTERN.search(rec.download_urls[0])
                if not m:
                    continue
                dsid, org, tag = m.group('dsid'), m.group('org'), m.group('tag')
                tag = tag.rstrip('.')
                if not (org == 'phlorest' or dsid.startswith('dplace-dataset')):
                    continue
                dsid = dsid.replace('dplace-dataset-', '')
                if dsid in OBSOLETE_CONTRIBUTIONS[org]:
                    continue
                if dsid not in clones[org]:
                    args.log.warning('No clone for repository {}/{}'.format(org, dsid))
                else:
                    dsdir = clones[org][dsid]
                    if (type_ is None) or (type_ == dsdir.parent.name):
                        yield dsdir, rec, dsid, org, tag

        yield from sorted(iter_records(), key=lambda i: (i[3], i[2]))

    def cmd_download(self, args: argparse.Namespace):
        glottolog_versions = collections.defaultdict(list)
        with UnicodeWriter(self.etc_dir / 'contributions.csv') as writer:
            writer.writerow(['type', 'name', 'tag', 'doi', 'cit', 'bib'])
            for d, rec, dsid, org, tag in self.iter_contributions(args):
                update(d, tag)
                glottolog_versions[glottolog_version(d)].append((org, dsid))
                dsid = 'dplace-{}-{}'.format(
            'phylogeny' if org == 'phlorest' else 'dataset', dsid)
                writer.writerow([
                    d.parent.name,
                    d.name,
                    tag,
                    rec.doi,
                    rec.get_citation(API),
                    rec.get_bibtex(bibid=dsid)])
        if len(glottolog_versions) > 1:
            args.log.warning('multiple Glottolog versions!')
            print(glottolog_versions)
        else:
            args.log.info('Contributions compiled with Glottolog version {}'.format(
                list(glottolog_versions.keys())[0]))

    @functools.cached_property
    def contrib_meta(self):
        return {
            (row['type'], row['name']): row
            for row in self.etc_dir.read_csv('contributions.csv', dicts=True)}

    def add_contribution(self, writer, dsdir, cldf, type_, desc=None):
        repo = Repository(dsdir)
        writer.cldf.add_provenance(wasDerivedFrom=[repo.json_ld()])
        src = None
        meta = self.contrib_meta[(dsdir.parent.name, dsdir.name)]
        if meta:
            src = Source.from_bibtex(meta['bib'])
            #try:
            writer.cldf.add_sources(src)
            #except:
            #    assert meta['name'] == 'carneiro'
        res = dict(
            ID=('dplace-phylogeny-' if type_ == 'phylogeny' else '') + cldf.properties['rdf:ID'],
            Name=cldf.properties['dc:title'],
            Description=desc or cldf.properties.get('dc:description'),
            DOI=meta['doi'],
            Contributor=src['author'] if src else None,
            Citation='{}\n{}'.format(meta.get('cit', ''), cldf.properties.get('dc:bibliographicCitation', '')).strip(),
            Source=[src.id] if src else [],
            type=type_,
        )
        writer.objects['ContributionTable'].append(res)
        return res

    def cmd_makecldf(self, args):
        data_schema(args.writer.cldf)
        self.schema(args.writer.cldf)
        self.add_schema(args.writer.cldf)
        self.cldf_dir.joinpath('trees').mkdir(exist_ok=True)

        # -------------
        # Add datasets:
        # -------------
        # Keep track which Glottolog languages are represented in D-PLACE:
        glangs = {l.id: l for l in args.glottolog.api.languoids()}
        glangs_in_dplace = {
            lid: set() for lid, l in glangs.items()
            if l.level == args.glottolog.api.languoid_levels.language}
        assert glangs_in_dplace
        glangs_with_parents = {l.id: {li[1] for li in l.lineage} for l in glangs.values()}
        for dsdir, rec, dsid, org, tag in self.iter_contributions(args, type_='datasets'):
            self.add_dataset(
                args.writer,
                dsdir,
                args.glottolog.api,
                glangs,
                glangs_in_dplace,
                glangs_with_parents)

        args.writer.cldf['ParameterTable', 'category'].datatype = Datatype.fromvalue(
            dict(
                base="string",
                format="|".join(sorted(set(itertools.chain(
                    *[r['category'] for r in args.writer.objects['ParameterTable']]))))))

        # --------------------------
        # Add Glottolog phylogenies:
        # --------------------------
        tag, doi, cit, bib = API.get_github_release_info(
            'glottolog/glottolog', tag=args.glottolog_version)
        args.writer.cldf.add_sources(bib)

        for gc in list(glangs_in_dplace.keys()):
            if not glangs_in_dplace[gc]:
                del glangs_in_dplace[gc]
        families_in_dplace = collections.defaultdict(set)
        for gc in glangs_in_dplace:
            if glangs[gc].lineage:
                families_in_dplace[glangs[gc].lineage[0][1]].add(gc)
        for gc, ext in families_in_dplace.items():
            if len(ext) > 1:
                self.add_glottolog_classification(
                    args.writer,
                    glangs[gc],
                    {code: glangs[code] for code in ext},
                    args.glottolog_version,
                    bib,
                    doi,
                    cit)

        # -------------------------
        # Add Phlorest phylogenies:
        # -------------------------
        for dsdir, rec, dsid, org, tag in self.iter_contributions(args, type_='phylogenies'):
            self.add_phlorest_phylogeny(args.writer, dsdir)

    def cmd_readme(self, args):
        def table(contribs):
            t = Table('title', 'version', 'DOI')
            for contrib in contribs:
                bib = Source.from_bibtex(contrib['bib'])
                t.append([
                    bib['title'],
                    contrib['tag'],
                    '[{0}](https://doi.org/{0})'.format(contrib['doi'])])
            return t.render()

        contribs = self.etc_dir.read_csv('contributions.csv', dicts=True)
        return add_markdown_text(
            super().cmd_readme(args),
            "\n\n{}\n\n".format(README.format(
                table(c for c in contribs if c['type'] == 'datasets'),
                table(c for c in contribs if c['type'] == 'phylogenies'))),
            section='Description')

    def add_schema(self, cldf):
        t = cldf.add_component('MediaTable')
        t.common_props['dc:description'] = \
            ("For better re-usability, D-PLACE provides the Glottolog classification trees and "
             "Phlorest phylogenies in the NEXUS file format.")
        cldf.add_columns(
            'LanguageTable',
            {
                'name': 'type',
                'datatype': {'base': 'string', 'format': 'society|languoid'},
            },
            {
                'name': 'Language_Level_Glottocodes',
                'separator': ' ',
                'dc:description':
                    'Glottocode(s) of the language-level languoid(s) in Glottolog associated with '
                    'the languoid specified by Glottocode. Matches the "Glottocode" column for '
                    'languages, but differs for dialects and lists all contained languages for '
                    'subgroups. The language-level Glottocodes can be used to match societies to '
                    'languages in the Glottolog classification trees.',
            },
            {
                'name': 'ISO639P3code',
                'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#iso639P3code',
            },
            {
                'name': 'Contribution_ID',
                'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#contributionReference',
            },
        )
        cldf['LanguageTable'].common_props['dc:description'] = \
            ('The aggregated D-PLACE data lists two kinds of entities in its LanguageTable: '
             'Societies, i.e. cultural groups for which D-PLACE datasets provide data, and '
             'Languoids, i.e. language (varieties) which are referenced in Phlorest phylogenies. '
             'The two kinds are marked as "society" and "languoid"respectively in the type column.')
        cldf.add_columns(
            'ParameterTable',
            {
                'name': 'Contribution_ID',
                'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#contributionReference',
            },
        )
        t = cldf.add_component(
            'ContributionTable',
            {
                'name': 'DOI',
                'valueUrl': 'https://doi.org/{DOI}',
            },
            {
                'name': 'type',
                'datatype': {'base': 'string', 'format': 'dataset|phylogeny'},
                'dc:description':
                    'D-PLACE aggregates two kinds of data: D-PLACE datasets, i.e. lists variables '
                    'and coded values for cultural groups and language phylogenies from Phlorest. ',
            },
            {
                'name': 'Source',
                'separator': ';',
                'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#source'
            }
        )
        t.common_props['dc:description'] = \
            ("Both, individual D-PLACE datasets as well as Phlorest phylogenies and Glottolog "
             "classification trees are citable units - and should be cited, if their data is used.")
        t = cldf.add_component(
            'TreeTable',
            {
                'name': 'Contribution_ID',
                'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#contributionReference',
            },
        )
        t.common_props['dc:description'] = \
            ("D-PLACE contains the summary trees of Phlorest phylogenies and classification trees "
             "for Glottolog families which are associated with at least two societies in D-PLACE.")

    def add_dataset(self,
                    writer,
                    dsdir,
                    glottolog,
                    glangs,
                    glangs_in_dplace,
                    glangs_with_parents):
        def iter_child_languages(gc):
            for lg in glangs.values():
                if lg.level == glottolog.languoid_levels.language:
                    if gc in glangs_with_parents[lg.id]:
                        yield lg

        ds = CLDFDataset.from_metadata(dsdir / 'cldf' / 'StructureDataset-metadata.json')
        contrib = self.add_contribution(writer, dsdir, ds, 'dataset')
        prefix = contrib['ID'].replace('dplace-dataset-', '')

        if 'LanguageTable' in ds:
            for row in ds.iter_rows('LanguageTable'):
                if row['Glottocode']:
                    if row['Glottocode'] in glangs_in_dplace:
                        glangs_in_dplace[row['Glottocode']].add(row['Glottocode'])
                        llgcs = [row['Glottocode']]
                    else:
                        for parent in glangs_with_parents[row['Glottocode']]:
                            if parent in glangs_in_dplace:
                                glangs_in_dplace[parent].add(row['Glottocode'])
                                llgcs = [parent]
                                break
                        else:
                            llgcs = [lg.id for lg in iter_child_languages(row['Glottocode'])]
                else:
                    llgcs = []
                row['type'] = 'society'
                row['Language_Level_Glottocodes'] = llgcs
                row['Contribution_ID'] = ds.properties['rdf:ID']
                writer.objects['LanguageTable'].append(row)

        for row in ds.iter_rows('ParameterTable'):
            #
            # FIXME: normalize: Labor/Labour!
            #
            row['category'] = sorted({c.split(':')[0].strip() for c in row['category']})
            row['Contribution_ID'] = ds.properties['rdf:ID']
            writer.objects['ParameterTable'].append(row)

        if 'CodeTable' in ds:
            for row in sorted(ds.iter_rows('CodeTable'), key=lambda r: (r['Var_ID'], int(r['ord'] or -1))):
                writer.objects['CodeTable'].append(row)

        for vid, row in enumerate(sorted(ds.iter_rows('ValueTable'), key=lambda r: (r['Var_ID'], r['Soc_ID']))):
            row['ID'] = '{}-{}'.format(prefix, vid + 1)
            writer.objects['ValueTable'].append(row)

        for src in ds.sources.items():
            if src.id in writer.cldf.sources._bibdata.entries:
                # Merge!
                if ('url' in src) and ('url' not in writer.cldf.sources._bibdata.entries[src.id].fields):
                    writer.cldf.sources._bibdata.entries[src.id].fields['url'] = src['url']
            else:
                writer.cldf.add_sources(src)

    def add_nexus(self, writer, desc, nwk, mid):
        assert nwk
        trees_dir = self.cldf_dir / 'trees'
        nex = Nexus('#NEXUS\n[{}]\n'.format(desc))
        nex.append_block(Trees.from_data(('summary', nwk, True)))
        nex.to_file(trees_dir / '{}.trees'.format(mid))
        nex = trees_dir / '{}.trees'.format(mid)

        writer.objects['MediaTable'].append(dict(
            ID=nex.stem,
            Media_Type='text/plain',
            Download_URL='file:///trees/{}'.format(nex.name),
        ))

    def add_glottolog_classification(
            self, writer, family, ext, glottolog_version, bib, doi, cit):
        def drop_internal_names(n):
            if not n.is_leaf:
                n.name = None

        nwk = family.newick_node(template='{l.id}')
        nwk.prune_by_names([lg.id for lg in ext.values()], inverse=True)
        nwk.remove_redundant_nodes(keep_leaf_name=True)
        nwk.visit(drop_internal_names)
        desc = ('Classification of {} languages in Glottolog {} pruned to languages '
                'represented in D-PLACE'.format(family.name, glottolog_version))
        writer.objects['ContributionTable'].append(dict(
            ID=family.id,
            Name="{} (Glottolog {})".format(family.name, glottolog_version),
            Description=desc,
            Contributor=bib['author'],
            type='phylogeny',
            DOI=doi,
            Citation=cit,
            Source=[bib.id],
        ))
        for n in nwk.walk():
            if n.name:
                assert n.is_leaf
                writer.objects['LanguageTable'].append(dict(
                    ID=n.name,
                    Glottocode=n.name,
                    Name=ext[n.name].name,
                    Latitude=ext[n.name].latitude,
                    Longitude=ext[n.name].longitude,
                    ISO639P3code=ext[n.name].iso,
                    type='languoid',
                    Contribution_ID=family.id,
                ))

        self.add_nexus(writer, desc, nwk, family.id)
        writer.objects['TreeTable'].append(dict(
            ID=family.id,
            Name='summary',
            Description='',
            Tree_Is_Rooted=True,
            Tree_Type='summary',
            Tree_Branch_Length_Unit=None,
            Media_ID=family.id,
            Contribution_ID=family.id,
            Source=[bib.id],
        ))

    def add_phlorest_phylogeny(self, writer, dsdir):
        ds = CLDFDataset.from_metadata(dsdir / 'cldf' / 'Generic-metadata.json')
        dsid = ds.properties['rdf:ID']
        desc = 'Summary tree of the {}'.format(ds.properties['dc:title'])
        contrib = self.add_contribution(writer, dsdir, ds, 'phylogeny', desc=desc)

        names = {}
        for row in ds.iter_rows('LanguageTable'):
            row['type'] = 'languoid'
            names[row['ID']] = '{}_{}'.format(dsid, row['ID'])
            row['ID'] = names[row['ID']]
            row['Contribution_ID'] = contrib['ID']
            writer.objects['LanguageTable'].append(row)

        nwk = None
        for tree in TreeTable(ds):
            if tree.tree_type == 'summary':
                nwk = tree.newick()
                nwk.rename(**names)
                nwk.strip_comments()
                break

        self.add_nexus(writer, desc, nwk, dsid)
        writer.objects['TreeTable'].append(dict(
            ID=ds.properties['rdf:ID'],
            Name='summary',
            Description='',
            Tree_Is_Rooted=True,
            Tree_Type='summary',
            Tree_Branch_Length_Unit='',
            Media_ID=dsid,
            Contribution_ID=contrib['ID'],
            Source=['dplace-phylogeny-{}'.format(dsdir.name)],
        ))
