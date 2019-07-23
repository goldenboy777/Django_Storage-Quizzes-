"""quizzes URL Configuration
  
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from django.urls import path,include
from board import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('',views.home,name='home'),
    path('boards/<int:pk>/',views.board_documents,name='board_documents'),
	#path('accounts/', include('django.contrib.auth.urls')),
    path('boards/<int:pk1>/<int:pk2>',views.subjects,name='subjects'),
    path('signup/',accounts_views.SignUpView.as_view(), name='signup'),
    path('signup/student/', accounts_views.StudentSignUpView.as_view(), name='student_signup'),
    path('signup/teacher/', accounts_views.ModeratorSignUpView.as_view(), name='moderator_signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('boards/<int:pk>/newsubject',views.new_subject,name='new_subject'),
    path('boards/<int:pk1>/<int:pk2>/new',views.new_document,name='new_document'),
    path('boards/<int:pk1>/<int:pk2>/review',views.review, name='review'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)