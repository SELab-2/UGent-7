def admin():
    from authentication.models import User
    a = User.objects.get(username='vvallaey')
    a.is_staff = True
    a.save()
