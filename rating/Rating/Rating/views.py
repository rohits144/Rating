import json
from datetime import datetime
import os
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .forms import RatingForm
from .config import FILE_DIR


class CreatePremium(viewsets.ViewSet):
    '''
    This class is the main API which will receive request from frontend and will save the data in form of file or
    Database as needed according to Business need
    '''

    def get(self, requests):
        form = RatingForm()
        context = {
            "form": form
        }
        render(requests, "templates/Rating/create_premium.html", context)

    def post(self, requests):
        form = RatingForm(requests.data)
        if form.is_valid():
            form_dict = form.cleaned_data() # All fields are taken input from a form except Date
            # set date to current time
            form_dict['date'] = (datetime.now())
            exposure_unit = form_dict['exposure_unit']
            rates = json.load(form_dict['rate']) # rates is a dictionary of rates like {'rate1': value1, 'rate2': value2 ...}
            for rate in rates.keys():
                if rate < 1.0 and rate > 0.1:
                    print('Rate is valid')
                else:
                    raise Exception

            insurance_premium_dict = dict()
            counter = 0
            for rate in rates:
                insurance_premium_dict[counter] = rate * exposure_unit # Calculation of Insurance Premium
            form_dict['insurance_premium'] = insurance_premium_dict
            premium_name = form_dict['premium_name']
            os.chdir(FILE_DIR)
            filename = premium_name + '.txt'
            with open(filename, 'r+') as f:
                f.write(json.dump(form_dict))

        else:
            print('Form Data is not valid, redirect to create premium page')
            redirect("premium")


class RetrivePremium(viewsets.ViewSet):
    """
    This class redirect you to a HTML page where you need to enter premium name and it will retrive details for that
    premium by reading the file in which details are present
    """
    def get(self, requests):
        redirect(requests, 'templates/Rating/retrive_premium.html')

    def post(self, requests):
        premium_name = requests.data['premium_name']
        os.chdir(FILE_DIR)
        filename = premium_name + '.txt'
        detail = ''
        with open(filename, 'r') as f:
            print(f.read())
            detail = f.read()

        redirect(requests, 'templates/Rating/display_premium.html', detail)
