from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Value
from .forms import ValueForm
from django.urls import reverse_lazy

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
    success_url = '/values/'  # 追加後にリダイレクトするURL
    
class ValueUpdateView(UpdateView):
    model = Value
    form_class = ValueForm
    template_name = 'values/value_edit.html'
    success_url = reverse_lazy('valuelist')  # 編集成功後にリダイレクトするURL
    def get_success_url(self):
        return reverse_lazy('values:value_list')
    
class ValueDeleteView(DeleteView):
    model = Value
    success_url = reverse_lazy('values:value_list')  # 削除後にリダイレクトするURL
    template_name = 'values/value_confirm_delete.html'
