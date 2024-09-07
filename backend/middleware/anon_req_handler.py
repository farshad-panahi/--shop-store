import uuid
import logging

logger = logging.getLogger(__name__)


class StrangerRequestHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid.uuid4())
        response = self.get_response(request)
        response["X-Request-ID"] = request.request_id

        logging.basicConfig(
            format=f"[Request ID: {request.request_id}] %(levelname)s: %(message)s",
            level=logging.INFO,
        )

        return response
