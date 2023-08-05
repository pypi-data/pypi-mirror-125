import json
import logging
from appconf.utils import import_attribute
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


TYPOGRAF_CLASS = getattr(
    settings, "WAGTAIL_TYPOGRAF",
    "wagtail_typograf.handlers.Typograf",
)


@csrf_exempt
@staff_member_required
def typograf_api(request, **kwargs):
    if request.method != "POST":
        logger.debug("Typograf bad request")
        return HttpResponse(status=405)

    try:
        data_json = json.loads(request.body)

        # process
        cls = import_attribute(TYPOGRAF_CLASS)
        for block in data_json["blocks"]:
            block["text"] = cls(block["text"]).process()

        response = JsonResponse({
            "success": True,
            "data": data_json,
        })
    except Exception as e:
        response = JsonResponse({
            "success": False,
            "error": e.__str__(),
        })

    logger.debug(
        "Typograf response: %s...",
        response.content[:100],
    )

    return response
