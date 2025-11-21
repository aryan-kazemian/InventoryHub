from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title', 'slug')
    list_display_links = ('indented_title',)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'slug')
    list_filter = ('parent',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'sku', 'price', 'created_by', 'created_at', 'updated_at')
    list_filter = ('category', 'created_by', 'created_at')
    search_fields = ('name', 'sku', 'category__name')
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
