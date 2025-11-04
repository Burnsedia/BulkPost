from django.contrib import admin
from django import forms
from django.utils.html import format_html

from .models import SystemPrompt, Prompt, Post, ProviderCredential

# ---------- Masked input widgets for secrets
class SecretInput(forms.PasswordInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("render_value", True)
        super().__init__(*args, **kwargs)

# ---------- ProviderCredential admin (mask secrets, write-only feel)
class ProviderCredentialForm(forms.ModelForm):
    class Meta:
        model = ProviderCredential
        fields = "__all__"
        widgets = {
            "api_key": SecretInput(),
            "api_secret": SecretInput(),
            "access_token": SecretInput(),
            "access_token_secret": SecretInput(),
            "openai_api_key": SecretInput(),
        }

class ProviderCredentialAdmin(admin.ModelAdmin):
    form = ProviderCredentialForm
    list_display = ("user", "platform", "masked_openai_key", "has_twitter_creds")
    list_filter = ("platform",)
    search_fields = ("user__username", "user__email")

    @admin.display(description="OpenAI key")
    def masked_openai_key(self, obj):
        v = obj.openai_api_key or ""
        return ("••••" + v[-4:]) if v else "—"

    @admin.display(description="Twitter creds")
    def has_twitter_creds(self, obj):
        ok = all([
            obj.api_key, obj.api_secret, obj.access_token, obj.access_token_secret
        ])
        color = "#16a34a" if ok else "#ef4444"
        text  = "OK" if ok else "Missing"
        return format_html('<b style="color:{}">{}</b>', color, text)

admin.site.register(ProviderCredential, ProviderCredentialAdmin)

# ---------- SystemPrompt admin
class SystemPromptAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "model_name", "temperature", "updated_at")
    list_filter = ("model_name",)
    search_fields = ("user__username", "user__email", "name")
    readonly_fields = ("created_at", "updated_at")

admin.site.register(SystemPrompt, SystemPromptAdmin)

# ---------- Prompt admin
class PromptAdmin(admin.ModelAdmin):
    list_display = ("user", "short_text", "category", "created_at")
    list_filter = ("category",)
    search_fields = ("user__username", "user__email", "text")

    @admin.display(description="text")
    def short_text(self, obj):
        return (obj.text or "")[:80]

admin.site.register(Prompt, PromptAdmin)

# ---------- Post admin with a quick action to run now (optional)
from .services import run_post_generation_and_publish

@admin.action(description="Generate + Post now")
def action_run_now(modeladmin, request, queryset):
    for post in queryset:
        if post.status in ("pending", "failed"):
            run_post_generation_and_publish(post)

class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "prompt", "status", "scheduled_for", "posted_at", "twitter_id")
    list_filter = ("status",)
    search_fields = ("user__username", "user__email", "prompt__text", "twitter_id")
    actions = [action_run_now]
    readonly_fields = ("text", "twitter_id", "posted_at", "created_at", "error")

admin.site.register(Post, PostAdmin)

