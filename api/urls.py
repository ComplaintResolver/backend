from django.conf.urls import url, include

from rest_framework_nested import routers


from .views import ComplaintViewSet, CommentViewSet

router = routers.SimpleRouter()
router.register(r'complaints', ComplaintViewSet)

comments_router = routers.NestedSimpleRouter(router,
                                             r'complaints',
                                             lookup='complaint')
comments_router.register(r'comments',
                         CommentViewSet,
                         base_name='complaint-comment')

urlpatterns = [
    url(r'^auth/', include('rest_auth.urls')),
]

urlpatterns += router.urls + comments_router.urls
