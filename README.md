Better Elided Pagination
=====

Better Elided Pagination extends the Django Pagination class to provide elided pagination (pagination with ellipses) that does not change lengths when the selected page is near the start or end of the list. The list of pagination nodes will have a predictable and fixed length when the number of nodes exceeds the desired length of the node list.

This app can also output the elided pagination list as an HTML string using Tailwind CSS classes.
