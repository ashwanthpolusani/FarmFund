from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from home.models import Farm, Income, Expenditure, Farm
from itertools import chain
from django.db.models import Sum
from collections import defaultdict

# Create your views here.
def home(request):
    total_budget = Farm.objects.aggregate(total_budget=Sum('crop_budget'))['total_budget'] or 0
    total_income = Income.objects.aggregate(total_income=Sum('amount'))['total_income'] or 0
    total_expenditure = Expenditure.objects.aggregate(total_expenditure=Sum('amount'))['total_expenditure'] or 0

    # Data for graphs
    farms = Farm.objects.all()
    crop_names = [farm.crop_name for farm in farms]
    crop_budgets = [farm.crop_budget for farm in farms]

    expenditures = Expenditure.objects.all()

    # Merge expenditures with the same details
    merged_expenditures = defaultdict(int)
    for expenditure in expenditures:
        merged_expenditures[expenditure.details] += expenditure.amount

    # Prepare data for the graph
    expenditure_details = list(merged_expenditures.keys())
    expenditure_amounts = list(merged_expenditures.values())

    context = {
        'total_budget': total_budget,
        'total_income': total_income,
        'total_expenditure': total_expenditure,
        'crops': farms,  # Updated to use Farm objects
        'crop_names': crop_names,
        'crop_budgets': crop_budgets,
        'expenditure_details': expenditure_details,
        'expenditure_amounts': expenditure_amounts,
    }
    return render(request, 'home.html', context)

def addFarm(request):
    context={'success': False}
    if request.method == 'POST':
        crop_name = request.POST['crop_name']
        farm_name = request.POST['farm_name']
        Description = request.POST['description']
        Budget = request.POST['budget']
        ins=Farm(crop_name=crop_name, farm_name=farm_name, crop_description=Description, crop_budget=Budget)
        ins.save()
        context={'success': True}
        print(crop_name, farm_name,Description, Budget)
    return render(request, 'addFarm.html', context)

def farms(request):
    all_farms = Farm.objects.all()
    context = {'farms': all_farms}
    return render(request, 'farms.html', context)

def farm_detail(request, farm_id):
    # Fetch the Farm object with related Income and Expenditure objects
    farm = get_object_or_404(Farm.objects.prefetch_related('income_set', 'expenditure_set'), id=farm_id)
    
    # Calculate total income and expenditure using Django's aggregate function
    total_income = farm.income_set.aggregate(total=Sum('amount'))['total'] or 0
    total_expenditure = farm.expenditure_set.aggregate(total=Sum('amount'))['total'] or 0
    
    # Fetch all farms
    all_farms = Farm.objects.all()
    
    context = {
        'farm': farm,
        'total_income': total_income,
        'total_expenditure': total_expenditure,
        'incomes': farm.income_set.all(),
        'expenditures': farm.expenditure_set.all(),
        'all_farms': all_farms
    }
    return render(request, 'farm_detail.html', context)

def add_income_expenditure(request):
    if request.method == 'POST':
        farm_id = request.POST['farm_id']
        amount = int(request.POST['amount'])
        type = request.POST['type']
        details = request.POST['details']
        collaborate_farms = request.POST.getlist('collaborate_farms')
        collaborate_farms.append(farm_id)
        len_collaborate_farms = len(collaborate_farms)
        split_amount = amount // (len_collaborate_farms)
        for farm in collaborate_farms:
            if farm==collaborate_farms[-1]:
                split_amount=amount
            if type == 'income':
                
                Income.objects.create(farm_id=farm, amount=split_amount, details=details)
            else:
                Expenditure.objects.create(farm_id=farm, amount=split_amount, details=details)
            amount-=split_amount

        return redirect('farm_detail', farm_id=farm_id)
    
def txnHistory(request):
    inc = Income.objects.all()
    exp = Expenditure.objects.all()
    # Combine income and expenditure transactions
    transactions = list(chain(inc, exp))
    
    # Prepare detailed transaction data
    detailed_transactions = []
    for txn in transactions:
        farm = Farm.objects.get(id=txn.farm_id)
        txn_type = 'income' if isinstance(txn, Income) else 'expense'
        detailed_transactions.append({
            'date': txn.date,
            'crop': farm.crop_name,
            'farm': farm.farm_name,
            'type': txn_type,
            'amount': txn.amount,
            'details': txn.details
        })
    
    context = {'transactions': detailed_transactions}
    return render(request, 'txnHistory.html', context)

def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id)
    farm_id = income.farm.id
    income.delete()
    return redirect('farm_detail', farm_id=farm_id)

def delete_expenditure(request, expenditure_id):
    expenditure = get_object_or_404(Expenditure, id=expenditure_id)
    farm_id = expenditure.farm.id
    expenditure.delete()
    return redirect('farm_detail', farm_id=farm_id)

def edit_transaction(request, transaction_id, transaction_type):
    if transaction_type == 'income':
        transaction = get_object_or_404(Income, id=transaction_id)
    elif transaction_type == 'expenditure':
        transaction = get_object_or_404(Expenditure, id=transaction_id)
    else:
        return redirect('farm_detail')  # Redirect if invalid type

    if request.method == 'POST':
        transaction.amount = request.POST['amount']
        transaction.details = request.POST['details']
        transaction.save()
        return redirect('farm_detail', farm_id=transaction.farm.id)

    context = {
        'transaction': transaction,
        'transaction_type': transaction_type
    }
    return render(request, 'edit_transaction.html', context)
