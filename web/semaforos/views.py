#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import FormView, TemplateView,ListView, View, UpdateView
from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from semaforos.forms import LoginForm
from django.conf import settings
from braces.views import LoginRequiredMixin
from semaforos.utils import serial_ports

class Login(FormView):
    """
    View que maneja el proceso de login, solicita dos input: Username y password que son comprobados en form_valid
    """
    template_name = 'login.html'
    form_class = LoginForm
    success_url = settings.INIT_URL

    def form_valid(self, form):
        context = self.get_context_data()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect(settings.INIT_URL)
            else:
                context['error'] = "Tu usuario no se encuentra activo"
                return self.render_to_response(context)

        else:
            context['error'] = "El username la contraseña que ingresaste no coinciden."
            return self.render_to_response(context)

class Logout(TemplateView):
    """
    View que maneja el logout de la aplicación, en el metodo dispatch solicita el cierre de sesión y retorna a la url de
    login.
    """
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect(settings.LOGIN_URL)

class Index(LoginRequiredMixin,
            TemplateView):
    """
    View de inicio, se usa un mixin que requiere el estado login del usuario, en caso de no estarlo regresa a la url de
    login.
    """
    login_url = settings.LOGIN_URL
    template_name = 'index.html'

    def get_serial_port_list(self):
        list = serial_ports()
        return list

    def get_context_data(self, **kwargs):
        kwargs['serial_ports'] = self.get_serial_port_list()
        return super(Index, self).get_context_data(**kwargs)