# Changelog

## 1.1.0

### Features

We release a method for automated standardization of species scientific names using SP2000 China.

For example, `Ephedra ma-huang` is a non-standardized species name and is a synonym of `Ephedra sinica`. By using the following code:

```py
from shennongname.utils.sp2000_china import standardize_species_scientific_name

output = standardize_species_scientific_name(
    species_scientific_name="Ephedra ma-huang",
    sp2000_china_api_key="<your_sp2000_china_api_key>",
)

output
```

The `output` will be a Python dictionary:

```py
{
    "matched_a_species": True,  # Indicates that a species name was matched in the SP2000 China database
    "matched_species_scientific_name": "Ephedra ma-huang",  # The matched species name
    "matched_species_name_code": "T20171000011149",  # The ID of the matched species name
    "name_status": "synonym",  # The status of the matched species name, either 'synonym' or 'accepted name'
    "standardized_species_scientific_name": "Ephedra sinica",  # The corresponding standardized species name
    "standardized_species_name_code": "T20171000011148",  # The ID of the standardized species name
}
```

Alternatively, when searching for a species name that is already standardized (e.g., `Ephedra sinica`):

```py
output = standardize_species_scientific_name(
    species_scientific_name="Ephedra sinica",
    sp2000_china_api_key="<your_sp2000_china_api_key>",
)

output
```

The result will be:

```py
{
    "matched_a_species": True,
    "matched_species_scientific_name": "Ephedra sinica",
    "matched_species_name_code": "T20171000011148",
    "name_status": "accepted name",
    # When `name_status` is `"accepted name"`,
    # `standardized_species_scientific_name` equals `matched_species_scientific_name`
    # `standardized_species_name_code` equals `matched_species_name_code`
    "standardized_species_scientific_name": "Ephedra sinica",
    "standardized_species_name_code": "T20171000011148",
}
```

When searching for a species name that does not exist (e.g., `Ephedra hhh`):

```py
output = standardize_species_scientific_name(
    species_scientific_name="Ephedra hhh",
    sp2000_china_api_key="<your_sp2000_china_api_key>",
)

output
```

The result will be:

```py
{
    "matched_a_species": False,
}
```
