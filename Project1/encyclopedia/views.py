from django.shortcuts import render, redirect
import markdown2
from django import forms
from django.http import HttpResponseNotFound
from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Markdown Content")


def edit_page(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return HttpResponseNotFound("<h1>Page Not Found</h1>")

    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            util.save_entry(title, form.cleaned_data['content'])
            return redirect('entry_page', title=title)

    else:  # GET request
        form = NewPageForm(initial={'title': title, 'content': entry_content})  

    return render(request, 'encyclopedia/edit_page.html', {
        'form': form,
        'title': title
    })


def create_new_page(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "message": "An encyclopedia entry with that title already exists."
                })

            util.save_entry(title, content)
            return redirect('entry_page', title=title)
    else:
        form = NewPageForm()
    return render(request, 'encyclopedia/create_page.html', {'form': form})


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    entry = util.get_entry(title) 
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Encyclopedia entry not found."
        })
    else:
        content = markdown2.markdown(entry)  # Convert to HTML
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content})


def search_results(request):
    query = request.GET.get('q')  # Get the 'q' query parameter
    print("Query: ", query)
    entries = util.list_entries()  
    print("Entries: ",entries)
    perfect_match = [entry for entry in entries if query.lower() == entry.lower()] # Exact match
    print("Perfect match: ", perfect_match)
    matches = [entry for entry in entries if query.lower() in entry.lower()]
    print("Matches: ",matches)

    if len(perfect_match) == 1:
        return redirect('entry_page', perfect_match[0])  # Direct match, use redirect
    else:
        return render(request, "encyclopedia/search_results.html", {
            "matches": matches, 
            "query": query
        })
    

