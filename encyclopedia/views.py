from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util
from . import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def newPage(request):
    if (request.method == "POST"):
        return HttpResponseRedirect("/")
    form = forms.PageForm()
    return render(request, "encyclopedia/new-page.html", {"form": form})

