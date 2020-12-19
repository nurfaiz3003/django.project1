from django.shortcuts import render, redirect
from django import forms
from . import util
import markdown2, random

class NewPagesForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Render Page from Markdown Entries
def openpage(request, title):
    #Get the entry based on the title
    entry = util.get_entry(title)

    # Conditional if no entry found
    if not entry:
        return render(request, "encyclopedia/warning.html", {
        "content" : "<h1>Page not Found</h1>"
    })

    # Render Markdown Entry to HTML Page
    content = markdown2.markdown(entry)
    return render(request, "encyclopedia/page.html", {
        "content" : content,
        "title" : title,
        # Adding link to edit page
        "editform" : f"<a href='/editform/{title}'>Edit Page</a>"
    })

# Search Function
def search(request):
    # Get query string from user
    get = request.GET
    q = get['q']
    # List entries for searching 
    entries = util.list_entries()

    # Case insensitive search
    if q.upper() in (entry.upper() for entry in entries):
        return redirect(f'wiki/{q}')
    else:
        result = [i for i in entries if q.upper() in i.upper()]
        return render(request, "encyclopedia/search.html", {
        "result": result
    })

# Adding New Page
def add(request):
    # If request to post
    if request.method == "POST":
        # Server side validation
        form = NewPagesForm(request.POST)
        if form.is_valid():
            # Input cleaned variable for title, content, and entries
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()

            # Search in case there is already same entries title
            if title.upper() in (entry.upper() for entry in entries):
                return render(request, "encyclopedia/warning.html", {
                    "content": "<h1>Page already exist.</h1>"
                })
            # If there is not save entry and return to the page
            else:
                util.save_entry(title, content)
                return redirect(f'wiki/{title}')

        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
    })

    # Else just show the form
    else:
        return render(request, "encyclopedia/add.html", {
            "form": NewPagesForm()
        })

# Edit entry based on title
def editform(request, title):
        content = util.get_entry(title)
        form = NewPagesForm({'title': title,'content': content})
        return render(request, "encyclopedia/editform.html", {
            "form": form
        })

# Push the edit to the entry
def pushedit(request):
    if request.method == "POST":
        form = NewPagesForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            title = form.cleaned_data["title"]
            util.save_entry(title, content)
            return redirect(f'wiki/{title}')

# Random Page
def randompage(request):
    entries = util.list_entries()
    title = random.choice(entries)
    entry = util.get_entry(title)
    content = markdown2.markdown(entry)
    return render(request, "encyclopedia/page.html", {
        "content" : content,
        "title" : title,
        "editform" : f"<a href='/editform/{title}'>Edit Page</a>"
    })