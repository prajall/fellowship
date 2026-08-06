from django.contrib import admin
from django.contrib import messages
from .models import ExpenseModel, ExpenseParticipant


# Inline to show participants within an expense
class ExpenseParticipantInline(admin.TabularInline):
    model = ExpenseParticipant
    extra = 0
    readonly_fields = ('created_at', 'updated_at')


def delete_selected_expenses(modeladmin, request, queryset):
    """Custom delete action for expenses that also removes related participants."""
    count = queryset.count()
    # CASCADE on the FK will auto-delete related ExpenseParticipants
    queryset.delete()
    messages.success(request, f"Successfully deleted {count} expense(s) and their participants.")

delete_selected_expenses.short_description = "Delete selected expenses (with participants)"


# Register your models here.
@admin.register(ExpenseModel)
class ExpenseModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'group_id', 'total_amount', 'created_at', 'updated_at')
    list_filter = ('group_id', 'created_at', 'updated_at')
    search_fields = ('title',)
    inlines = [ExpenseParticipantInline]
    actions = ['delete_selected', delete_selected_expenses]

    def delete_model(self, request, obj):
        """Handle single-object delete from the detail page."""
        messages.success(request, f'Expense "{obj.title}" and its participants have been deleted.')
        obj.delete()

    def delete_queryset(self, request, queryset):
        """Handle bulk delete from the list page."""
        count = queryset.count()
        queryset.delete()
        messages.success(request, f"Successfully deleted {count} expense(s) and their participants.")


def delete_selected_participants(modeladmin, request, queryset):
    """Custom delete action for expense participants."""
    count = queryset.count()
    queryset.delete()
    messages.success(request, f"Successfully deleted {count} participant record(s).")

delete_selected_participants.short_description = "Delete selected participants"


@admin.register(ExpenseParticipant)
class ExpenseParticipantAdmin(admin.ModelAdmin):
    list_display = ('expense_id', 'user_id', 'paid_amount', 'allocated_amount', 'created_at', 'updated_at')
    list_filter = ('expense_id', 'created_at', 'updated_at')
    search_fields = ('expense_id__title', 'user_id__name')
    actions = ['delete_selected', delete_selected_participants]

    def delete_model(self, request, obj):
        """Handle single-object delete from the detail page."""
        messages.success(request, f'Participant "{obj}" has been deleted.')
        obj.delete()

    def delete_queryset(self, request, queryset):
        """Handle bulk delete from the list page."""
        count = queryset.count()
        queryset.delete()
        messages.success(request, f"Successfully deleted {count} participant record(s).")

