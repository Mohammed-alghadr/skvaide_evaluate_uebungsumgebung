from pyramid.view import view_config
from .logic_service import EvaluationLogicService

logic_service = EvaluationLogicService()


@view_config(route_name="start_eval", request_method="POST", renderer="json")
def start_evaluation_view(request):
    try:
        payload = request.json_body
        prompt_text = payload.get("prompt", "")
        result = logic_service.start_evaluation(prompt_text)
        return result
    except ValueError as err:
        request.response.status = 400
        return {"error": str(err)}
    except Exception:
        request.response.status = 400
        return {"error": "Invalid JSON payload."}


@view_config(route_name="eval_status", request_method="GET", renderer="json")
def get_status_view(request):
    eval_id = request.matchdict.get("eval_id")
    try:
        result = logic_service.get_status(eval_id)
        return result
    except KeyError as err:
        request.response.status = 404
        return {"error": str(err)}
