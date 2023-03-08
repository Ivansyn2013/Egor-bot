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
    result = [x[1] for x in sorted(result, reverse=True)]
    return result if len(result) < 5 else result[:4]


if __name__ == "__main__":
    print(my_fuzzy_search())