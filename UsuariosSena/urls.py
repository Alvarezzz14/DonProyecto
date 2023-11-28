from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views

# from django.contrib.auth.views import (
# 	PasswordResetView,
# 	PasswordResetDoneView,
# 	PasswordResetConfirmView,
# 	PasswordResetCompleteView,	
# 	)
# from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
 #logout
    path('logout/', auth_views.LogoutView.as_view(template_name='indexLogin.html'), name='logout'),
    # path('reset_password/', PasswordResetView.as_view(), name='password_reset'),
    # path('reset_password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
    
    