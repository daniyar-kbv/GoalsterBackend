from rest_framework.response import Response
from rest_framework import status

from main.serializers import GoalAddSerializer

from . import response


def get_type_name(types, number):
    for type in types:
        if type[0] == number:
            return type[1]


def add_goal(request):
    context = {
        'user': request.user,
        'observer': request.data.pop('observer') if request.data.get('observer') else None,
        'request': request
    }
    serializer = GoalAddSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)
