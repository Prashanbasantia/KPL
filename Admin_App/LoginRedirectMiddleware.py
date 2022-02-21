from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render

class LoginRedirectMiddleware(MiddlewareMixin):
    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__       
        user=request.user
        if user.is_authenticated:
            if user.is_superuser:
                if modulename == "Admin_App.views" or modulename == "django.views.static" or  modulename == "Index_App.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("dashboard"))
            else:
                return HttpResponseRedirect(reverse("login"))

        else:
            if modulename == "Index_App.views" or modulename == "django.views.static" or  modulename == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("login"))


        