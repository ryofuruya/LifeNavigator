from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Value
from .forms import ValueForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

class ValueListView(ListView):
    model = Value
    template_name = 'values/value_list.html'  # 価値観リストのテンプレート
    context_object_name = 'values'

class ValueDetailView(DetailView):
    model = Value
    template_name = 'values/value_detail.html'  # 価値観の詳細テンプレート

class ValueCreateView(CreateView):
    model = Value
    form_class = ValueForm
    template_name = 'values/value_form.html'  # 価値観の追加フォームのテンプレート
    success_url = reverse_lazy('values:value_list')  # 追加後にリダイレクトするURL

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

class ValueUpdateView(UpdateView):
    model = Value
    form_class = ValueForm
    template_name = 'values/value_edit.html'
    success_url = reverse_lazy('values:value_list')  # 編集成功後にリダイレクトするURL

class ValueDeleteView(DeleteView):
    model = Value
    success_url = reverse_lazy('values:value_list')  # 削除後にリダイレクトするURL
    template_name = 'values/value_confirm_delete.html'
