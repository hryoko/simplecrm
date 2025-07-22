# # interviews/views/interview.py
# from django.views.generic import CreateView, UpdateView, ListView, DetailView
# from django.urls import reverse_lazy
# from ..models.interview import Interview
# from ..forms.interview import InterviewForm


# class InterviewListView(ListView):
#     model = Interview
#     template_name = 'interviews/interview_list.html'
#     context_object_name = 'interviews'


# class InterviewDetailView(DetailView):
#     model = Interview
#     template_name = 'interviews/interview_detail.html'
#     context_object_name = 'interview'


# class InterviewCreateView(CreateView):
#     model = Interview
#     form_class = InterviewForm
#     template_name = 'interviews/interview_form.html'
#     success_url = reverse_lazy('interviews:list')


# class InterviewUpdateView(UpdateView):
#     model = Interview
#     form_class = InterviewForm
#     template_name = 'interviews/interview_form.html'
#     success_url = reverse_lazy('interviews:list')
