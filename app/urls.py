from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangedForm, MyPasswordResetForm, MySetPasswordForm
### for image ###
from django.conf import settings
from django.conf.urls.static import static
#################

urlpatterns = [
    path('', views.home, name='home'),
    path('product-detail/<int:pk>/', views.product_detail, name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart', views.plus_cart, name='pluscart'),
    path('minuscart', views.minus_cart, name='minuscart'),
    path('removecart', views.remove_cart, name='removecart'),

    path('orders/', views.orders, name='orders'),
    path('buy/', views.buy_now, name='buy-now'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),

    path('mobile/', views.mobile, name='mobile'),
    path('mobiledata/<slug:data>/', views.mobile, name='mobiledata'),

    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomweardata/<slug:data>/', views.bottomwear, name='bottomweardata'),

    path('topwear/', views.topwear, name='topwear'),
    path('topweardata/<slug:data>/', views.topwear, name='topweardata'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangedForm, success_url='/passwordchangedone/'), name='changepassword'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password-reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    path('registration/', views.customerregistration, name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('orderdone/', views.orderdone, name='orderdone'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
