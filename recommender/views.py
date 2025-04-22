# recommender/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .forms import VaccineForm
from .utils import VaccineRecommender


def index(request):
    """View for the homepage with vaccine form"""
    form = VaccineForm()
    
    if request.method == 'POST':
        form = VaccineForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data['age']
            unit = form.cleaned_data['unit']
            
            # Process the form data
            try:
                recommender = VaccineRecommender()
                result = recommender.recommend_vaccine(age, unit)
                
                if 'error' in result:
                    messages.error(request, result['error'])
                    return render(request, 'recommender/index.html', {'form': form})
                
                # Store results in session for the result page
                request.session['vaccine_result'] = result
                return redirect(reverse('recommender:result'))
                
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    
    return render(request, 'recommender/index.html', {'form': form})

def result(request):
    """View for displaying vaccine recommendation results"""
    # Retrieve results from session
    result = request.session.get('vaccine_result')
    
    if not result:
        messages.warning(request, "No vaccine recommendation data found. Please enter your age information.")
        return redirect(reverse('recommender:index'))
    
    return render(request, 'recommender/result.html', {'result': result})

