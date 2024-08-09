from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseNotFound
from . import util
from .models import Entry
import markdown
import random

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def markdown_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content is None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "error": "Form already exists."
                })
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": markdown_to_html(title)
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "error": "Invalid form."
            })
    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })

def entry_view(request):
    entry = {
        'title': 'Sample Title',
        'content': 'Sample Content',
    }
    return render(request, 'encyclopedia/entry.html', {'entry': entry})

def entry(request, title):
    entry = markdown_to_html(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "error": "Entry not found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": entry
        })

def search(request):
    if request.method == "POST":
        search = request.POST["q"]
        search_content = markdown_to_html(search)
        if search_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": search,
                "content": search_content
            })
        else:
            existing = util.list_entries()
            suggestions = []
            for entry in existing:
                if search.lower() in entry.lower():
                    suggestions.append(entry)
            return render(request, "encyclopedia/search.html", {
                "suggestions": suggestions
            })

def modify(request, title):
    if request.method == "POST":
        content = util.get_entry(title)
        return render(request, "encyclopedia/modify.html", {
            "title": title,
            "content": content
        })
    
def save(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        html_content = markdown_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error": "Invalid form"
        })
    
def aleatory(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    entry = markdown_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": entry
    })