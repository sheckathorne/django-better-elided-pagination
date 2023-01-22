# Better Elided Pagination

Better Elided Pagination extends the Django Pagination class to provide elided pagination (pagination with ellipses) that does not change lengths when the selected page is near the start or end of the list. The list of pagination nodes will have a predictable and fixed length when the number of nodes exceeds the desired length of the node list.

The following illustrates the difference between Django's built in elided pagination and this project's "better" elided pagination:<br>
![Alt text](/screenshots/comparison.png?raw=true "Title")

Compatible with Django **3.0+**

If using Tailwind CSS, however no CSS framework is required:<br>
Compatible with Tailwind **1.9.6+**

## Installation

### PIP

This will install the latest stable release from PyPi.

```
    pip install django-better-elided-pagination
```


## Usage
The complete example in the next section assumes you are using Tailwind CSS in your project. The html_list property will generate a list of HTML nodes styled using Tailwind CSS classes. If you prefer to style the pagination items yourself, you can simply use:
```
from better_elided_pagination.paginators import BetterElidedPaginator

def some_view(request):
  # the items to be paginated - can be a list or queryset
  items = [str(x) for x in range(1, 41)]

  pagination = BetterElidedPaginator(
      request,
      items,
      3,  # items per page
  )

  elided_list = pagination.get_elided_page_range()
```
.get_elided_page_range() will return a genrator fuction that you can comprehend into a list, or loop over to view the nodes
```
print([p for p in elided_list])
```
The generator function will return a list of tuples with the first element representing the integer page number of the node, and the second element represeting the text label of the node.

The content that is being paginated (i.e. the actual list of items to be displayed) can be viewed by using the .item_list property of the BetterElidedPaginator class:
```
# continued from the example above:
item_list = pagination.item_list
print(item_list)
```


## Example
Import the BetterElidedPaginator to the .py file constructing pagination (views.py) in this example
```
# views.py
from better_elided_pagination.paginators import BetterElidedPaginator
```

Then use the class inside a view fuction:
```
# views.py
def homepage(request):
    # the items to be paginated - can be a list or queryset
    items = [str(x) for x in range(1, 41)]

    pagination = BetterElidedPaginator(
        request,
        items,
        3,  # items per page
    )

    return render(request=request,
              template_name="home.html",
              context={
                  "pagination_items": pagination.html_list,
                  "display_items": pagination.item_list
              })
```

In this example, the pagination is in its own template using Tailwind CSS:
```
# pagination.html
<div class="flex items-center space-x-1 w-full my-2">
    {% for item in pagination_items %}
        {{ item }}
    {% endfor %}
</div>
```
