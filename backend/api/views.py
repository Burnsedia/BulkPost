# views.py
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import SystemPrompt, Prompt, Post
from .serializers import SystemPromptSerializer, PromptSerializer, PostSerializer
from .services import (
    run_post_generation_and_publish,
    generate_tweet_text,
    build_user_prompt,
    load_openai_key_for,
)


class SystemPromptView(ModelViewSet):
    serializer_class = SystemPromptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            SystemPrompt.objects
            .filter(user=self.request.user)
            .order_by("-updated_at", "-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # enforce ownership on update
        instance = self.get_object()
        if instance.user_id != self.request.user.id:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(user=self.request.user)


class PromptView(ModelViewSet):
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        q = Prompt.objects.filter(user=self.request.user).order_by("-created_at")
        # Optional quick search by ?q=
        term = self.request.query_params.get("q")
        if term:
            q = q.filter(text__icontains=term)
        return q

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user_id != self.request.user.id:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(user=self.request.user)


class PostView(ModelViewSet):  # allows create/schedule + list
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (
            Post.objects
            .filter(user=self.request.user)
            .select_related("system_prompt", "prompt")
            .order_by("-created_at")
        )
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

    # Enforce that foreign keys (system_prompt, prompt) belong to the same user
    def perform_create(self, serializer):
        sp_id = self.request.data.get("system_prompt")
        p_id = self.request.data.get("prompt")

        # Ensure referenced objects exist and belong to the current user
        try:
            sp = SystemPrompt.objects.get(id=sp_id, user=self.request.user)
            pr = Prompt.objects.get(id=p_id, user=self.request.user)
        except (SystemPrompt.DoesNotExist, Prompt.DoesNotExist):
            raise_value = {
                "detail": "system_prompt and prompt must reference your own records."
            }
            return Response(raise_value, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=self.request.user, system_prompt=sp, prompt=pr)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user_id != self.request.user.id:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

        sp_id = self.request.data.get("system_prompt")
        p_id = self.request.data.get("prompt")

        # If client tries to change FKs, ensure ownership
        extra_kwargs = {}
        if sp_id is not None:
            try:
                extra_kwargs["system_prompt"] = SystemPrompt.objects.get(
                    id=sp_id, user=self.request.user
                )
            except SystemPrompt.DoesNotExist:
                return Response(
                    {"detail": "Invalid system_prompt."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if p_id is not None:
            try:
                extra_kwargs["prompt"] = Prompt.objects.get(
                    id=p_id, user=self.request.user
                )
            except Prompt.DoesNotExist:
                return Response(
                    {"detail": "Invalid prompt."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer.save(user=self.request.user, **extra_kwargs)

    @action(detail=True, methods=["post"])
    def run_now(self, request, pk=None):
        post = self.get_object()
        if post.user_id != request.user.id:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

        if post.status not in ("pending", "failed"):
            return Response({"detail": "Post already sent."}, status=status.HTTP_400_BAD_REQUEST)

        post = run_post_generation_and_publish(post)
        return Response(PostSerializer(post).data)

    @action(detail=False, methods=["post"])
    def preview(self, request):
        """
        Generate tweet text from provided inputs WITHOUT saving/posting.
        Body:
          - system_prompt (str, optional; falls back to SYSTEM_FALLBACK)
          - model_name (str, optional; default 'openai:gpt-4o-mini')
          - temperature (float, optional; default 0.7)
          - prompt (str, required)
          - category (str, optional; value/engagement/authority/contrast/transformation)
        """
        system_prompt = request.data.get("system_prompt", "")
        model_name = request.data.get("model_name", "openai:gpt-4o-mini")
        temperature = float(request.data.get("temperature", 0.7))
        base_prompt = (request.data.get("prompt") or "").strip()
        category = request.data.get("category", "") or ""

        if not base_prompt:
            return Response({"detail": "prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_prompt = build_user_prompt(category, base_prompt)
        api_key, base_url, org = load_openai_key_for(request.user)

        text = generate_tweet_text(
            system_prompt=system_prompt,
            model_name=model_name,
            temperature=temperature,
            user_prompt=user_prompt,
            openai_key=api_key,
            base_url=base_url,
            org=org,
        )
        return Response({"tweet": text}, status=status.HTTP_200_OK)






