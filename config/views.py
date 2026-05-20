from django.shortcuts import render


def page_not_found_view(request, exception):
    if 'adminpanel' in request.path:
        return render(request, 'admin_404.html', status=404)
    return render(request, '404.html', status=404)

def server_not_work(request):
    if 'adminpanel' in request.path:
        return render(request, 'admin_500.html', status=500)
    return render(request, '500.html', status=500)