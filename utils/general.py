from rest_framework.response import Response
from rest_framework import status

from main.serializers import GoalAddSerializer, GoalListSerializer

from . import response

def add_goal(request):
    context = {
        'user': request.user,
        'observer': request.data.pop('observer') if request.data.get('observer') else None,
        'request': request
    }
    serializer = GoalAddSerializer(data=request.data, context=context)
    if serializer.is_valid():
        goal = serializer.save(user=request.user)
        context = {
            'user': request.user
        }
        output_serializer = GoalListSerializer(goal, context=context)
        return Response(output_serializer.data)
    return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)
