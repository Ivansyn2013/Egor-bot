from fuzzywuzzy import fuzz
async def my_fuzzy_search(search: list, desired: str):
    '''

    :param search: list of products from db
    :param desired: typing product name
    :return: result sorted list of tuples (score, name of product) or None
    '''
    result = []
    for iteam in search:
        score = fuzz.ratio(iteam.lower(), desired.lower())
        result.append((score, iteam))
    if not result:
        return None
    return sorted(result, reverse=True)