from django import template

register = template.Library()

def paginatorizer(context, adjacent_pages=5):
    page = context['page_obj']
    num_pages = page.paginator.num_pages
    start_page = max(page.number - adjacent_pages, 2)
    end_page = min(page.number + adjacent_pages + 1, num_pages)
    page_numbers = range(start_page, end_page)
    context['page_numbers'] = page_numbers
    if len(page_numbers) > (adjacent_pages - 1):
        if page_numbers[0] > 2:
            context['show_begin_dots'] = True
        if page_numbers[-1] < num_pages-1:
            context['show_end_dots'] = True
        if len(page_numbers) > 1:
            context['show_end'] = True
    return context

register.inclusion_tag('paginator.html', takes_context=True)(paginatorizer)