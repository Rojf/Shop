from ninja.responses import Response


def authentication_middleware(get_response):
    def middleware(request):
        # Skip authorization for certain paths
        if request.path in ["/api/v1/orders/"] and not request.user.is_authenticated:
                return Response({"message": "Unauthorized"}, status=401)

        return get_response(request)
    return middleware

