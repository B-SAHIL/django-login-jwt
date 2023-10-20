from rest_framework import response
from rest_framework.renderers import JSONRenderer



def alter_response_code(code:int):
    if not response["code"]==401:
                response["code"] = 400

class CustomRenderer(JSONRenderer):
    """
    Gotta modify the response? Change the code here. As simple as that. 
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
       
        response = {
            "status": "success",
            "code": status_code,
            "data": data,
            "message": ""
        }

        if not str(status_code).startswith('2'):
            response["status"] = "error"
            if not response["code"]==401 and not response["code"]==402:
                response["code"] = 400
            response["data"] = {}
            message = ""
            if isinstance(data, str):
                message = message+data
            else:
                for key in data:
                    if isinstance(data[key], str):
                        message = message+key+" : "+data[key]
                    else:
                        if isinstance(data[key][0], list):
                            if data[key][0][0].endswith("field may not be blank."):              
                                message = message+key.replace("_"," ").title()+" field may not be blank."
                            elif data[key][0][0].endswith("field is required."):
                                message = message+key.replace("_"," ").title()+" field is required."
                            else:
                                message = message+data[key][0][0]
                        elif isinstance(data[key][0], str):
                            if data[key][0].endswith("field may not be blank."):              
                                message = message+key.replace("_"," ").title()+" field may not be blank."
                            elif data[key][0].endswith("field is required."):
                                message = message+key.replace("_"," ").title()+" field is required."
                            else:
                                message = message+data[key][0]

                    break
        
            try:
                # response["message"] = data["detail"]
                response["message"] = message
            except KeyError:
                response["data"] = data
        else:
            response["code"] = 200
            if isinstance(response["data"],str):
                response["message"] = response["data"]
                response["data"] = {}
        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)


