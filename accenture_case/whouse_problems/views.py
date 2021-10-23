from rest_framework.views import APIView
from rest_framework.response import Response

from .problem_finder import find_problems


class ProblemFinderView(APIView):

    def get(self, request, *args, **kwargs):
        if "date" in self.request.query_params:
            resp = find_problems(self.request.query_params.get("date"))
        else:
            resp = find_problems()
        return Response(resp)
