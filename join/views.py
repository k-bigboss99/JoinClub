from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import JoinForm
from .models import Member

def index(request):
    return render(request, 'index.html', {})

def join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            Member(name=form['name'].value(), nid=form['nid'].value(), dept=form['dept'].value(), level=form['level'].value(), phone=form['phone'].value(), email=form['email'].value()).save()
            form = JoinForm()
            return HttpResponseRedirect(reverse('join:index'))
    else:
        form = JoinForm()
    return render(request, 'join.html', {'form': form})

@login_required
def search(request):
    if request.method == 'POST':
        nid = request.POST.get('nid')
        name = request.POST.get('name')
        if nid:
            try:
                member = Member.objects.get(nid=nid)
                return HttpResponseRedirect(reverse('join:review', args=[member.id]))
            except Member.DoesNotExist:
                return render(request, 'search.html', {})
        elif name:
            try:
                member = Member.objects.get(name=name)
                return HttpResponseRedirect(reverse('join:review', args=[member.id]))
            except Member.DoesNotExist:
                return render(request, 'search.html', {})
    return render(request, 'search.html', {})

@login_required
def review(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        if member.status == 'UR':
            member.status = 'NP'
            member.save()
        elif member.status == 'NP':
            member.status = 'M'
            member.save()
    return render(request, 'review.html', {'member': member})

@login_required
def edit(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            member.name = form['name'].value()
            member.nid = form['nid'].value()
            member.dept = form['dept'].value()
            member.level = form['level'].value()
            member.phone = form['phone'].value()
            member.email = form['email'].value()
            member.save()
            form = JoinForm()
        return HttpResponseRedirect(reverse('join:review', args=[member.id]))
    else:
        form = JoinForm()
    return render(request, 'edit.html', {'form': form, 'member': member})

@login_required
def view(request):
    M_members = Member.objects.filter(status='M')
    NP_members = Member.objects.filter(status='NP')
    UR_members = Member.objects.filter(status='UR')
    return render(request, 'view.html', {'M_members': M_members, 'NP_members': NP_members, 'UR_members': UR_members})

def chart(request):
    return render(request, 'chart.html', {})