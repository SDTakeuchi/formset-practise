from django.shortcuts import redirect, render, get_object_or_404
from .models import Programmer, Language
from django.forms import modelformset_factory, inlineformset_factory
from django.views.generic import ListView
from .forms import ProgrammerCreateForm

class ProgrammerListView(ListView):
    template_name = 'proger_list.html'
    model = Programmer

# modelformset ver.
def model_index(request, programmer_id):
    programmer = Programmer.objects.get(pk=programmer_id)
    LanguageFormset = modelformset_factory(Language, fields=('name',))
    
    if request.method == 'POST':
        formset = LanguageFormset(request.POST, queryset=Language.objects.filter(programmer__id=programmer.id))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.programmer_id = programmer.id
                instance.save()
            return redirect('inline_index', programmer_id=programmer.id)
    
    formset = LanguageFormset(queryset=Language.objects.filter(programmer__id=programmer.id))
    context = {
        'formset': formset,
        'user': programmer,
        }

    return render(request, 'index.html', context)


LanguageFormset = inlineformset_factory(
    parent_model = Programmer, 
    model = Language,
    fields = ('name',),
    extra = 1,
    max_num = 100
    )

# inlineformset ver.
def inline_index(request, programmer_id):
    programmer = Programmer.objects.get(pk=programmer_id)
    
    if request.method == 'POST':
        formset = LanguageFormset(request.POST, instance=programmer) #associate w/ parent class
        if formset.is_valid():
            formset.save()
            return redirect('model_index', programmer_id=programmer.id)

    formset = LanguageFormset(instance=programmer)
    context = {
        'formset': formset,
        'user': programmer,
        }

    return render(request, 'index.html', context)


def add_user(request):
    form = ProgrammerCreateForm(request.POST or None)
    context = {'form': form}

    if request.method == 'POST' and form.is_valid():
        programmer = form.save(commit=False)
        formset = LanguageFormset(request.POST, request.FILES, instance=programmer)
        if formset.is_valid():
            programmer.save()
            formset.save()
            return redirect('list')

        else:
            context['formset'] = formset
    else:
        context['formset'] =LanguageFormset()
        return render(request, 'add_user.html', context)


def edit_user(request, pk):
    programmer = get_object_or_404(Programmer, pk=pk)
    form = ProgrammerCreateForm(request.POST or None, instance=programmer)
    formset = LanguageFormset(request.POST or None, instance=programmer)

    if request.method == 'POST' and form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('list')
    
    context = {
        'form':form,
        'formset':formset
    }
    return render(request, 'add_user.html', context)