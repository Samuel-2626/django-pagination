from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . models import Employee
from django.views.generic import ListView

# Create your views here.

def index(request):
    object_list = Employee.objects.all()
    paginator = Paginator(object_list, 6) # 35 employees in each page
    page = request.GET.get('page')
    print(page)
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        employees = paginator.page(1)
    except EmptyPage:
        # if the page is out of range deliver the last page
        employees = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'employees': employees,
        'page': page
    })

    """ Using class-based view """

# class Index(ListView):

#     model = Employee
#     context_object_name = 'employees'
#     paginate_by = 15
#     template_name = 'index.html'