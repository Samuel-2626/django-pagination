# Pagination in Django

Pagination is the process of breaking large chuncks of data across mulitple, discrete web pages. Rather than dumping all the data to the user especially where there are hundreds of records to be retrieved, you can define the number of data you want to be displayed per page and then send back the data that correspond to the page requested by the user.

Advantages of using this type of technique is that it improves the user experience of the person viewing the website. Implementing pagination in Django is seemlessly easy as it provides us with a `Paginator` class from which we can then use to group our content into different pages.

Pagination can come with different flavour depending on how it is configured by the developer. However, in this article, you'll be learning how to include pagination with function-based view and class-based view using three different UI flavours.

## Objectives

This are the striking goals for this article:

1. Understand what is pagination and why use it.
2. Implementing pagination using function-based view.
3. Implementing pagination using class-based view.
4. Configure the UI template using three pagination flavour.

## Function-based Views

Implementing pagination in a function-based view can be seen below.

```py
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . models import Employee

def index(request):
    object_list = Employee.objects.all()
    paginator = Paginator(object_list, 6) # 6 employees in each page
    page = request.GET.get('page')
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
```

Let me work you through the above code. In order to use pagination with Django, you need to import the Paginator class as well as the model to use. This case we're importing the Employee model.

We instantiated the `Paginator` class passing into it two parameters namely the total amout of data you are retreiving and the finite number of data we want to be distributed per page.

Next, we define a page variable, this is important in order to know the current page and to navigate to previous and next pages if any. This page variable will get its paramter from the URL which makes navigating between pages very easy.

This page parameter is then passed to the paginator class method called `page`, which is responsible for splitting the data across the different pages.

Also, take note of the two exception used to capture errors that could occur. Finally, we are passing the individual data and the page variable to the template.

--- link to the complete code ---

## Class-based Views

Implementing pagination in a class-based view can be seen below.

```py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . models import Employee
from django.views.generic import ListView

class Index(ListView):
    model = Employee
    context_object_name = 'employees'
    paginate_by = 6
    template_name = 'index.html'
```

__How does it work?__

We are basically using the same imports used to implement pagination in a function-based view. However, using a class-based view simplifies the process for us. 

Here, we are using the generic `ListView` Django gives us. The implementation is as follows:

1. State the model you want to use. Django will be create a function to list all the data from this model. Typically the `objects.all()` method. 
2. You can as well change this default implementation by not using a `model` variable but rather a `queryset` varaible where you can then state what you want to retrieve.
3. The `context_object_name` defines the varaible name to be used in the template. Here we are overiding the default name Django gives us which is `object_list`.
4. To sum up we state the number of pages we want to group the data to and the template to be used.

--- link to the complete code ---

## Templates

Implemeting the templates is where things start getting interesting as it can be implemented basically in many different ways. Below, we'll be taking a look at three flavors and they add to it some complexity as we move from one flavor to another.

### Flavor 0

This is the first flavor implemeting the pagination UI.

-- img --

```html
<div class="paginator">
    <span class="paginator-step-links">
        {% if page.has_previous %}
            <a href="?page={{ page.previous_page_number }}">Previous</a>
        {% endif %}
        <span class="paginator-current-page">
            Page {{ page.number }} of {{ page.paginator.num_pages }}.
        </span>
        {% if page.has_next %}
        <a href="?page={{ page.next_page_number }}">Next</a>
        {% endif %}
    </span>
</div>
```

To make our pagination syntax resuable across various template that needs paginated data. You can create a new file `pagination.html` and add the above code. 

This file can then be reused by-and-by in any template you like, this is supposedly following the DRY principle. 

Note that the actual paginated data is called `employees` as shown in the function-based view. Therefore, to reference this data in the template that includes paginated data, we use the following commnand for a function-based view.


```html
{% include "pagination.html" with page=employees %}
```

While for a class-based view it can be referenced like so in any template.

```html
{% include "pagination.html" with page=page_obj %} 
```

This is different in a class-based view as Django by default passes the selected page in a variable called `page_obj`.

--- link to the complete code ---

### Flavor 1

This is the second flavor implemeting the pagination UI. 

--- img --

```html
<ul class="pagination">
    {% if page.has_previous %}
      <li class="page-item"><a href="?page={{ page.previous_page_number }}" class="page-link" style="color: #DDAF94;">Previous</a></li>
    {% else %}
      <li class="page-item disabled"><a class="page-link" href="#" tabindex="-1" aria-disabled="true">Previous</a></li>
    {% endif %}
    {% for i in page.paginator.page_range %}
      {% if page.number == i %}
        <li class="page-item active" aria-current="page"><a class="page-link" href="#" style="color: #DDAF94; background-color: #E8CEBF; border: 1px solid #DDAF94;">{{ i }} </a></li>
      {% else %}
        <li class="page-item"><a class="page-link" href="?page={{ i }}" style="color: #DDAF94;">{{ i }}</a></li>
      {% endif %}
    {% endfor %}
    {% if page.has_next %}
      <li class="page-item"><a class="page-link" href="?page={{ page.next_page_number }}" style="color: #DDAF94;">Next</a></li>
    {% else %}
    <li class="page-item disabled"><a class="page-link" href="#" tabindex="-1" aria-disabled="true">Next</a></li>      
    {% endif %}    
</ul>
```

The first flavor we saw is not quite easy to navigate between pages especially where there are multiple pages. To combat this, we'll be presenting all the pages number in the UI by looping through the total paginated pages. This makes it seemlessly easy to navigate between the pages with just a click of a button.

Also, take note of the how the next and previous button are implemented. To get the previous page, we have to first check if their is a previous page and then call the `previous_page_number` method to load the previous page number. The same works with the next page button.

> Note that this same implementation works the same in all the flavors.

--- link to the complete code ---

### Flavour 2

This is the third and final flavor implemeting the pagination UI for this article. 

-- img --

```html
{% if page.has_previous %}
    <a class="btn btn-warning mb-4" href="?page={{ page.previous_page_number }}">« Previous page</a>
    {% if page.number > 3 %}
        <a class="btn btn-outline-warning mb-4" href="?page=1">1</a>
            {% if page.number > 4 %}
            <button class="btn btn-outline-warning mb-4" disabled="">...</button>
            {% endif %}
    {% endif %}
{% endif %}

{% for num in page.paginator.page_range %}
    {% if page.number == num %}
        <a class="btn btn-warning mb-4" href="?page={{ num }}">{{ num }}</a>
    {% elif num > page.number|add:'-3' and num < page.number|add:'3' %}
        <a class="btn btn-outline-warning mb-4" href="?page={{ num }}">{{ num }}</a>
    {% endif %}
{% endfor %}

{% if page.has_next %}
    {% if page.number < page.paginator.num_pages|add:'-3' %}
        <button class="btn btn-outline-warning mb-4" disabled="">...</button>
        <a class="btn btn-outline-warning mb-4" href="?page={{ page.paginator.num_pages }}">{{ page.paginator.num_pages }}</a>
    {% elif page.number < page.paginator.num_pages|add:'-2' %}
        <a class="btn btn-outline-warning mb-4" href="?page={{ page.paginator.num_pages }}">{{ page.paginator.num_pages }}</a>
    {% endif %}
    <a class="btn btn-warning mb-4" href="?page={{ page.next_page_number }}">Next Page »</a>
{% endif %}
```

The logic of the code above its quite complex and the reason why you might consider this is that using the second flavor can cause the number of pages to basically overflow out of the user screen if the number of pages in the paginated result in itself are numerous. To combat this, we are only allowing the user to see some pages data while some are not shown using this logic `{% elif num > page.number|add:'-3' and num < page.number|add:'3' %}`. Also, the previous and next button are also advanced in some ways to complement this logic.

--- link to the complete code ---

## Testing

To test pagination is quite simply, as all you need to do is to navigate to the URL as shown in the screenshoot and try inputting several pages to see if it gives the desired and expected result. 

--- img --

In addition to this, you can also input a page that is not a number to see how it combats it or even a page that is beyond the scope of the paginated result.

## Conclusion
     
This concludes the article about implementing pagination in Django. Here are the key takeaways to remeber:

1. Implementing Pagination in Django is quite easy due to the helper class it gives us write out the box.
2. We can customize how the Paginated data is viewed in the browser, and you saw three implementation of this.

Happy hacking.