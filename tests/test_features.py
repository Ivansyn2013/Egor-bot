import pytest
from features.fuzzy_search import my_fuzzy_search


@pytest.mark.asyncio
async def test_my_fuzzy_search_exact_match():
    search_list = ["Apple", "Banana", "Orange"]
    result = await my_fuzzy_search(search_list, "Apple")
    assert result[0] == "Apple"


@pytest.mark.asyncio
async def test_my_fuzzy_search_partial_match():
    search_list = ["Apple Juice", "Banana", "Orange"]
    result = await my_fuzzy_search(search_list, "Apple")
    assert result[0] == "Apple Juice"


@pytest.mark.asyncio
async def test_my_fuzzy_search_empty_list():
    result = await my_fuzzy_search([], "Apple")
    assert result is None


@pytest.mark.asyncio
async def test_my_fuzzy_search_limit():
    search_list = ["Apple1", "Apple2", "Apple3", "Apple4", "Apple5", "Apple6"]
    result = await my_fuzzy_search(search_list, "Apple")
    assert len(result) == 4
