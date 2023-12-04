import collections


def test_valid(cldf_dataset, cldf_sqlite_database, cldf_logger):
    #assert cldf_dataset.validate(log=cldf_logger)

    #
    # Murdock (1967) refers to as Tunava (Nd29) includes both the Deep Springs Valley and
    # Fish Lake Valley Paiute groups, whereas Binford (2001) describes the
    # Fish Lake (B211) and Deep Springs Paiute (B206) as distinct societies. D-PLACE highlights
    # potential links among such societies by assigning them a matched “cross-dataset id” (xd_id).
    #
    assert len(set(soc.data['xd_id'] for soc in [
        cldf_dataset.get_object('LanguageTable', 'Nd29'),
        cldf_dataset.get_object('LanguageTable', 'B211'),
        cldf_dataset.get_object('LanguageTable', 'B206'),
    ])) == 1

    soc2lang = collections.Counter()
    for soc in cldf_dataset.objects('LanguageTable'):
        if soc.data['type'] == 'society':
            llgcs = soc.data['Language_Level_Glottocodes']
            if len(llgcs) == 1:
                if llgcs[0] == soc.cldf.glottocode:
                    soc2lang.update(['language'])
                else:
                    soc2lang.update(['dialect'])
            else:
                soc2lang.update(['subgroup'])
    assert soc2lang['language'] > 100
    assert soc2lang['dialect'] > 0
    assert soc2lang['subgroup'] > 0

    # Make sure we haven't lost any data:
    ndp = {
        row[0]: row[1] for row in
        cldf_sqlite_database.query("""
select p.cldf_contributionReference, count(v.cldf_id)
from valuetable as v, parametertable as p
where p.cldf_id = v.cldf_parameterReference 
group by p.cldf_contributionReference;
""")}
    assert ndp['dplace-dataset-binford'] >= 13957
    assert ndp['dplace-dataset-ccmc'] >= 1007
    assert ndp['dplace-dataset-ea'] >= 121354
    assert ndp['dplace-dataset-ecoclimate'] >= 19880
    assert ndp['dplace-dataset-gmted2010'] >= 3976
    assert ndp['dplace-dataset-sccs'] >= 329449
    assert ndp['dplace-dataset-wnai'] >= 73788
    """
    Make sure we haven't lost any data:


sqlite> select p.cldf_contributionReference, count(v.cldf_id) from valuetable as v, parametertable as p where p.cldf_id = v.cldf_parameterReference and v.cldf_value is null group by p.cldf_contributionReference;
dplace-dataset-binford|3679
dplace-dataset-ea|31123
dplace-dataset-jenkins|309
dplace-dataset-kreft|127
dplace-dataset-modis|74
dplace-dataset-sccs|151473
dplace-dataset-teow|8
dplace-dataset-wnai|2684

"""