from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
import random

from markdown2 import Markdown

from . import util
from . import forms


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def new_page(request):
    if request.method == "POST":
        form = forms.PageForm(request.POST)
        if form.is_valid():
            util.save_entry(form.cleaned_data["title"], form.cleaned_data["content"])
            return HttpResponseRedirect("/")
    form = forms.PageForm()
    return render(
        request,
        "encyclopedia/form-page.html",
        {
            "form": form,
            "is_editing": False,
            "title_action": "Crear nueva página",
            "action": "crear una nueva página",
        },
    )


def edit_page(request, entry):
    if request.method == "POST":
        form = forms.PageForm(request.POST)
        if form.is_valid():
            util.save_entry(form.cleaned_data["title"], form.cleaned_data["content"])
            return HttpResponseRedirect("/")
    all_entries = util.list_entries()

    for entry_row in all_entries:
        if entry.lower() == entry_row.lower():
            entry = entry_row
            break

    entry_data = util.get_entry(entry)
    if entry_data is None:
        return HttpResponseRedirect("/")

    form = forms.PageForm(initial={"title": entry, "content": entry_data})
    return render(
        request,
        "encyclopedia/form-page.html",
        {
            "form": form,
            "entry": entry,
            "is_editing": True,
            "title_action": "Actualizar página",
            "action": "actualizar una página",
        },
    )


def page(request, title):
    markdowner = Markdown()
    all_entries = util.list_entries()
    for entry_row in all_entries:
        if title.lower() == entry_row.lower():
            title = entry_row
            break

    entry_data = util.get_entry(title)
    if entry_data is None:
        raise Http404()

    result = markdowner.convert(entry_data)
    return render(
        request, "encyclopedia/page.html", {"title": title, "content": result}
    )


def search(request):
    if request.method == "POST":
        all_entries = util.list_entries()
        recommendations = []
        search_term = request.POST.get("q")

        for entry in all_entries:
            if search_term.lower() in entry.lower():
                recommendations.append(entry)
        return render(request, "encyclopedia/index.html", {"entries": recommendations})


def random_page(request):
    all_entries = util.list_entries()

    entry = random.choices(all_entries)

    return HttpResponseRedirect(f"/wiki/{entry[0]}")
