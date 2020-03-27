from django.urls import path,re_path
from . import views
from . import filter_views, user_view,tutorial_view

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:name>', user_view.user_view, name='user_page'),
    path('problem/', views.title, name='title'),
    path('problem/page/<int:page_id>/',views.page, name='page'),
    path('problem/dif-<str:from_dif>-<str:to_dif>-tag-<str:tags>/page/<int:page_id>/', filter_views.dif_tag_filter, name="dif_tag_filter"),
    path('problem/dif-<str:from_dif>-<str:to_dif>/page/<int:page_id>/',filter_views.dif_filter, name='dif_filter'),
    path('problem/tag-<str:tags>/page/<int:page_id>/', filter_views.tag_filter, name='tag_filter'),
    path('problem/<str:pro_id>/', views.problem_page, name='problem_page'),
    path('tutorial/<str:pro_id>/', tutorial_view.tutorial_view, name='tutorial_page'),
    path('log_in/', views.log_in, name='log_in'),
    path('register/', views.register, name='register'),
    path('logout/', views.log_out, name='log_out'),
    path('log_in/<str:name>', views.log_in),
    path('submit/<int:contest_id>/<int:submit_id>/', views.submit_detail, name='submit_detail'),
    path('news/<int:news_id>/', views.news_page, name='news'),
    path('status/', views.status, name="status"),
]