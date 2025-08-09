from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
import random

from markdown2 import Markdown

from . import util
from . import forms


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def new_page(request):
    form = forms.PageForm()
    if request.method == "POST":
        form = forms.PageForm(request.POST)
        title = form.data.get('title')
        
        if util.search_entry(title) is not None:
            form.add_error('title', '¡La página ya existe!')
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
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            util.save_entry(title, content)
            return HttpResponseRedirect("/")
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
        title = form.data.get('title')
        search_data = util.search_entry(title) 
        if search_data is not None and search_data != title:
            form.add_error('title', f'¡La página con el nombre {title} ya existe!')
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
        
        if form.is_valid():
            util.save_entry(form.cleaned_data["title"], form.cleaned_data["content"])
            return HttpResponseRedirect("/")
        
    entry = util.search_entry(entry)

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
    title = util.search_entry(title)

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
        search_term = request.POST.get("q").strip().lower()
        
        recommendations = []
        for entry in all_entries:
            if entry.lower() == search_term:
                return HttpResponseRedirect(reverse(page, args=[entry]))
            if search_term in entry.lower():
                recommendations.append(entry)
        return render(request, "encyclopedia/index.html", {"entries": recommendations})
    return HttpResponseRedirect("/")


def random_page(request):
    all_entries = util.list_entries()
    entry = random.choice(all_entries)
    
    return HttpResponseRedirect(reverse(page, args=[entry]))
