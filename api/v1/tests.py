import pytest
from fastapi.testclient import TestClient
from starlette import status

from main import app
from settings import redis_instance

client = TestClient(app)


def test_redis():
    response: bool = redis_instance.ping()
    assert response is True


def test_get_land():
    response = client.get("/land/")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "response, status_code",
    (
            (
                    {
                        "number_of_smiles_to_compare": 5,
                        "similarity": {
                            "C(C(C(=O)O)N)C(=O)N": 1.0,
                            "C([C@@H](C(=O)O)N)C(=O)N": 1.0,
                            "CCN(CC)CCCC(C)NC1=C2C=CC(=CC2=NC=C1)Cl": 0.07357859531772576,
                            "CCC(CC)COC(=O)C(C)NP(=O)(OCC1C(C(C(O1)(C#N)C2=CC=C3N2N=CN=C3N)O)O)OC4=CC=CC=C4": 0.059782608695652176,
                            "CCC(CC)COC(=O)[C@H](C)N[P@](=O)(OC[C@@H]1[C@H]([C@H]([C@](O1)(C#N)C2=CC=C3N2N=CN=C3N)O)O)OC4=CC=CC=C4": 0.059782608695652176,
                        },
                    },
                    status.HTTP_200_OK,
            ),
    ),
)
def test_compare_to_hash(get_payload, response: dict, status_code: int):
    await client.post(
        f"/smiles/add-to-hash?redis_hash",
        json=get_payload,
    )

    get_response = await client.get(
        f"/smiles/compare-to-hash?redis_h"
    )
    assert get_response.status_code == status_code
    assert response == get_response.json()
