import os
from dotenv import load_dotenv

import pytest


from shennongname.utils.sp2000_china import standardize_species_scientific_name


load_dotenv()
SP2000_API_KEY = os.getenv("SP2000_API_KEY")


@pytest.mark.sp2000_china
@pytest.mark.parametrize(
    "species_name, expected_output",
    [
        (
            "Ephedra ma-huang",
            {
                "matched_a_species": True,
                "matched_species_scientific_name": "Ephedra ma-huang",
                "matched_species_name_code": "T20171000011149",
                "name_status": "synonym",
                "standardized_species_scientific_name": "Ephedra sinica",
                "standardized_species_name_code": "T20171000011148",
            },
        ),
        (
            "Artemisia wadei",
            {
                "matched_a_species": True,
                "matched_species_scientific_name": "Artemisia wadei",
                "matched_species_name_code": "T20171000100825",
                "name_status": "synonym",
                "standardized_species_scientific_name": "Artemisia annua",
                "standardized_species_name_code": "T20171000100824",
            },
        ),
    ],
)
def test_synonym_species_name(species_name, expected_output):
    output = standardize_species_scientific_name(species_name, SP2000_API_KEY)
    assert output == expected_output


@pytest.mark.sp2000_china
@pytest.mark.parametrize(
    "species_name, expected_output",
    [
        (
            "Ephedra sinica",
            {
                "matched_a_species": True,
                "matched_species_scientific_name": "Ephedra sinica",
                "matched_species_name_code": "T20171000011148",
                "name_status": "accepted name",
                "standardized_species_scientific_name": "Ephedra sinica",
                "standardized_species_name_code": "T20171000011148",
            },
        ),
        (
            "Artemisia annua",
            {
                "matched_a_species": True,
                "matched_species_scientific_name": "Artemisia annua",
                "matched_species_name_code": "T20171000100824",
                "name_status": "accepted name",
                "standardized_species_scientific_name": "Artemisia annua",
                "standardized_species_name_code": "T20171000100824",
            },
        ),
    ],
)
def test_accepted_species_name(species_name, expected_output):
    output = standardize_species_scientific_name(species_name, SP2000_API_KEY)
    assert output == expected_output


@pytest.mark.sp2000_china
def test_non_existent_species_name():
    species_name = "Ephedra hhh"

    output = standardize_species_scientific_name(species_name, SP2000_API_KEY)

    expected_output = {"matched_a_species": False}

    assert output == expected_output
