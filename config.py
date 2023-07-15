debug = False

inputBaseUrl = 'data/'

# # for customer_churn_dataset-testing-master
# ei = ['CustomerID']
# qi = ['Age', 'Gender', 'Tenure', 'Usage_Frequency', 'Support_Calls', 'Payment_Delay',
#       'Subscription_Type', 'Contract_Length']
# inputFile = 'customer_churn_dataset-testing-master.csv'

# for Salary_Data
ei = []
qi = ['Age', 'Gender', 'Education_Level', 'Years_of_Experience']
inputFile = 'Salary_Data.csv'


k_list = [5, 10, 15, 20, 25, 30]
outputBaseUrl = 'output/'
mode = 'strict'  # ['strict', 'relaxed']

# if True, user needs to provide generalization hierarchies for categorical attributes below
userDefinedCatAvailable = True
userDefinedCat = {
    'Gender': {
        '0': 'Male',
        '1': 'Female',
        '2': 'Other',
        '0-1': 'Person',
        '0-2': 'Person',
        '1-2': 'Person'
    },
    'Education_Level': {
        '0': 'Bachelor\'s',
        '1': 'Master\'s',
        '2': 'PhD',
        '3': 'High School',
        '0-1': 'University',
        '1-2': 'Post-Graduate',
        '0-2': 'University',
        '0-3': 'Educated',
        '1-3': 'Educated',
        '2-3': 'Educated'
    },
    'Subscription_Type': {
        '0': 'Basic',
        '1': 'Standard',
        '2': 'Premium',
        '0-1': 'non-premium',
        '1-2': 'non-basic',
        '0-2': 'subscribed'
    },
    'Contract_Length': {
        '0': 'Monthly',
        '1': 'Quarterly',
        '2': 'Annual',
        '0-1': 'non-annual',
        '1-2': 'multi-month',
        '0-2': 'has-contract'
    }
}
