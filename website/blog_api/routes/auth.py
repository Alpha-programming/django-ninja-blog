from ninja import Router # type: ignore
from blog_api.schemas.auth import UserLoginSchema, UserRegistrationSchema, UserSchema
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from ninja.errors import ValidationError # type: ignore

router = Router(
    tags=['Auth']
)

@router.post('/auth/login',response=UserSchema)
def login_user(request, login_data: UserLoginSchema):
    user = authenticate(
        username=login_data.username,
        password=login_data.password
    )
    if user is None:
        raise ValidationError('User not found')
    login(request, user)
    return user

@router.post('/auth/register/', response=UserSchema)
def register_user(request, register_data: UserRegistrationSchema):
    if User.objects.filter(username=register_data.username).exists():
        raise ValidationError('User with this username already registered')

    if '@' not in register_data.email and '.' not in register_data.email:
        raise ValidationError('email is incorrect')

    data = register_data.dict()
    password1 = data.pop('password1')
    password2 = data.pop('password2')
    if password1 != password2:
        raise ValidationError('passwords are not similiar')
    
    user = User.objects.create(**data)
    user.set_password(password1)
    user.save()
    return user

@router.post('/aith/logout/')
def user_logout(request):
    logout(request)
    return {'is_authenticated': request.user.is_authenticated}