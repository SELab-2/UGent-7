from django.db import models
from authentication.models import User


class RoleMixin(models.Model):
    # Whether the role model is active.
    is_active = models.BooleanField(
        default=True
    )

    @classmethod
    def create(cls, user: User, **attributes) -> None:
        """Create a model role for the given user"""
        model: cls = cls.objects.filter(id=user.id).first()

        if model is not None:
            model.activate()

        return cls(user_ptr=user, **attributes).save_base(raw=True)

    def activate(self):
        """Activate the role"""
        self.is_active = True
        self.save()

    def deactivate(self) -> None:
        """Deactivate the role"""
        self.is_active = False
        self.save()

    class Meta:
        abstract = True
