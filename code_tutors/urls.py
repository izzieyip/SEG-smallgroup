
"""
URL configuration for code_tutors project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from tutorials import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student_dashboard/', views.dashboard, name='student_dashboard'),
    path('tutor_dashboard/', views.dashboard, name='tutor_dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('view_bookings/', views.ViewBookingsView.as_view(), name='view_bookings'),
    path('delete-booking/<int:id>/', views.ViewBookingsView.delete_booking, name='delete_booking'),
    path('my_bookings/', views.ViewMyBookings.as_view(), name='my_bookings'),
    path('create_booking/', views.createBooking, name='create_booking'),
    path('view_requests/', views.display_all_booking_requests, name='view_requests'),
    path('create_new_admin/', views.CreateNewAdminView.as_view() , name='create_new_admin'),
    path('update_booking/<int:booking_id>', views.updateBooking, name='update_booking'),
    path('view_users/', views.display_all_users, name='view_users'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('update_user/<int:user_id>/', views.update_user, name = 'update_user'),
    path('create_booking_request/', views.creatingBookingRequest, name='create_booking_request'),
    path('invoices/', views.ViewInvoicesView.as_view(), name='invoices'),
    path('pay_invoice/<int:id>/', views.ViewInvoicesView.mark_as_paid, name='pay_invoice'),
    path('my_payments/', views.ViewMyPayments.as_view(), name='my_payments'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
