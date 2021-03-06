from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.
from saasapp.drf import insert_permission_field
from saasapp.model_viewset import CustomModelViewSet
from saasapp.sops_task.handlers import (
    TaskHandler,
    BizHandler,
    TemplateHandler,
    PermissionHandler,
)

from saasapp.sops_task.models import Tasks
from saasapp.sops_task.serializers import TaskSerializer


class TaskViewSet(CustomModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

    @insert_permission_field(
        id_field=lambda d: d["id"],
        data_field=lambda d: d["info"],
        actions=[],
        resource_meta=None,
    )
    def list(self, request, *args, **kwargs):
        return TaskHandler().list(request=request, view=self)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        params = dict(serializer.data)
        return Response(TaskHandler().create(request=request, **params))

    def retrieve(self, request, pk=None, *args, **kwargs):
        return Response(TaskHandler().retrieve(id=pk))

    @action(methods=["GET"], detail=False)
    def sync(self, request, *args, **kwargs):
        return Response(TaskHandler().sync(request=request))


class BizViewSet(CustomModelViewSet):
    def list(self, request, *args, **kwargs):
        return Response(BizHandler().list(request=request))


class TemplateViewSet(CustomModelViewSet):
    def list(self, request, *args, **kwargs):
        bk_biz_id = request.GET.get("bk_biz_id")
        return Response(TemplateHandler().list(request=request, bk_biz_id=bk_biz_id))

    @action(methods=["GET"], detail=True)
    def params(
        self,
        request,
        pk,
        *args,
        **kwargs,
    ):
        return Response(TemplateHandler().params(request=request, template_id=pk))


class PermissionViewSet(CustomModelViewSet):
    @action(methods=["GET"], detail=False)
    def has_permission(
        self,
        request,
        *args,
        **kwargs,
    ):
        action_id = request.GET.get("action_id")
        resource_type = request.GET.get("resource_type")
        resource_id = request.GET.get("resource_type")
        has_permission = PermissionHandler(
            action_id=action_id,
            resource_type=resource_type,
            resource_id=resource_id,
        ).has_permission(request=request)
        return Response({"action_id": action_id, "is_allowed": has_permission})

    @action(methods=["GET"], detail=False)
    def get_apply_url(
        self,
        request,
        *args,
        **kwargs,
    ):
        action_id = request.GET.get("action_id")
        resource_type = request.GET.get("resource_type")
        resource_id = request.GET.get("resource_type")
        apply_url = PermissionHandler(
            action_id=action_id,
            resource_type=resource_type,
            resource_id=resource_id,
        ).get_apply_url(request=request)
        return Response({"apply_url": apply_url})
