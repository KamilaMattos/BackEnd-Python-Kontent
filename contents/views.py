from rest_framework.views import APIView, Request, Response, status
from django.forms.models import model_to_dict
from contents.models import Content
from contents.validators import ContentValidation


class ContentView(APIView):
    def get(self, request: Request) -> Response:
        contents = Content.objects.all()
        content_list = [model_to_dict(content) for content in contents]

        return Response(content_list, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        body_validation = ContentValidation(**request.data)

        if not body_validation.is_valid():
            return Response(
                body_validation.errors, status.HTTP_400_BAD_REQUEST
            )

        content = Content.objects.create(**request.data)
        content_dict = model_to_dict(content)

        return Response(content_dict, status.HTTP_201_CREATED)


class ContentDetailView(APIView):
    def get(self, request: Request, content_id: int) -> Response:
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response(
                {"message": "Content not found!"}, status.HTTP_404_NOT_FOUND
            )

        content_dict = model_to_dict(content)

        return Response(content_dict)

    def patch(self, request: Request, content_id: int) -> Response:
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response(
                {"message": "Content not found!"}, status.HTTP_404_NOT_FOUND
            )

        for key, value in request.data.items():
            setattr(content, key, value)

        content.save()
        content_dict = model_to_dict(content)

        return Response(content_dict, status.HTTP_200_OK)

    def delete(self, request: Request, content_id: int) -> Response:
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response(
                {"message": "Content not found!"}, status.HTTP_404_NOT_FOUND
            )

        content.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ContentFilterView(APIView):
    def get(self, request: Request) -> Response:

        title = request.query_params.get("title", None)
        contents = Content.objects.filter(title__icontains=title)
        filtered_contents = [model_to_dict(content) for content in contents]

        return Response(filtered_contents, status.HTTP_200_OK)
