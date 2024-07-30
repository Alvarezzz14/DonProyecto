import pytest
from  UsuariosSena.models import  UsuariosSena, UsuariosSenaManager

@pytest.mark.django_db
def test_userCreation():
    user = UsuariosSena.objects.create_user(
            numeroIdentificacion = '123',
            email = 'user@example.com',
            password = '123'
   )
    
    assert user is not None
    assert user.numeroIdentificacion == '123'
    assert user.email == 'user@example.com'
    assert user.check_password('123')
    
@pytest.mark.django_db
def test_createUserWithoutEmail():
    with pytest.raises(ValueError, match='The Email field Must be set'):
        UsuariosSena.objects.create_user(
            numeroIdentificacion = '123',
            password='123', 
            email=None,
        )
