from accounts.api.viewsets import userviewsets
from rest_framework import routers

router = routers.DefaultRouter()
router.register('accounts', userviewsets, basename = 'acccounts_api')
