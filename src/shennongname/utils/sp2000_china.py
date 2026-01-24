import requests


def standardize_species_scientific_name(
    species_scientific_name, sp2000_china_api_key, page=1
):
    url = "http://www.sp2000.org.cn/api/v2/getSpeciesByScientificName"

    params = {
        "apiKey": sp2000_china_api_key,
        "scientificName": species_scientific_name,
        "page": page,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("code") == 200 and data["data"]["count"] > 0:
            species_data = data["data"]["species"][0]
            matched_species = {
                "matched_a_species": True,
                "matched_species_scientific_name": species_data["scientific_name"],
                "matched_species_name_code": species_data["name_code"],
                "name_status": species_data["name_status"],
                "standardized_species_scientific_name": species_data[
                    "accepted_name_info"
                ]["scientificName"]
                if species_data["name_status"] == "synonym"
                else species_data["scientific_name"],
                "standardized_species_name_code": species_data["accepted_name_info"][
                    "namecode"
                ]
                if species_data["name_status"] == "synonym"
                else species_data["name_code"],
            }
            return matched_species
        else:
            return {"matched_a_species": False}
    else:
        response.raise_for_status()
