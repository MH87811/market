from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('register/', Register, name='Register'),
    path('login/', Login, name='Login'),
    path('login_token/', EmailLoginToken, name='login_token'),
    path('email_login/', EmailLoginVerify, name='email_login'),
    path('logout/', Logout_view, name='Logout'),
    path('profile/<int:id>', profile, name='Profile'),
    path('editprofile/', ProfileUpdate, name='EditProfile'),
    path('displayprofile/<int:id>', DisplayProfile, name='DisplayProfile'),
    path('favorite/', DisplayFave, name='fave'),
    path('requests/', BuyRequests, name='requests'),
    path('done/<int:cart_id>,<int:user_id>', AcceptRequest, name='done'),
    path('change/', ChangePassword, name='ChangePassword'),
    path('verifytoken/', Send_Verify_Code, name='send'),
    path('verify/', Verify, name='verify'),
    # path('send/<user>', send_verification_email, name='send'),
    # path('verify/<uidb64>/<token>/', verify_email, name='verify_email'),
    # path('forgotpassowrd/', ForgotPassowrd, name='forgot'),
]