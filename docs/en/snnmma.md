# Systematic Nomenclature for Natural Medicinal Materials Algorithm (SNNMMA)

The input to SNNMMA could be a JSON Object. To elucidate, we illustrate with a common natural medicinal material, Mi-ma-huang (蜜麻黄).

```json
{
    "nmm_type": "processed",
    "species_origins": [["Ephedra sinica", "草麻黄"], "or", ["Ephedra intermedia", "中麻黄"], "or", ["Ephedra equisetina", "木贼麻黄"]],
    "medicinal_parts": [["stem herbaceous", "草质茎"]],
    "special_descriptions": [],
    "processing_methods": [["segmented", "段制"], "and", ["aquafried honey", "蜜炙制"]]
}
```

Within the aforementioned input data structure, users of SNNMMA are required to provide information pertaining to the NMM type along with the associated details for the four kinds of name elements. It is noteworthy that these four types of name elements are collectively stored utilizing a data structure denominated as `NmmNeData`.

The basic structure is as follows, exemplified by `species_origins`:

```json
[
    ["Ephedra sinica", "草麻黄"], 
    "or",
    ["Ephedra intermedia", "中麻黄"], 
    "or", 
    ["Ephedra equisetina", "木贼麻黄"]
]
```

The list encompassed in `NmmNeData` permits the incorporation of multiple name element pairs, each with a data substructure: `["name element in English or Latin", "name element in Chinese"]`, which can be interconnected by the logical operator strings `"or"` or `"and"`.

Subsequently, when `NmmNeData` is conveyed to SNNMMA, the algorithm autonomously executes a series of processes for each name element type of NmmNeData. This includes string data verification, deduplication, sorting, character transformation, and more. Ultimately, the algorithm calculates and derives the NMM Systematic Name (NMMSN) and NMM Systematic Chinese Name (NMMSN-zh), presenting the results as another JSON Object:

```json
{
    "success": true,
    "error_msg": "Pipe: construct_nmmsn_spe_ori. Status: warning. Reason: Multiple species origins detected.", 
    "error_msg_en_zh": {
        "en": "Multiple species origins detected.",
        "zh": "检测到多个物种基源。"
    },
    "nmmsn": {
        "nmmsn": "Ephedra equisetina vel intermedia vel sinica Stem-herbaceous Segmented and Aquafried-honey",
        "nmmsn_zh": {
            "zh": "蜜炙制段制木贼麻黄或中麻黄或草麻黄草质茎",
            "pinyin": "mì zhì zhì duàn zhì mù zéi má huáng huò zhōng má huáng huò cǎo má huáng cǎo zhì jīng"
        },
        "nmmsn_name_element": { 
            "nmm_type": "processed",
            "species_origins": [["Ephedra equisetina", "木贼麻黄"], "or", ["Ephedra intermedia", "中麻黄"], "or", ["Ephedra sinica", "草麻黄"]],
            "medicinal_parts": [["stem herbaceous", "草质茎"]],
            "special_descriptions": [],
            "processing_methods": [["segmented", "段制"], "and", ["aquafried honey", "蜜炙制"]]
        },
        "nmmsn_seq": [["Ephedra equisetina vel intermedia vel sinica", "木贼麻黄或中麻黄或草麻黄"], ["Stem-herbaceous", "草质茎"], ["", ""], ["Segmented and Aquafried-honey", "蜜炙制段制"]] 
    }
}
```

The output of the SNNMMA displays the following characteristics:

Once user data is successfully processed by SNNMMA to construct an NMMSN, the value of `success` will be set to `true`. Moreover, the resultant information post-NMMSN construction by SNNMMA will be stored under the `nmmsn` key.

The specific meanings of each hierarchical key in the SNNMMA output are described as follows:

- `error_msg`: In the SNNMM framework, there exist certain valid yet non-preferred rules. For instance, using multiple species origins for systematic naming of NMM is not recommended. The SNNMMA can automatically detect such anomalies during NMMSN construction. Consequently, there might be instances where the NMMSN is successfully constructed, yet the `error_msg` remains populated, recording any issues encountered during the process. These error messages adhere to a standardized format: `Pipe: xxx. Status: xxx. Reason: xxx.` and are stored within `error_msg`.
- `error_msg_en_zh`: To enhance the user experience for both English and Chinese users, error messages in SNNMMA have been localized. Information pertaining to the `Reason` in `error_msg` is processed and stored in both English and Chinese within `error_msg_en_zh.en` and `error_msg_en_zh.zh` respectively. This ensures that even users with programming or language barriers can clearly understand any issues encountered during NMMSN construction by SNNMMA.
- `nmmsn`: This key houses all information directly related to NMMSN.
- `nmmsn.nmmsn`: Represents the successfully constructed NMM Systematic Name.
- `nmmsn.nmmsn_zh`: `nmmsn.nmmsn_zh.zh` denotes the successfully constructed NMM Systematic Chinese Name, while `nmmsn.nmmsn_zh.pinyin` represents the corresponding pinyin transcription.
- `nmmsn.nmmsn_name_element`: The data structure of this key mirrors the structure of input data. However, the order of elements within the `NmmNeData` data structure might be adjusted or reordered based on the SNNMM rules. For example, the order in `species_origins` might change from `[["Ephedra sinica", "草麻黄"], "or", ["Ephedra intermedia", "中麻黄"], "or", ["Ephedra equisetina", "木贼麻黄"]]` to `[["Ephedra equisetina", "木贼麻黄"], "or", ["Ephedra intermedia", "中麻黄"], "or", ["Ephedra sinica", "草麻黄"]]` due to the alphabetical ordering being `e -> i -> s` among the three species origins.
- `nmmsn.nmmsn_seq`: Given that NMMSN comprises four name elements, this key stores the NMMSN corresponding to each name element. This sequenced NMMSN, within ShennongName, can be utilized to distinctively display each name element in a unique color, enhancing user-friendliness.

If SNNMMA encounters issues during the NMMSN construction process and fails, the output from SNNMMA will be strikingly similar:

```json
{
    "success": false,
    "error_msg": "...", 
    "error_msg_en_zh": {
        "en": "...",
        "zh": "..."
    }
}
```

However, the value of `success` will be set to `false`, and the resulting JSON Object will not include the `nmmsn` key and its corresponding value.
