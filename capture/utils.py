"""Useful stuff that has no proper home
"""
import pandas as pd
import re

from capture.devconfig import REAGENT_ALIAS


def get_explicit_experiments(rxnvarfile, only_volumes=True):
    """Extract reagent volumes for the manually specified experiments, if there are any.

    :param rxnvarfile: the Template
    :param only_volumes: only return the experiment Reagent volumes
    :return:
    """
    explicit_experiments = pd.read_excel(io=rxnvarfile, sheet_name='ManualExps')
    # remove empty rows:
    explicit_experiments = explicit_experiments[~explicit_experiments['Manual Well Number'].isna()]
    # remove unused reagents:
    explicit_experiments = explicit_experiments.ix[:, explicit_experiments.sum() != 0]

    if only_volumes:
        explicit_experiments = explicit_experiments.filter(regex='{}\d \(ul\)'.format(REAGENT_ALIAS)).astype(int)

    return explicit_experiments


def get_reagent_number_as_string(reagent_str):
    """Get the number from a string representation"""
    reagent_pat = re.compile('{}(\d+)'.format(REAGENT_ALIAS))
    return reagent_pat.match(reagent_str).group(1)


def abstract_reagent_colnames(df, inplace=True):
    """Replace instances of 'Reagent' with devconfig.REAGENT_ALIAS

    :param df: dataframe to rename
    :return: None or pandas.DataFrame (depending on inplace)
    """
    result = df.rename(columns=lambda x: re.sub('[Rr]eagent', REAGENT_ALIAS, x), inplace=inplace)
    return result


def flatten(L):
    """Flatten a list recursively

    Inspired byt his fun discussion: https://stackoverflow.com/questions/12472338/flattening-a-list-recursively

    np.array.flatten did not work for irregular arrays, and itertools.chain.from_iterable cannot handle arbitrary

    :param L: A list to flatten
    :return: the flattened list
    """
    if L == []:
        return L
    if isinstance(L[0], list):
        return flatten(L[0]) + flatten(L[1:])
    return L[:1] + flatten(L[1:])


