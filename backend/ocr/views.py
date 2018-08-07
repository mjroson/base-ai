from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.http import (
    HttpResponse,
)
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from .models import OCR
from .forms import (
    OCRForm,
)


class OCRListView(ListView):
    # template_name = "ocr/ocr_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = OCR.objects.all()
        query = self.request.GET.get('query', None)
        if query:
            qs = qs.filter(content__icontains=query)

        return qs


class OCRDetailView(DetailView):
    queryset = OCR.objects.all()
    template_name = 'ocr/ocr_detail.html'
    slug_field = 'pk'


class OCRCreateView(CreateView):
    form_class = OCRForm

    template_name = 'ocr/ocr_create.html'
    success_url = '/ocr/'


class OCRUpdateView(UpdateView):
    queryset = OCR.objects.all()
    form_class = OCRForm

    template_name = 'ocr/ocr_update.html'
    success_url = '/ocr/'


class OCRDeleteView(DeleteView):
    queryset = OCR.objects.all()
    # as a DeleteView, the selected object will be sent to the template
    # with variable name {{ object }} or {{ ocr }} (the model name)
    template_name = 'ocr/ocr_delete.html'
    success_url = '/ocr/'
