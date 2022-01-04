# Pagination in Django

Pagination is the process of breaking large chunks of data up across multiple, discrete web pages. Rather than dumping all the data to the user, you can define the number of individual records you want to be displayed per page and then send back the data that corresponds to the page requested by the user.

The advantage of using this type of technique is that it improves the user experience, especially when there are thousands of records to be retrieved. Implementing pagination in Django is fairly easy as Django provides a [Paginator](https://docs.djangoproject.com/en/4.0/ref/paginator/#paginator-class) class from which we can then use to group content onto different pages.

Pagination can come in different flavors depending on how it is configured by the developer. That said, in this article, we'll look at how to include pagination with function and class-based views using three different UI flavors.

> The example project can be found on the [django-pagination-example](https://github.com/testdrivenio/django-pagination-example) repo on GitHub.

## Objectives

By the end of this article, you will be able to:

1. Explain what pagination is and why you may want to use it.
1. Work with Django's `Paginator` class and `Page` objects.
1. Implement pagination in Django with function and class-based views.

## Django Constructs

When implementing pagination in Django, rather than re-inventing the logic required for pagination, you'll work with the following constructs:

1. [Paginator](https://docs.djangoproject.com/en/4.0/ref/paginator/#paginator-class) - splits a Django QuerySet or list into chunks of `Page` objects.
1. [Page](https://docs.djangoproject.com/en/4.0/ref/paginator/#page-class) - holds the actual paginated data along with pagination metadata.

Let's look at some quick examples.

### Paginator

```python
from django.contrib.auth.models import User


for num in range(43):
    User.objects.create(username=f"{num}")
```

Here, we created 43 User objects.

Next, we'll import the `Paginator` class and create a new instance:

```python
from django.core.paginator import Paginator

users = User.objects.all()

paginator = Paginator(users, 10)

print(paginator.num_pages)  # => 5
```

The `Paginator` class takes four parameters:

1. `object_list` - any object with a `count()` or `__len__()` method, like a list, tuple, or QuerySet
1. `per_page` - maximum number of items to include on a page
1. `orphans` (optional) - used to prevent the last page from having very few items, defaults to `0`
1. `allow_empty_first_page` (optional) - as implied by the name, you can raise an `EmtpyPage` error if you disallow the first page from being empty by setting the argument to `False`, defaults to `True`.

So, in the above example, we sliced the users into pages (or chunks) of ten. The first four pages will have ten users while the last page will have three.

The `Paginator` class has the following [attributes](https://docs.djangoproject.com/en/4.0/ref/paginator/#attributes):

1. `count` - total number of objects
1. `num_pages` - total number of pages
1. `page_range` - range iterator of page numbers

> For consistent paginated results, the QuerySet or the model should be ordered.

If you'd prefer to not have just three users on the final page, you can use the [orphans](https://docs.djangoproject.com/en/4.0/ref/paginator/#django.core.paginator.Paginator.orphans) argument like so to add the final three users to the previous page:

```python
from django.core.paginator import Paginator

users = User.objects.all()

paginator = Paginator(users, 10, orphans=3)

print(paginator.num_pages)  # => 4
```

So, when the number of remaining objects for the last page is less than or equal to the value of `orphans`, those objects will be added to the previous page.

### Page

After the Django QuerySet has been broken up into `Page` objects. We can then use the `page()` method to access the data for each page by passing the page number to it:

```python
from django.core.paginator import Paginator

users = User.objects.all()

paginator = Paginator(users, 10)

page_obj = paginator.page(1)

print(page_obj)  # => <Page 1 of 5>
```

Here, `page_obj` gives us a page object that represents the first page of results. This can then be used in your templates.

> Note that we didn't literally create a `Page` instance. Instead, we obtained the instance from the Paginator class.

What happens if the page doesn't exist?

```python
from django.core.paginator import Paginator

users = User.objects.all()

paginator = Paginator(users, 10)

page_obj = paginator.page(99)
```

You should see:

```sh
    raise EmptyPage(_('That page contains no results'))
django.core.paginator.EmptyPage: That page contains no results
```

Thus, it's a good idea to catch an `EmptyPage` exception like so:

```python
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

users = User.objects.all()

paginator = Paginator(users, 10)

try:
    page_obj = paginator.page(99)
except EmptyPage:
    # Do something
    pass
```

You may want to catch a `PageNotAnInteger` exception as well. For more on this, review the [Exceptions](https://docs.djangoproject.com/en/4.0/ref/paginator/#exceptions) section from the Paginator documentation.

However, instead of catching the `EmptyPage` and `PageNotAnInteger` ourselves using the `try` and `except` keywords. We could use another method that will also create for us a `Page` object. This is the [get_page](https://docs.djangoproject.com/en/4.0/ref/paginator/#django.core.paginator.Paginator.get_page) method.

```python
from django.core.paginator import Paginator

users = User.objects.all()

paginator = Paginator(users, 10)
page_obj = paginator.get_page(99) # new
```

Using this over the `page` method to create a `Page` object save us the time from explicitly catching any exception ourselves. As shown in the example above, even though the number `99` is beyond the range, it will by default return the last page. Also, if the page isn't a valid number it returns by default the first page.

Therefore, both methods can be used it does depend on your preferences. But for the examples shown in this article, we'll be using the `page` method and state out the exceptions explicitly.

The `Page` object has several [attributes](https://docs.djangoproject.com/en/4.0/ref/paginator/#id2) and [methods](https://docs.djangoproject.com/en/4.0/ref/paginator/#id1) that can be used while constructing your template:

1. `number` - shows the page number for a given page
1. `paginator` - displays the associated `Paginator` object
1. `has_next()` - returns `True` if there's a next page
1. `has_previous()` - - returns `True` if there's a previous page
1. `next_page_number()` - returns the number of the next page
1. `previous_page_number()` - returns the number of the previous page

## Function-based Views

Next, let's look at how to work with pagination in function-based views:

```python
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from . models import Employee


def index(request):
    object_list = Employee.objects.all()
    page_num = request.GET.get('page', 1)

    paginator = Paginator(object_list, 6) # 6 employees per page


    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'page_obj': page_obj})
```

Here, we:

1. Defined a `page_num` variable from the URL.
1. Instantiated the `Paginator` class passing it the required parameters, the `employees` QuerySet and the number of employees to be included on each page.
1. Generated a page object called `page_obj`, which contains the paginated employee data along with metadata for navigating to the previous and next pages.

[https://github.com/Samuel-2626/django-pagination/blob/main/employees/views.py#L8](https://github.com/Samuel-2626/django-pagination/blob/main/employees/views.py#L8)

## Class-based Views

Example of implementing pagination in a class-based view:

```py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from . models import Employee


class Index(ListView):
    model = Employee
    context_object_name = 'employees'
    paginate_by = 6
    template_name = 'index.html'
```

[https://github.com/Samuel-2626/django-pagination/blob/main/employees/views.py#L29](https://github.com/Samuel-2626/django-pagination/blob/main/employees/views.py#L29)

## Templates

Working with pagination in the template is where things start to get interesting, as there are several different implementations. In this article, we'll look at three different implementations, each showing a different way in which to navigate to the previous and next pages.

> You can find the code for each example on the [django-pagination-example](https://github.com/testdrivenio/django-pagination-example) repo on GitHub.

### Flavor 1

This is the first flavor implementing the pagination UI.

![Pagination UI - first flavor](https://github.com/Samuel-2626/django-pagination/blob/main/img/1.png)

So, in this example, we have "Previous" and "Next" links that the end-user can click to move from page to page.

*index.html*:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css">
    <title>Pagination in Django</title>
  </head>
  <body>
    <div class="container">
      <h1 class="text-center">List of Employees</h1>
      <hr>

      <ul class="list-group list-group-flush">
        {% for employee in page_obj %}
          <li class="list-group-item">{{ employee }}</li>
        {% endfor %}
      </ul>

      <br><hr>

     {% include "pagination.html" %}
    </div>
  </body>
</html>
```

*pagination.html*:

```html
<div class="paginator">
  <span class="paginator-step-links">
    {% if page_obj.has_previous %}
      <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
    {% endif %}
    <span class="paginator-current-page">
      Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
    </span>
    {% if page_obj.has_next %}
      <a href="?page={{ page_obj.next_page_number }}">Next</a>
    {% endif %}
  </span>
</div>
```

Keep in mind that the *pagination.html* template can be reused across many templates.

### Flavor 2

![Pagination UI - second flavor](https://github.com/Samuel-2626/django-pagination/blob/main/img/2.png)

*pagination.html*:

```html
{% if page_obj.has_previous %}
 <a href="?page={{ page_obj.previous_page_number }}" class="page-link">Previous</a>
  {% else %}
 <a class="page-link disabled">Previous</a>
  {% endif %}

  {% for i in page_obj.paginator.page_range %}
    {% if page_obj.number == i %}
  <a class="page-link active" href="#">{{ i }} </a>
    {% else %}
  <a class="page-link" href="?page={{ i }}">{{ i }}</a>
    {% endif %}
  {% endfor %}

  {% if page_obj.has_next %}
    <a class="page-link" href="?page={{ page_obj.next_page_number }}">Next</a>
  {% else %}
    <a class="page-link disabled">Next</a>
{% endif %}
```

This flavor presents all the page numbers in the UI, making it easier to navigate to different pages.

### Flavor 3

![Pagination UI - third flavor](https://github.com/Samuel-2626/django-pagination/blob/main/img/3.png)

*pagination.html*:

```html
{% if page_obj.has_previous %}
  <a class="btn btn-warning mb-4" href="?page={{ page_obj.previous_page_number }}">« Previous page</a>

  {% if page_obj.number > 3 %}
    <a class="btn btn-outline-warning mb-4" href="?page=1">1</a>
    {% if page_obj.number > 4 %}
      <button class="btn btn-outline-warning mb-4" disabled="">...</button>
    {% endif %}
  {% endif %}
{% endif %}

{% for num in page_obj.paginator.page_range %}
  {% if page_obj.number == num %}
    <a class="btn btn-warning mb-4" href="?page={{ num }}">{{ num }}</a>
  {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
    <a class="btn btn-outline-warning mb-4" href="?page={{ num }}">{{ num }}</a>
  {% endif %}
{% endfor %}

{% if page_obj.has_next %}
  {% if page_obj.number < page_obj.paginator.num_pages|add:'-3' %}
    <button class="btn btn-outline-warning mb-4" disabled="">...</button>
    <a class="btn btn-outline-warning mb-4" href="?page={{ page_obj.paginator.num_pages }}">{{ page_obj.paginator.num_pages }}</a>
  {% elif page_obj.number < page_obj.paginator.num_pages|add:'-2' %}
    <a class="btn btn-outline-warning mb-4" href="?page={{ page_obj.paginator.num_pages }}">{{ page_obj.paginator.num_pages }}</a>
  {% endif %}

  <a class="btn btn-warning mb-4" href="?page={{ page_obj.next_page_number }}">Next Page »</a>
{% endif %}
```

If you have a large number of pages, you may want to look at this third and final flavor.

## Conclusion

This concludes the article about implementing pagination in Django. Here are the key takeaways to remember:

1. Implementing Pagination in Django is quite easy due to the `Paginator` and `Page` helper classes provided out the box.
1. Once the view is created, you simply pass back the page object, with the paginated data, to be used in the view.
