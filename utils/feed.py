from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from users.models import FollowModel, Reaction
from users.serializers import ProfileFullSerializer, ReactSerializer
from utils import time


def follow_user(view_set, request):
    instance = view_set.get_object()
    user = request.user
    try:
        follow = FollowModel.objects.get(user=instance, follower=user)
        follow.delete()
    except:
        FollowModel.objects.create(user=instance, follower=user)
    context = {
        'request': request
    }
    serializer = ProfileFullSerializer(instance, context=context)
    return Response(serializer.data)


def react_user(view_set, request):
    serializer = ReactSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = view_set.get_object()
    try:
        reaction = Reaction.objects.get(type=serializer.reaction_type, user=user, sender=request.user,
                                        created_at__date=time.get_local_dt().date())
        reaction.delete()
    except:
        reactions = Reaction.objects.filter(user=user, sender=request.user,
                                            created_at__date=time.get_local_dt().date())
        reactions.delete()
        Reaction.objects.create(type=serializer.reaction_type, user=user, sender=request.user)
    return Response({
        'id': serializer.reaction_type.id,
        'emoji': serializer.reaction_type.emoji,
        'count': Reaction.objects.filter(user=user, type=serializer.reaction_type,
                                         created_at__date=time.get_local_dt().date()).count(),
        'reacted': Reaction.objects.filter(user=user, type=serializer.reaction_type, sender=request.user,
                                           created_at__date=time.get_local_dt().date()).exists()
    })