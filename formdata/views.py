from django.shortcuts import render, redirect, HttpResponse
def show_form(request):
    '''show the HTML form to the client'''
    #use this to produce the response 
    template_name = 'formdata/form.html'
    return render(request, template_name)

def submit(request):
    '''Handle the form submission. Read out the form data. Generate a response'''
    template_name = 'formdata/confirmation.html'
    # read the form data into python variables
    #check if the request is a POST (vs GET)
    if request.POST:
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']
        #package the data up to be used in response
        context = {
            'name': name,
            'favorite_color': favorite_color,
        }

        return render(request, template_name, context)
    # if client got here on get then send them back to the form 

    # template_name = 'formdata/form.html'
    # return render(request, template_name)
    return redirect("show_form")

