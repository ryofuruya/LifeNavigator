from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Value
from .forms import ValueForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import  Http404

class ValueListView(LoginRequiredMixin, ListView):
    model = Value
    template_name = 'values/value_list.html'
    context_object_name = 'values'

    def get_queryset(self):
        return Value.objects.filter(user=self.request.user)

class ValueDetailView(LoginRequiredMixin, DetailView):
    model = Value
    template_name = 'values/value_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404
        return obj

class ValueCreateView(LoginRequiredMixin, CreateView):
    model = Value
    form_class = ValueForm
    template_name = 'values/value_form.html'
    success_url = reverse_lazy('values:value_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

class ValueUpdateView(LoginRequiredMixin, UpdateView):
    model = Value
    form_class = ValueForm
    template_name = 'values/value_edit.html'
    success_url = reverse_lazy('values:value_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404
        return obj

class ValueDeleteView(LoginRequiredMixin, DeleteView):
    model = Value
    success_url = reverse_lazy('values:value_list')
    template_name = 'values/value_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404
        return obj
