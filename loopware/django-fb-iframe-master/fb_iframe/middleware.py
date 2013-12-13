from django.http import QueryDict

class FacebookMiddleware():
    """Middleware for Facebook applications."""

    def process_request(self, request):

        # Signed request found in either GET, POST or COOKIES...
        if 'signed_request' in request.REQUEST or 'signed_request' in request.COOKIES:
            
            # If the request method is POST and its body only contains the signed request,
            # chances are it's a request from the Facebook platform and we'll override
            # the request method to HTTP GET to rectify their misinterpretation
            # of the HTTP standard.
            #
            # References:
            # "POST for Canvas" migration at http://developers.facebook.com/docs/canvas/post/
            # "Incorrect use of the HTTP protocol" discussion at http://forum.developers.facebook.net/viewtopic.php?id=93554
            if request.method == 'POST' and 'signed_request' in request.POST:
                request.POST = QueryDict('')
                request.method = 'GET'


    def process_response(self, request, response):
        """
        Set compact P3P policies and save signed request to cookie.

        P3P is a WC3 standard (see http://www.w3.org/TR/P3P/), and although largely ignored by most
        browsers it is considered by IE before accepting third-party cookies (ie. cookies set by
        documents in iframes). If they are not set correctly, IE will not set these cookies.
        """
        if 'signed_request' in request.REQUEST:
            response.set_cookie('signed_request', request.REQUEST['signed_request'])
        response['P3P'] = 'CP="IDC CURa ADMa OUR IND PHY ONL COM STA"'
        return response