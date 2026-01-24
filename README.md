# `shennongname`

[![PyPI version](https://img.shields.io/pypi/v/shennongname.svg)](https://pypi.org/project/shennongname/)

## Documentation

The documentation for `shennongname` is hosted via GitHub Pages:

- [English](https://shennong-program.github.io/shennongname/#/en/)
- [中文](https://shennong-program.github.io/shennongname/#/zh/)

## Systematic Nomenclature for Natural Medicinal Materials Algorithm (SNNMMA)

The following code shows how to use `shennongname` Python package to construct an NMM systematic name (NMMSN).

```py
from shennongname.snnmma.algorithm import construct_nmmsn
from shennongname.snnmma.model import NmmsnNameElement

# Construct a Natural Medicinal Material Scientific Name (NMMSN)
input = NmmsnNameElement.model_validate(
    {
        'nmm_type': 'processed',
        'species_origins': [['Ephedra sinica', '草麻黄'], 'or', ['Ephedra intermedia', '中麻黄'], 'or', ['Ephedra equisetina', '木贼麻黄']],
        'medicinal_parts': [['stem herbaceous', '草质茎']],
        'special_descriptions': [],
        'processing_methods': [['segmented', '段制'], 'and', ['aquafried honey', '蜜炙制']]
    }
)

construct_nmmsn(input).model_dump()
```

The output is a Python dictionary:

```py
{
    'success': True,
    'error_msg': 'Pipe: construct_nmmsn_spe_ori. Status: warning. Reason: Multiple species origins detected.',
    'error_msg_en_zh': {
        'en': 'Multiple species origins detected.',
        'zh': '检测到多个物种基源。'
    },
    'nmmsn': {
        'nmmsn': 'Ephedra equisetina vel intermedia vel sinica Stem-herbaceous Segmented and Aquafried-honey',
        'nmmsn_zh': {
            'zh': '蜜炙制段制木贼麻黄或中麻黄或草麻黄草质茎',
            'pinyin': 'mì zhì zhì duàn zhì mù zéi má huáng huò zhōng má huáng huò cǎo má huáng cǎo zhì jīng'
        },
        'nmmsn_name_element': {
            'nmm_type': 'processed',
            'species_origins': [['Ephedra equisetina', '木贼麻黄'], 'or', ['Ephedra intermedia', '中麻黄'], 'or', ['Ephedra sinica', '草麻黄']],
            'medicinal_parts': [['stem herbaceous', '草质茎']],
            'special_descriptions': [],
            'processing_methods': [['segmented', '段制'], 'and', ['aquafried honey', '蜜炙制']]
        },
        'nmmsn_seq': [['Ephedra equisetina vel intermedia vel sinica', '木贼麻黄或中麻黄或草麻黄'], ['Stem-herbaceous', '草质茎'], ['', ''], ['Segmented and Aquafried-honey', '蜜炙制段制']]
    }
}
```

## Start ShennongName Flask Server

The `shennongname` package also provides a Flask server for constructing NMMSNs.

### 1. Configure the `.env` file

```shell
cp .env.example .env
```

### 2. Install dependencies with `uv`

```shell
uv sync
```

We use `uv` to manage the dependencies. If you want development dependencies (e.g., tests), run:

```shell
uv sync --dev
```

### 3. Run the Flask server

```shell
# Production
uv run gunicorn -b 0.0.0.0:5001 shennongname.flask.run:app

# Development
uv run python shennongname/flask/run.py
```

## Start ShennongName Flask Server with Docker

You can also use Docker to run the Flask server.

```shell
docker build -t shennongname .
docker run -d -p 5001:5001 shennongname
```

## Cite this work

Yang, Z., Yin, Y., Kong, C. et al. ShennongAlpha: an AI-driven sharing and collaboration platform for intelligent curation, acquisition, and translation of natural medicinal material knowledge. Cell Discov 11, 32 (2025). <https://doi.org/10.1038/s41421-025-00776-2>
