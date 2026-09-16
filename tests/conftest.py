import pytest

from tests.helpers.golden import golden_case, load_golden_cases


@pytest.fixture(scope="session")
def golden_cases():
    return load_golden_cases()


@pytest.fixture
def eval_case(golden_cases):
    def _get(case_id: str):
        return golden_case(case_id, golden_cases)

    return _get
