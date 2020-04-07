from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic, View


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class UserAccountView(View):
    template_name='account/user_account.html'

    def get(self, request, *args, **kwargs):
        user = self.kwargs.get('user')
        current_user=request.user

        context={
            'current_user':current_user
        }
        return render(self.request, self.template_name, context)
