from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailVerificationCode

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_verified', 'is_staff', 'is_active')
    list_filter = ('is_verified', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_verified',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'is_verified')}),
    )

class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_expired')
    search_fields = ('user__email', 'code')
    readonly_fields = ('created_at',)

    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired?'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EmailVerificationCode, EmailVerificationCodeAdmin)


from django.contrib import admin
from .models import Teacher, TeacherVote

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'vote', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at',)

@admin.register(TeacherVote)
class TeacherVoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'teacher', 'voted_at')
    search_fields = ('voter__username', 'teacher__name')
    list_filter = ('voted_at',)
    # جلوگیری از اضافه کردن رأی‌های تکراری به صورت برنامه‌نویسی (اگر نیاز بود)
    def save_model(self, request, obj, form, change):
        if not change:
            # بررسی وجود رأی مشابه
            if TeacherVote.objects.filter(voter=obj.voter, teacher=obj.teacher).exists():
                from django.core.exceptions import ValidationError
                raise ValidationError("This user has already voted for this teacher.")
        super().save_model(request, obj, form, change)


from .models import TimerSetting

admin.site.register(TimerSetting)