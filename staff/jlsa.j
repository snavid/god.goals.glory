    path('add/', views.add_user, name='add_user'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
    path('users_list/', views.users_list, name='users_list'),
    path("edit_user/<int:user_id>/", views.edit_user, name="edit_user"),  # Edit template
    
def users_list(request):
    users = user.objects.all()
    return render(request, 'staff/users_list.html', {'user': users})

def edit_user(request, user_id):
    user = get_object_or_404(user, id=user_id)
    
    if request.method == "POST":
        form = userForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'user edited successfully')
            return redirect('users_list')
    else:
        form = userForm(instance=user)
    
    return render(request, 'staff/actions_form.html', {'form': form, 'title': 'Edit user'})


@login_required
def add_user(request):
    if request.method == 'POST':
        form = userForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'user added successfully')
            return redirect('users_list')
    else:
        form = userForm()
    context = {
    'form': form,
    'title': 'Add user',
    'action': 'Add user',
    }
    return render(request, 'staff/actions_form.html', context)

@login_required
def delete_user(request, pk):
    user = get_object_or_404(user, pk=pk)
    user.delete()
    return redirect('users_list')

