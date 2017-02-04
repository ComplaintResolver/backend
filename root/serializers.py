from rest_framework.serializers import ModelSerializer

from . import models


class SupervisorSerializer(ModelSerializer):

    class Meta:
        model = models.Supervisor
        fields = ('id',
                  'username',
                  'email',
                  'designation',
                  'first_name',
                  'last_name')
        read_only = ('id',)


class ComplaintSerializer(ModelSerializer):

    class Meta:
        model = models.Complaint
        fields = ('id',
                  's_id',
                  'status',
                  'text',
                  'timestamp',
                  'complainant')
        read_only = ('id', 'timestamp', 'complainant')


class ComplainantSerializer(ModelSerializer):

    class Meta:
        model = models.Complainant
        fields = ('id',
                  'account_type',
                  'account_handle')
        read_only = ('id',)


class CommentSerializer(ModelSerializer):

    class Meta:
        model = models.Comment
        fields = ('id',
                  's_id',
                  'text',
                  'timestamp',
                  'complaint',
                  'next_comment')
        read_only = ('id', 'timestamp', 'complaint')
