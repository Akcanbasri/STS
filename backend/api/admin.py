from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Teacher, Parent, Administrator, Payment, Installment

class CustomUserAdmin(UserAdmin):
    model = User
    # 'username' yerine 'email' kullanın
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff']

    # 'UserAdmin.fieldsets' ve 'UserAdmin.add_fieldsets' güncellenmeli
    # Bu, Django'nun varsayılan kullanıcı modeli yerine özelleştirilmiş modeli kullanacağınız anlamına gelir.
    # Örneğin, 'username' alanını kaldırıp 'email' alanını ekleyin.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
         ),
    )

# ParentAdmin sınıfınızı veya ilgili yerleri güncelleyin
class ParentAdmin(admin.ModelAdmin):
    # 'students' yerine 'children' kullanın
    filter_horizontal = ['children']

# Diğer model admin kayıtları...
admin.site.register(User, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Administrator)
admin.site.register(Payment)
admin.site.register(Installment)
