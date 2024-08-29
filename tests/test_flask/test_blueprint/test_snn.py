from shennongname.flask.blueprint.snn import (
    blueprint_snn,
)

import json
from flask import Flask
import pytest
        

def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint_snn)
    return app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_blueprint_snn(client):
    # Test 1
    datas = [
            {
                "nmm_type": "plant",
                "species_origins": [["Ephedra sinica", "草麻黄"]],
                "medicinal_parts": [["herbaceous stem", "草质茎"]],
                "special_descriptions": [],
                "processing_methods": [],
            },
            {
                "nmm_type": "processed",
                "species_origins": [["Ephedra sinica", "草麻黄"], "or", ["Ephedra intermedia", "中麻黄"], "or", ["Ephedra equisetina", "木贼麻黄"]],
                "medicinal_parts": [["root", "根"], "and", ["rhizome", "根茎"], "or", ["herbaceous stem", "草质茎"]],
                "special_descriptions": [["fresh", "鲜"], "or", ["dried", "干"]],
                "processing_methods": [["stirfried", "炒制"], "and", ["steamed", "蒸制"]],
            },
        ]

    expected_outputs = [
        {
            'success': True,
            'error_msg': '',
            'nmmsn': {
                'nmmsn': 'Ephedra sinica Herbaceous-stem',
                'nmmsn_zh': {
                    'zh': '草麻黄草质茎',
                    'pinyin': 'cǎo má huáng cǎo zhì jīng',
                },
                'nmmsn_name_element': {
                    'nmm_type': 'plant',
                    'species_origins': [['Ephedra sinica', '草麻黄']],
                    'medicinal_parts': [['herbaceous stem', '草质茎']],
                    'special_descriptions': [],
                    'processing_methods': []
                },
                'nmmsn_seq': [['Ephedra sinica', '草麻黄'], ['Herbaceous-stem', '草质茎'], ['', ''], ['', '']]
            },
            'error_msg_en_zh': {
                'en': '',
                'zh': '',
            }
        },
        {
            'success': True,
            'error_msg': 'Pipe: construct_nmmsn_spe_ori. Status: warning. Reason: Multiple species origins detected.\nPipe: construct_nmmsn_med_par. Status: warning. Reason: Multiple medicinal parts detected.\nPipe: construct_nmmsn_spe_des. Status: warning. Reason: Multiple special descriptions detected.',
            'error_msg_en_zh': {
                'en': 'Multiple species origins detected.\nMultiple medicinal parts detected.\nMultiple special descriptions detected.',
                'zh': '检测到多个物种基源。\n检测到多个药用部位。\n检测到多个特殊描述。',
            },
            'nmmsn': {
                'nmmsn': 'Ephedra equisetina vel intermedia vel sinica Herbaceous-stem or Rhizome and Root Dried or Fresh Stirfried and Steamed',
                'nmmsn_zh': {
                    'zh': '蒸制炒制鲜或干木贼麻黄或中麻黄或草麻黄草质茎或根茎与根',
                    'pinyin': 'zhēng zhì chǎo zhì xiān huò gàn mù zéi má huáng huò zhōng má huáng huò cǎo má huáng cǎo zhì jīng huò gēn jīng yǔ gēn',
                },
                'nmmsn_name_element': {
                    'nmm_type': 'processed',
                    'species_origins': [['Ephedra equisetina', '木贼麻黄'], 'or', ['Ephedra intermedia', '中麻黄'], 'or', ['Ephedra sinica', '草麻黄']],
                    'medicinal_parts': [['herbaceous stem', '草质茎'], 'or', ['rhizome', '根茎'], 'and', ['root', '根']],
                    'special_descriptions': [['dried', '干'], 'or', ['fresh', '鲜']],
                    'processing_methods': [['stirfried', '炒制'], 'and', ['steamed', '蒸制']]
                },
                'nmmsn_seq': [['Ephedra equisetina vel intermedia vel sinica', '木贼麻黄或中麻黄或草麻黄'], ['Herbaceous-stem or Rhizome and Root', '草质茎或根茎与根'], ['Dried or Fresh', '鲜或干'], ['Stirfried and Steamed', '蒸制炒制']]
            }
        }
    ]
    
    for data, expected_output in zip(datas, expected_outputs):
        response = client.post('/api/name', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.get_json() == expected_output
