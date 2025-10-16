from drf_spectacular.utils import OpenApiResponse
from .serializers import ErrorSerializer

DEFAULT_ERROR_RESPONSES = {
    400: OpenApiResponse(ErrorSerializer, description="Bad request"),
    401: OpenApiResponse(ErrorSerializer, description="Not authenticated"),
    403: OpenApiResponse(ErrorSerializer, description="Forbidden"),
    404: OpenApiResponse(ErrorSerializer, description="Not found"),
}
