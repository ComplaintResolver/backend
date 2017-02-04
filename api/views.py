from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import authentication, permissions
from rest_framework import status

from root.models import Complaint, Comment, Supervisor
from root.serializers import ComplaintSerializer, CommentSerializer
from .pagination import StandardPagination
from social import twitter

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import Http404


class ComplaintViewSet(ModelViewSet):

    class TempSerializer(serializers.Serializer):
        status = serializers.ChoiceField(choices=['rejected', 'resolved'])

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = StandardPagination
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

    def update(self, request, pk, partial=None):
        try:
            complaint = self.queryset.get(pk=pk)
        except (ObjectDoesNotExist, ValueError):
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.TempSerializer(data=request.data)

        if serializer.is_valid():
            if(complaint.status == 'waiting'):

                complaint.status = serializer.data['status']
                complaint.save()
                status_text = ('Your complaint status has been '
                               'changed to: {}').format(complaint.status)
                last_comment = Comment.objects.order_by('-timestamp').first()
                if(last_comment is None):
                    reply_to_status = complaint.s_id
                else:
                    reply_to_status = last_comment.s_id

                twitter.set_status(text=status_text,
                                   in_reply_to=reply_to_status,
                                   handles_to_tag=[complaint.complainant.account_handle])

            return Response(ComplaintSerializer(complaint).data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(ModelViewSet):

    class TempSerializer(serializers.Serializer):
        text = serializers.CharField()

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        try:
            complaint = get_object_or_404(
                Complaint, pk=self.kwargs['complaint_pk'])
        except ValueError:
            raise Http404
        return complaint.comment_set.all()

    def retrieve(self, request, pk, complaint_pk):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, complaint_pk):
        complaint = Complaint.objects.get(pk=complaint_pk)
        prev_comment = Comment.objects.order_by('-timestamp').first()

        serializer = self.TempSerializer(data=request.data)
        if(serializer.is_valid()):
            text = serializer.data['text']
            s_id = twitter.set_status(text=text,
                                      in_reply_to=prev_comment.s_id,
                                      handles_to_tag=[complaint.complainant.account_handle])

            comment = Comment(text=text,
                              supervisor=request.user,
                              s_id=s_id,
                              complaint=complaint)
            comment.save()

            if prev_comment is not None:
                prev_comment.next_comment = comment
                prev_comment.save()

            s = CommentSerializer(comment)
            return Response(s.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
