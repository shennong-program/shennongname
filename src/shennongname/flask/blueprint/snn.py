
from shennongname.snnmma.algorithm import construct_nmmsn
from shennongname.snnmma.model import NmmsnNameElement, SnnmmaOutputFail

from shennongname.lang.lang import get_translation
_ = get_translation('zh')

from flask import Blueprint, request, jsonify
from flask.views import MethodView

api_snn = '/api/name'
blueprint_snn = Blueprint('snn', __name__) 


class ApiSnn(MethodView):
    def get(self):
        return "ShennongName is working!"
    
    
    def post(self):
        data = request.get_json()
        data_model = NmmsnNameElement.model_validate(data)
        
        try:
            response = construct_nmmsn(data_model).model_dump()
            return jsonify(response), 200

        except Exception as e:
            return jsonify(
                SnnmmaOutputFail.model_validate(
                    {
                        'success': False,
                        'error_msg': str(e),
                        'error_msg_en_zh': {
                            'en': str(e),
                            'zh': str(_(str(e)))
                        }
                    }
                ).model_dump()
            ), 400


blueprint_snn.add_url_rule(api_snn, view_func=ApiSnn.as_view('snn'))
