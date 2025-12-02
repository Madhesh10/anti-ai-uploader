# uploader/admin.py
from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    # keep only names that we know exist + a callable display_created_at
    list_display = ("id", "file", "display_created_at")
    search_fields = ("file",)

    def display_created_at(self, obj):
        """
        Try common timestamp field names; if none exist, fall back to pk.
        This ensures admin loads even if your model's timestamp field is named differently.
        """
        for attr in ("created_at", "uploaded_at", "timestamp", "created", "uploaded"):
            if hasattr(obj, attr):
                return getattr(obj, attr)
        # fallback
        return getattr(obj, "pk", str(obj))

    display_created_at.short_description = "Created at"
