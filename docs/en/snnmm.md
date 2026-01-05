# Systematic Nomenclature for Natural Medicinal Materials (SNNMM)

## Rule 1: Two names, one ID

Each **Natural Medicinal Material (NMM)** is assigned an **NMM Systematic Name (NMMSN)**, an **NMM Generic Name (NMMGN)**, and an **NMM ID**.

## Rule 2: Uniqueness

The **NMMSN**, **NMMGN**, and **NMM ID** generated under SNNMM are all unique.

## Rule 3: ANMM/PNMM distinct naming

SNNMM classifies NMMs into three types: **Raw NMMs (RNMMs)**, **Agricultural NMMs (ANMMs)**, and **Processed NMMs (PNMMs)** (Fig. 1). RNMMs are generally regulated as agricultural products, while PNMMs are generally regulated as drugs.

![Types of NMMs](../images/nmm.svg ':size=50%')

> **Fig. 1: Types of NMMs**  
> Raw NMMs can be processed at the production site into Agricultural NMMs, which are often further processed to yield Processed NMMs. In SNNMM, different types of NMMs (e.g., ANMMs vs. PNMMs) are assigned different and unique systematic names, generic names, and NMM IDs.

## Rule 4: Legitimate characters

To allow people from any country to easily input NMMSN or NMMGN using a standard keyboard, NMMSN and NMMGN may contain **only**: uppercase/lowercase Latin letters `a-zA-Z`, and the hyphen `-`.

## Rule 5: Case-insensitive

In NMMSN or NMMGN, uppercase and lowercase letters may both appear, but **only** for readability. In SNNMM, different NMMs **must not** be distinguished by letter case.

## Rule 6: Upright type

NMMSN or NMMGN should be written in upright type.

## Rule 7: NMMSN rules

### Rule 7.1: Standard Chinese correspondence

To facilitate communication in a Chinese context, for each NMM named with NMMSN, SNNMM also provides a corresponding **standard Chinese systematic name (NMMSN-zh)**.

### Rule 7.2: NMMSN composition

NMMSN consists of the following four naming components (Fig. 2):

1. **I. Species origin**
2. **II. Medicinal part**
3. **III. Special description**
4. **IV. Processing method**

### Rule 7.3: NMMSN syntax parsing

Based on principles of natural language processing and computational linguistics, the syntax parsing structure of NMMSN is shown in Fig. 2.

![Parsing structure of NMMSN](../images/ne.svg ':size=50%')

> **Fig. 2: Parsing structure of NMMSN**  
> A valid NMMSN is a lawful combination of four naming components. At a minimum, an NMMSN includes components I and II. For ANMMs, an NMMSN may include I, II, and III; for PNMMs, it may include I, II, III, and IV. Solid lines indicate required components for that NMM type; dashed lines indicate that component III is optional.

### Rule 7.4: Minimal NMMSN composition

- The NMMSN of an **ANMM** must contain at least components **I and II**.
- The NMMSN of a **PNMM** must contain at least components **I, II, and IV** (Fig. 2).

### Rule 7.5: NMMSN order

- The component order in NMMSN is fixed: **I–II–III–IV**.
- For **NMMSN-zh** (Chinese convention), the order is: **IV–III–I–II**.

### Rule 7.6: Species origin naming rules

#### Rule 7.6.1: Complete taxonomic name

Prioritize the **full Latin taxonomic name** of a species when naming. When a specific species can be identified, do **not** use only the genus name or species epithet.

- ✅ NMMSN: [Solidago decurrens Herb](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0020); NMMSN-zh: 一枝黄花全草 (species origin: *Solidago decurrens*)  
  ❌ Solidago Herb

- ✅ NMMSN: [Panax ginseng Rhizome and Root](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-001l); NMMSN-zh: 人参根茎与根 (species origin: *Panax ginseng*)  
  ❌ Ginseng Rhizome and Root

#### Rule 7.6.2: Standard taxonomic name

When naming NMMSN, prioritize the **current standard taxonomic name**. Standard names should primarily refer to: [Catalogue of Life](https://www.catalogueoflife.org/), [Species 2000 China Node](http://sp2000.org.cn)

**Example:**  
In the *Chinese Pharmacopoeia: 2020 Edition: Volume I* (“ChP”), the NMM “吴茱萸” is recorded as a multi-species NMM (based on *Euodia rutaecarpa* or *Evodia ruticarpa var. officinalis* or *Evodia ruticarpa var. bodinieri*). However, all three scientific names are non-standard; the standardized name for all of them is *Tetradium ruticarpum*. Therefore, “吴茱萸” is still a single-species NMM. Its correct NMMSN is:

NMMSN: [Tetradium ruticarpum Fruit](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-012w); NMMSN-zh: 吴茱萸果实

#### Rule 7.6.3: Multiple species origins

When the same part of multiple species is used as the medicinal part of an NMM and these species are interchangeable (i.e., in an “or” relationship), **all species origins** should be fully listed in the NMMSN. Species names are listed side by side, connected by **“vel”** (Latin for “or”) (in NMMSN-zh, use “或”), and arranged in **alphabetical order**. When the genus name repeats, it can be omitted the second time it appears.

- **Multiple species from the same genus:**  
  In ChP, “麻黄” has 3 species origins: *Ephedra sinica* or *Ephedra intermedia* or *Ephedra equisetina*. Thus, it should be named as:  
  - Ephedra equisetina vel Ephedra intermedia vel Ephedra sinica Stem-herbaceous  
  Since the genus name is identical, it should be further abbreviated as:  
  - NMMSN: [Ephedra equisetina vel intermedia vel sinica Stem-herbaceous](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0006); NMMSN-zh: 木贼麻黄或中麻黄或草麻黄草质茎

- **Multiple species from different genera:**  
  - Cremastra appendiculata vel Pleione bulbocodioides vel Pleione yunnanensis Pseudobulb  
  After abbreviating the genus name for the last species, it becomes:  
  - NMMSN: [Cremastra appendiculata vel Pleione bulbocodioides vel yunnanensis Pseudobulb](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-00ac); NMMSN-zh: 杜鹃兰或独蒜兰或云南独蒜兰假鳞茎

#### Rule 7.6.4: Refinement of species origin

When a more refined species origin can be specified, prioritize using it to refer to the NMM.

- NMMSN: [Ephedra sinica Stem-herbaceous](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0003); NMMSN-zh: 草麻黄草质茎  
- NMMSN: [Ephedra intermedia Stem-herbaceous](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0004); NMMSN-zh: 中麻黄草质茎  
- NMMSN: [Ephedra equisetina Stem-herbaceous](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0005); NMMSN-zh: 木贼麻黄草质茎

#### Rule 7.6.5: Species inclusion

For a multi-species NMM, if the taxonomic levels of its species origins are in a hierarchical (inclusion) relationship, **only the species with the highest hierarchical level** is used for naming.

**Example:**  
ChP records the species origins of “山楂” as *Crataegus pinnatifida* and *Crataegus pinnatifida var. major*. Since *C. pinnatifida* includes its variety *var. major*, the variety should not be included when naming “山楂”.

- ✅ NMMSN: [Crataegus pinnatifida Fruit](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-009x); NMMSN-zh: 山楂果实  
  ❌ Crataegus pinnatifida vel pinnatifida var major Fruit

The NMM with a more refined species origin can be named separately to clarify:

- ✅ NMMSN: [Crataegus pinnatifida var major Fruit](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-009y); NMMSN-zh: 山里红果实

#### Rule 7.6.6: Uncertain specific species information

For NMMs whose specific species information is uncertain, naming may use only the genus name followed by **“unspecified”** (in NMMSN-zh, add “未定种”) to indicate that the species information has not been clarified.

**Example:**  
There are thousands of species under the genus *Taraxacum* (see [Catalogue of Life: Taraxacum](https://www.catalogueoflife.org/data/taxon/7SSF)), any of which could potentially be used as an NMM:

- NMMSN: [Taraxacum unspecified Herb](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-01yf); NMMSN-zh: 蒲公英属未定种全草

#### Rule 7.6.7: Omit non-legitimate characters in taxonomic names

If the taxonomic name of the species origin contains non-legitimate characters, those characters should be omitted.

- ✅ NMMSN: [Ziziphus jujuba var spinosa Seed](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-005x); NMMSN-zh: 酸枣种子  
  ❌ Ziziphus jujuba var. spinosa Seed

### Rule 7.7: Medicinal part naming rules

#### Rule 7.7.1: Syntax

The medicinal part in NMMSN should be named using **singular nouns** or **noun phrases** in English.

- ✅ NMMSN: [Panax ginseng Leaf](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-001s); NMMSN-zh: 人参叶  
  ❌ Panax ginseng Leaves

#### Rule 7.7.2: Capitalization and hyphenation

For readability, the first letter of the medicinal part should be capitalized. If the medicinal part consists of multiple words, connect them using a hyphen `-`.

- NMMSN: [Solidago decurrens Herb](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0020); NMMSN-zh: 一枝黄花全草  
- NMMSN: [Ephedra sinica Stem-herbaceous](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0003); NMMSN-zh: 草麻黄草质茎

#### Rule 7.7.3: Multiple medicinal parts

If an NMM uses multiple different medicinal parts from the same species, connect them with **“and”** (in NMMSN-zh, “与”). If an NMM can use multiple **interchangeable** medicinal parts from the same species, connect them with **“or”** (in NMMSN-zh, “或”). The order of medicinal parts follows alphabetical order.

- NMMSN: [Vincetoxicum pycnostelma Rhizome and Root](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-01mz); NMMSN-zh: 徐长卿根茎与根

#### Rule 7.7.4: Refinement of medicinal part

When a more specific medicinal part can be identified, prioritize using the refined medicinal part. This helps further clarify the medicinal part of the NMM.

**Example:**  
“*Vincetoxicum pycnostelma* Rhizome and Root” can be further refined as:

- NMMSN: [Vincetoxicum pycnostelma Rhizome](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-01mx); NMMSN-zh: 徐长卿根茎  
- NMMSN: [Vincetoxicum pycnostelma Root](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-01my); NMMSN-zh: 徐长卿根

### Rule 7.8: Special description naming rules

#### Rule 7.8.1: Syntax

Some NMMs require specific characteristics or special initial preparation at the production site before they can be used as medicine. For these NMMs, **adjectives**, **adjective phrases**, **nouns**, or **appositives** may be used in component III.

#### Rule 7.8.2: Capitalization and hyphenation

For readability, the first letter of the special description should be capitalized. If it consists of multiple words, connect them using a hyphen `-`.

- NMMSN: [Zingiber officinale Rhizome](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-003g); NMMSN-zh: 姜根茎  
- NMMSN: [Zingiber officinale Rhizome Fresh](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-003m); NMMSN-zh: 鲜姜根茎

- NMMSN: [Curcuma wenyujin Rhizome](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-000t); NMMSN-zh: 温郁金根茎  
- NMMSN: [Curcuma wenyujin Rhizome Freshly-sliced](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0015); NMMSN-zh: 鲜切片温郁金根茎

#### Rule 7.8.3: Genuine regional NMMs (道地药材)

For NMMs that must be sourced from genuine regions, geographical nouns may be used as special descriptions. For genuine regional Chinese NMMs, the standard English name of the provincial capital is generally used; in NMMSN-zh, the abbreviation of the provincial capital plus “产” (“produced in”) is used.

- NMMSN: [Fritillaria thunbergii Bulb Zhejiang](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-024c); NMMSN-zh: 浙产浙贝母鳞茎

### Rule 7.9: Processing method naming rules

#### Rule 7.9.1: Syntax

A **PNMM must include a processing method**. A PNMM is named based on its corresponding ANMM by adding an English adjective, adjective phrase, appositive, or abbreviation describing the processing method in component IV. The corresponding Chinese term for the processing method should end with “制”.

**Example:**

- ANMM: NMMSN: [Artemisia annua Part-aerial](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0001); NMMSN-zh: 黄花蒿地上部  
- PNMM: NMMSN: [Artemisia annua Part-aerial Segmented](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0002); NMMSN-zh: 段制黄花蒿地上部

#### Rule 7.9.2: Capitalization and hyphenation

For readability, the first letter of the processing method should be capitalized. If the processing method consists of multiple words, connect them using a hyphen `-`.

#### Rule 7.9.3: Multiple processing methods

For PNMMs requiring multiple processing methods, connect them with **“and”**, placing the later processing method after the earlier one (in NMMSN-zh, methods end with “制” and do not need logical connectors; the later method is placed before). The order of processing methods reflects processing order and must not be changed arbitrarily.

- ✅ NMMSN: [Ephedra sinica Stem-herbaceous Segmented and Aquafried-honey](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-000b); NMMSN-zh: 蜜炙制段制草麻黄草质茎  
  ❌ Ephedra sinica Stem-herbaceous Aquafried-honey and Segmented

#### Rule 7.9.4: Processing methods for Chinese NMMs

Processing methods for Chinese NMMs follow “0231 General Rules for Processing” in the *Chinese Pharmacopoeia: 2020 Edition: Volume IV*. If a specific subtype can be determined, it should be used; otherwise, the broader category may be used.

- NMMSN: [Crataegus pinnatifida Fruit Cleaned and Stirfried-golden](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-00a1); NMMSN-zh: 炒黄制净制山楂果实  
- NMMSN: [Crataegus pinnatifida Fruit Cleaned and Stirfried-charred](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-00a3); NMMSN-zh: 炒焦制净制山楂果实

#### Rule 7.9.5: Classification of Chinese processing (炮制) methods

There are three main categories of processing methods for Chinese NMMs:

1. **Processing by cleaning (净制)**
2. **Processing by cutting (切制)**
3. **Processing by preparing (备制)**

Chinese NMMs that have undergone cutting are assumed to have been cleaned. Any NMM that requires preparing must first go through cleaning or cutting.

- ✅ NMMSN: [Ephedra sinica Stem-herbaceous Segmented and Aquafried-honey](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-000b); NMMSN-zh: 蜜炙制段制草麻黄草质茎  
  ❌ Ephedra sinica Stem-herbaceous Aquafried-honey

- ✅ NMMSN: [Zingiber officinale Rhizome Cleaned and Stirfried-sand](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-003l); NMMSN-zh: 砂炒制净制姜根茎  
  ❌ Zingiber officinale Rhizome Stirfried-sand

### Rule 7.10: Non-species origin or unclear species origin

If the NMM to be named is of non-species origin, or its species origin is hard to determine, its NMMSN may use an English common name.

- NMMSN: [Talc](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-01xx); NMMSN-zh: 滑石  
- NMMSN: [Talc Pulverized](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-01xz); NMMSN-zh: 粉制滑石

## Rule 8: NMMGN rules

### Rule 8.1: Conciseness

Because NMMSN must specify detailed information (species origin, medicinal part, special description, processing method), it is often lengthy. To facilitate everyday usage and clinical prescription, each NMM is also assigned a corresponding shorter **NMMGN**.

### Rule 8.2: Conventional naming for Chinese NMMGN-zh

For Chinese NMMs, **NMMGN-zh** prefers the commonly used name. If an NMM is from ChP, the Chinese name listed in ChP is generally used as NMMGN-zh. For NMMs refined to a single species to prevent naming conflicts, the prefix “单”/“独” (“single”) may be added to the beginning of some NMMGN-zh.

### Rule 8.3: Pinyin naming priority for Chinese NMMGN

To correspond with NMMGN-zh, NMMGN for Chinese NMMs preferably uses the **pinyin** of NMMGN-zh. Pinyin uses no tone marks or spaces; hyphens connect syllables; the first letter is capitalized; and **“v”** is used instead of **“ü”**.

- NMMSN: [Erycibe obtusifolia Stem](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0022); NMMSN-zh: 丁公藤茎;  
  NMMGN: Dan-ding-gong-teng; NMMGN-zh: 单丁公藤 (to differentiate from “丁工藤”, add prefix “单”)

- NMMSN: [Erycibe obtusifolia vel schmidtii Stem](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0024); NMMSN-zh: 丁公藤或光叶丁公藤茎;  
  NMMGN: Ding-gong-teng; NMMGN-zh: 丁公藤

- NMMSN: [Ligustrum lucidum Fruit](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-00d7); NMMSN-zh: 女贞果实;  
  NMMGN: Nv-zhen-zi; NMMGN-zh: 女贞子

### Rule 8.4: Minimum length of NMMGN-zh

NMMGN-zh must use **two or more** Chinese characters.

- NMMSN: [Prunus mume Fruit](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-008w); NMMSN-zh: 梅果实  
  NMMGN-zh: ✅ 乌梅; ❌ 梅

### Rule 8.5: First-come-first-served

Because NMMGN is short, naming conflicts may arise. In such cases, the first assigned NMMGN has priority; later conflicting NMMGNs must add extra information to distinguish them.

**Example:**  
Suppose the following NMM has already been named:

- NMMSN: [Ephedra sinica Stem-herbaceous](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0003); NMMSN-zh: 草麻黄草质茎;  
  NMMGN: Cao-ma-huang; NMMGN-zh: 草麻黄

In this case, the NMMGN-zh does not mention the medicinal part, because it was assigned first. If we further name the root as medicinal, we must differentiate:

- NMMSN: [Ephedra sinica Root](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-000g); NMMSN-zh: 草麻黄根;  
  NMMGN: Cao-ma-huang-gen; NMMGN-zh: 草麻黄根

## Rule 9: NMM ID rules

Each NMM is assigned a unique **NMM ID**. The encoding format is: `NMM-XXXX`, where `XXXX` is a 4-digit base-36 code (`0-9`, `A-Z`), starting from `0001` and increasing to `ZZZZ`, encoding up to `36^4 − 1 = 1,679,615` kinds of NMMs. NMM ID is case-insensitive, but for readability it is usually written in uppercase.

**Examples:**

- NMM-ID: [NMM-0001](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0001)  
  NMMSN: Artemisia annua Part-aerial  
  NMMSN-zh: 黄花蒿地上部  
  NMMGN: Qing-hao  
  NMMGN-zh: 青蒿
- NMM-ID: [NMM-0002](https://shennongalpha.westlake.edu.cn/en-zh/knowledge/nmm-0002)  
  NMMSN: Artemisia annua Part-aerial Segmented  
  NMMSN-zh: 段制黄花蒿地上部  
  NMMGN: Qing-hao-duan  
  NMMGN-zh: 青蒿段

## Rule 10: Standard referencing rules

### Rule 10.1: First complete appearance

To ensure the NMM name in a scientific text accurately corresponds to the actual NMM, it is recommended that the first occurrence in an independent text (e.g., paper or encyclopedia) uses: `NMMSN (NMM ID, NMMGN)`

In subsequent occurrences, any one of NMMSN, NMMGN, or NMM ID may be used.

**Examples:**

- Artemisia annua Part-aerial (NMM-0001, Qing-hao) is a commonly used Chinese natural medicinal material. Artemisia annua Part-aerial has the effect of treating malaria.
- Artemisia annua Part-aerial (NMM-0001, Qing-hao) is a commonly used Chinese natural medicinal material. Qing-hao has the effect of treating malaria.
- Artemisia annua Part-aerial (NMM-0001, Qing-hao) is a commonly used Chinese natural medicinal material. NMM-0001 has the effect of treating malaria.
- 黄花蒿地上部（NMM-0001，青蒿）是一种常用的中药材。黄花蒿地上部可用于治疗疟疾。
- 黄花蒿地上部（NMM-0001，青蒿）是一种常用的中药材。青蒿可用于治疗疟疾。
- 黄花蒿地上部（NMM-0001，青蒿）是一种常用的中药材。NMM-0001 可用于治疗疟疾。

### Rule 10.2: Appendix complete information

If a study involves a large number of NMMs, presenting all NMMSN, NMMGN, and NMM ID in the main text can make it excessively lengthy. In such cases, only one of NMMSN, NMMGN, or NMM ID may be used in the main text; however, in the appendix, a complete list in the format: `NMM ID – NMMSN – NMMGN`, should be provided.
