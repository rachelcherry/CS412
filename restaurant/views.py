from django.shortcuts import render, redirect, HttpResponse
import random
import datetime
import time



special_list = ["Pita and Hummus $10", "Shrimp Kebab $10", "Brussel Sprouts $10"]
def main(request):
    '''show the main page'''
    template_name = 'restaurant/main.html'
    return render(request, template_name)

def order(request):
    '''show the order page '''
    template_name = 'restaurant/order.html'
    context = {
        'special': random.choice(special_list),
    }
    return render(request, template_name, context)

def submit(request):
    '''Handle the form submission. Read out the form data. Generate a response'''
    template_name = 'restaurant/confirmation.html'
    # variables to accumulate the total price
    Seafood = 34
    Chicken = 15
    Swordfish = 18
    Bronzino = 28
    Special = 10
    Rice = 2
    Sauce = 1
    total = 0
    # read the form data into python variables
    #check if the request is a POST (vs GET)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']
        maincourse1 = request.POST.get('MainCourse1')  
        maincourse2 = request.POST.get('MainCourse2')  
        maincourse3 = request.POST.get('MainCourse3')  
        maincourse4 = request.POST.get('MainCourse4')  
        add1 = request.POST.get('Additions1') 
        add2 = request.POST.get('Additions2') 
        add3 = request.POST.get('Additions3') 
        special = request.POST.get('DailySpecial')  
        # getting the time and then adding a random numnber between 30 and 60 
        current_time = datetime.datetime.now()
        add = random.randint(30, 60)
        ready_time = current_time + datetime.timedelta(minutes=add)
    #checking if the user clicked on each main course item
    # if they did, add its price to the total price 
        if maincourse1:
            total += Seafood
        if maincourse2:
            total+= Chicken
        if maincourse3:
            total+= Bronzino
        if maincourse4:
            total += Swordfish
        if add1:
            total += Rice
        if add2:
            total += Sauce
        if special:
            total += Special
        special_instructions = request.POST.get('SpecialInstructions')
         #package the data up to be used in response
        context = {
            'name': name,
            'email': email,
            'number': number,
            'time': ready_time,
            'main_course1': maincourse1,
            'main_course2': maincourse2,
            'main_course3': maincourse3,
            'main_course4': maincourse4,
            'additions1': add1,
            'additions2': add2,
            'additions3': add3,
            'special': special,
            'total': total,
            'special_instructions': special_instructions,
        }

   
        return render(request, template_name, context)
    #redirect 
    return redirect("order")
