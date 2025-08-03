from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util
from . import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new_page(request):
    if (request.method == "POST"):
        return HttpResponseRedirect("/")
    form = forms.PageForm()
    return render(request, "encyclopedia/new-page.html", {"form": form})

def search(request): 
    if(request.method == "POST"):
        all_entries = util.list_entries()
        recommendations = [] 
        search_term = request.POST.get('q')
        
        for entry in all_entries:
            if search_term.lower() in entry.lower():
                recommendations.append(entry)
        return render(request, "encyclopedia/index.html", {
            "entries": recommendations
        })