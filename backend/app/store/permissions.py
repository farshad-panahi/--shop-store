import pprint
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        """
        Category Creator Has to Be An Staff
        """

        if request.method in SAFE_METHODS:
            return True
        
        pprint.pprint(dir(request.user))
        return bool(
                    request.user 
                    and 
                    request.user.is_staff
                )