from django.core.paginator import Paginator
from django.utils.safestring import mark_safe


class BetterElidedPaginator(Paginator):
    def __init__(
            self,
            request,
            object_list,
            per_page,
            orphans=0,
            allow_empty_first_page=True,
            current_page_num=None,
            pages_on_each_side=2,
            pages_on_ends=1,
            next_and_prev_buttons=True,
            next_button="&raquo;",
            prev_button="&laquo;",
            display_item_range=False,
            css_classes=None,

    ):
        if css_classes is None:
            css_classes = {
                "tw_base": "rounded py-2 px-4 text-center",
                "tw_enabled_hover": "hover:bg-blue-100 hover:text-gray-900 hover:shadow",
                "tw_enabled_text_color": "text-gray-800",
                "tw_disabled": "bg-transparent text-gray-500 cursor-default focus:shadow-none",
                "tw_active": "text-white bg-blue-600 shadow-xl",
                "outer_div": "",
            }

        self.request = request
        self.items_per_page = per_page
        self.display_item_range = display_item_range
        self.pages_on_each_side = pages_on_each_side
        self.pages_on_ends = pages_on_ends
        self.next_and_prev_buttons = next_and_prev_buttons
        self.current_page_num = current_page_num if current_page_num else int(request.GET.get('page', 1))
        self.css_classes = css_classes
        self.item_count = len(object_list)
        self.next_button = next_button
        self.prev_button = prev_button
        super().__init__(object_list, per_page, orphans, allow_empty_first_page)

    def get_elided_page_range(self, current_page_num=None, pages_on_each_side=None, pages_on_ends=None,
                              items_per_page=None, display_item_range=None):
        """
        Returns a list of page numbers with ellipses (`...`) in between certain sections to indicate omitted pages.

        Parameters:
        - current_page_num (int): the current page number being viewed
        - pages_on_each_side (int): the number of page numbers to show on either side of the current page number
        - pages_on_ends (int): the number of page numbers to show at the beginning and end of the range, before and
          after the ellipses
        """

        def range_string(n, i):
            range_end = f"{min(n * i, self.item_count)}"

            if (n * i) - i + 1 == self.item_count:
                return f"{self.item_count}"
            else:
                return f"{(n * i) - i + 1} - {range_end}"

        if current_page_num is None:
            current_page_num = self.current_page_num

        if pages_on_each_side is None:
            pages_on_each_side = self.pages_on_each_side

        if pages_on_ends is None:
            pages_on_ends = self.pages_on_ends

        if items_per_page is None:
            items_per_page = self.items_per_page

        if display_item_range is None:
            display_item_range = self.display_item_range

        if not all(map(lambda x: isinstance(x, int) and x > 0, [current_page_num, pages_on_each_side, pages_on_ends])):
            raise ValueError("current_page_num, pages_on_each_side and pages_on_ends should be positive integers")
        if current_page_num > self.num_pages:
            raise ValueError("current_page_num should be less than or equal to total number of pages")

        MIDPOINT_AND_ENDS = 3
        current_page_num = self.validate_number(current_page_num)
        node_count = MIDPOINT_AND_ENDS + ((pages_on_each_side + pages_on_ends) * 2)

        if self.num_pages <= node_count:
            if display_item_range:
                for num in self.page_range:
                    yield num, range_string(num, items_per_page)
            else:
                for num in self.page_range:
                    yield num, str(num)
            return

        left_nodes_to_add = \
            max(node_count - current_page_num - pages_on_each_side - pages_on_ends - 1, 0)
        right_nodes_to_add = \
            max(node_count - pages_on_ends - 2 - pages_on_each_side - self.num_pages + current_page_num, 0)

        if current_page_num > (1 + pages_on_each_side + pages_on_ends) + 1:
            if display_item_range:
                for num in range(1, pages_on_ends + 1):
                    yield num, range_string(num, items_per_page)
                yield self.ELLIPSIS, self.ELLIPSIS
                for num in range(current_page_num - pages_on_each_side - right_nodes_to_add, current_page_num + 1):
                    yield num, range_string(num, items_per_page)
            else:
                for num in range(1, pages_on_ends + 1):
                    yield num, str(num)
                yield self.ELLIPSIS, self.ELLIPSIS
                for num in range(current_page_num - pages_on_each_side - right_nodes_to_add, current_page_num + 1):
                    yield num, str(num)
        else:
            if display_item_range:
                for num in range(1, current_page_num + left_nodes_to_add + 1):
                    yield num, range_string(num, items_per_page)
            else:
                for num in range(1, current_page_num + left_nodes_to_add + 1):
                    yield num, str(num)
        if current_page_num < (self.num_pages - pages_on_each_side - pages_on_ends) - 1:
            if display_item_range:
                for num in range(current_page_num + left_nodes_to_add + 1, current_page_num + pages_on_each_side +
                                 left_nodes_to_add + 1):
                    yield num, range_string(num, items_per_page)
                yield self.ELLIPSIS, self.ELLIPSIS
                for num in range(self.num_pages - pages_on_ends + 1, self.num_pages + 1):
                    yield num, range_string(num, items_per_page)
            else:
                for num in range(current_page_num + left_nodes_to_add + 1, current_page_num + pages_on_each_side +
                                 left_nodes_to_add + 1):
                    yield num, str(num)
                yield self.ELLIPSIS, self.ELLIPSIS
                for num in range(self.num_pages - pages_on_ends + 1, self.num_pages + 1):
                    yield num, str(num)
        else:
            if display_item_range:
                for num in range(current_page_num + 1, self.num_pages + 1):
                    yield num, range_string(num, items_per_page)
            else:
                for num in range(current_page_num + 1, self.num_pages + 1):
                    yield num, str(num)

    @property
    def item_list(self):
        """
        Returns the paginated content to display on the page, i.e. returns the items to be displayed on page Y.
        """
        page_num = self.request.GET.get('page', 1)
        return self.get_page(page_num)

    @property
    def html_list(self):
        """
        Generates a string of HTML styled with Tailwind CSS from the list of page nodes generated in
        get_elided_page_range.
        """
        pagination_html = []
        if self.get_page(self.current_page_num).paginator.num_pages > 0:
            page_list = self.get_elided_page_range()
            current_url = remove_page_from_url(self.request.get_full_path())

            pagination_html = tailwind_pagination(
                pagination_list=page_list,
                current_page_num=self.current_page_num,
                page_count=self.num_pages,
                current_url=current_url,
                next_and_prev_buttons=self.next_and_prev_buttons,
                css_classes=self.css_classes,
                next_button=self.next_button,
                prev_button=self.prev_button,
            )

        return pagination_html


def remove_page_from_url(full_path):
    if 'page' not in full_path:
        return full_path
    else:
        return full_path[:full_path.find('page') - 1]


def tailwind_pagination(
        pagination_list=None,
        current_page_num=None,
        page_count=None,
        current_url="",
        next_and_prev_buttons=True,
        next_button="&raquo;",
        prev_button="&laquo;",
        css_classes=None):

    pagination_items = list()
    active_page = int(current_page_num)

    base_class = css_classes["tw_base"]
    hover_color = css_classes["tw_enabled_hover"]
    enabled_class = f"{base_class} {hover_color} {css_classes['tw_enabled_text_color']}"
    disabled_class = f"{base_class} {css_classes['tw_disabled']}"
    active_class = f"{base_class} {css_classes['tw_active']}"

    prev_page = 1 if active_page == 1 else active_page - 1
    next_page = page_count if active_page == page_count else active_page + 1

    prev_disabled = disabled_class if active_page == 1 else enabled_class
    next_disabled = disabled_class if active_page == page_count else enabled_class

    qm_index = current_url.find("?")
    query = "?"

    if qm_index > 0:
        query = query + current_url[qm_index + 1:] + "&"

    ellipses = f"<div class='{css_classes['outer_div']}'><a class='{enabled_class}'" \
               f"href=''>...</a></div>"

    href = "#" if active_page == 1 else f"'{query}page={prev_page}'"

    prev_button = f"<div class='{css_classes['outer_div']}'><a class='{prev_disabled}' " \
                  f"href={href} tabindex='-1' " \
                  f">{prev_button}</a></div>"

    if next_and_prev_buttons:
        pagination_items.append(mark_safe(prev_button))

    for item, item_text in pagination_list:
        if item == Paginator.ELLIPSIS:
            pagination_items.append(mark_safe(ellipses))
        elif item == active_page:
            num_button = f"<div class='{css_classes['outer_div']}'><a class='{active_class}' href='{query}" \
                         f"page={item}'>{item_text}</a></div>"
            pagination_items.append(mark_safe(num_button))
        else:
            num_button = f"<div class='{css_classes['outer_div']}'><a class='{enabled_class}' href='{query}" \
                         f"page={item}'>{item_text}</a></div>"

            pagination_items.append(mark_safe(num_button))

    href = "#" if active_page == page_count else f"'{query}page={next_page}'"
    next_button = f"<div class='{css_classes['outer_div']}'><a class='{next_disabled}' " \
                  f"href={href} tabindex='-1' " \
                  f">{next_button}</a></div>"

    if next_and_prev_buttons:
        pagination_items.append(mark_safe(next_button))

    return pagination_items
