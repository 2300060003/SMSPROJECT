from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.projecthomepage, name='projecthomepage'),
    path('printpagecall/', views.printpagecall, name='printpagecall'),
    path('printpagelogic/', views.printpagelogic, name='printpagelogic'),

    path('exceptionpagecall/',views.exceptionpagecall, name='exceptionpagecall'),
    path('exceptionpagelogic/',views.exceptionpagelogic, name='exceptionpagelogic'),

    path('randompagecall/',views.randompagecall, name='randompagecall'),
    path('randomlogic/',views.randomlogic, name='randomlogic'),

    path('calculatorpagecall/',views.calculatorpagecall, name='calculatorpagecall'),
    path('calculatorlogic/',views.calculatorlogic, name='calculatorlogic'),

    path('add_task/', views.add_task, name='add_task'),
    path('<int:pk>/delete/', views.delete_task, name='delete_task'),

    path('loginpagecall/',views.loginpagecall, name='loginpagecall'),
    path('loginpagelogic/',views.loginpagelogic, name='loginpagelogic'),

    path('registerpagecall/',views.registerpagecall, name='registerpagecall'),
    path('registerlogic/',views.registerlogic, name='registerlogic'),

    ]