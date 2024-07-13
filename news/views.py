from django.shortcuts import render
from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin






class PostList(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

   # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
     #   context['time_now'] = datetime.utcnow()
      #  context['next_sale'] = "Все свежие новости в эту среду!"
      #  return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context




class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostSearch(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 2


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'
    permission_required = ('news.add_post')


    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/articles/create/':
            post.positions = "AR"
        post.save()
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'
    permission_required = ('news.change_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/articles/edit/':
            post.positions = "AR"
        post.save()
        return super().form_valid(form)




class PostDelete(DeleteView):
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('post_list')


    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/articles/delete/':
            post.positions = "AR"
        post.save()
        return super().form_valid(form)

#from django.views.generic.edit import CreateView

class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )


class ChangePost(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    # а дальше пишите код вашего представления


