import os
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import FileResponse
from src.skvaider_evaluate_uebungsumgebung.ui_prototype.views import (
    start_evaluation_view,
    get_status_view,
)


def index_view(request):
    here = os.path.dirname(os.path.abspath(__file__))
    return FileResponse(os.path.join(here, "index.html"), request=request)


def create_app():
    here = os.path.dirname(os.path.abspath(__file__))
    with Configurator() as config:
        config.add_route("home", "/")
        config.add_view(index_view, route_name="home")

        config.add_route("start_eval", "/api/evaluate")
        config.add_view(
            start_evaluation_view,
            route_name="start_eval",
            request_method="POST",
            renderer="json",
        )

        config.add_route("eval_status", "/api/status/{eval_id}")
        config.add_view(
            get_status_view,
            route_name="eval_status",
            request_method="GET",
            renderer="json",
        )

        config.add_static_view(name="static", path=here, cache_max_age=0)

        return config.make_wsgi_app()


if __name__ == "__main__":
    app = create_app()
    server = make_server("0.0.0.0", 8080, app)
    print("Pyramid server running on http://0.0.0.0:8080")
    server.serve_forever()
