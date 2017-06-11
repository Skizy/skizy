from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from students.models import Student
from students.forms import StudentModelForm


class StudentListView(ListView):
    model = Student

    def get_queryset(self):
        qs = super().get_queryset()
        course_id = self.request.GET.get('course_id')
        if course_id:
            qs = Student.objects.filter(courses=course_id)
        return qs


class StudentDetailView(DetailView):
    model = Student


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentModelForm
    success_url = reverse_lazy('students:list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Student registration'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Student %s has been successfully added.' % form.instance.full_name())
        return super().form_valid(form)


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentModelForm
    # success_url = reverse_lazy('students:list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Student info update'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Info on the student has been successfully changed.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('students:edit', kwargs={'pk': self.kwargs.get('pk')})


class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('students:list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Student info suppression'
        return context

    def delete(self, request, *args, **kwargs):
        response = super().delete(self, request, *args, **kwargs)
        messages.success(request, ("Info on %s has been successfully deleted." % self.object.full_name()))
        return response
