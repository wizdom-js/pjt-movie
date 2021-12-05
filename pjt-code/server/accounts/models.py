from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
import os

def user_directory_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.pk, filename)  # user를 upload_user로 저장했기 때문에 instance.upload_user로 사용함
def user_path(instance):
    return 'users/{0}'.format(instance.pk)


class User(AbstractUser):
    nickname = models.CharField(max_length=10, unique=True)
    profile_image = models.ImageField(null=True, upload_to=user_directory_path)
    first_name = None
    last_name = None
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    
    def delete(self, *args, **kargs):   # DB 를 삭제하면 저장한 이미지도 삭제되도록 하기 위해
        if self.profile_image:
            img_path = f'{settings.MEDIA_ROOT}/{user_path}'
            os.remove(os.path.join(img_path, self.profile_image.path))
        super(User, self).delete(*args, **kargs)

    def __str__(self):
        return self.username

class Feedback(models.Model):
    user = models.TextField()
    reason = models.TextField()     # 드롭다운
    feedback = models.TextField(null=True)   # 선택사항, 디테일한이유

    def __str__(self):
        return self.reason

