from django.shortcuts import render
from joblib import load
# model =load('./savedModels/model.joblib')



# # def predict_route(request):
# #     if request.method == 'POST':
# #         vehicle_type = request.POST.get('vehicle_type')
# #         place = request.POST.get('place')
# #         road_type = request.POST.get('road_type')

# #         # Your logic for predicting accident risk based on the inputs
# #         y_pred=model.predict([[vehicle_type, place, road_type]])
        
# #         return render(request, 'userdash.html', {'prediction': "HAII"})

# #     return render(request, 'userdash.html')


# from django.shortcuts import render
# from sklearn.preprocessing import LabelEncoder

# # Assuming label_encoders is available and was created during model training
# label_encoders = {
#     'road_name_in_googleMap': le_road_name,
#     'vehicle_type': vehicle_type,
#     'road_type': le_road_type,
#     'seviarity_of_accident': le_severity,
# }

# def predict_route(request):
#     if request.method == 'POST':
#         vehicle_type = request.POST.get('vehicle_type')
#         place = request.POST.get('place')  # Assuming place is numerical or preprocessed
#         road_type = request.POST.get('road_type')

#         # Encode inputs using the pre-fitted label encoders
#         vehicle_type_encoded = label_encoders['vehicle_type'].transform([vehicle_type])[0]
#         road_type_encoded = label_encoders['road_type'].transform([road_type])[0]

#         # Prepare the input array for the model (ensure the order matches your training data)
#         X_new = [place, vehicle_type_encoded, road_type_encoded]

#         # Make a prediction (assuming `model` is your trained model)
#         prediction = model.predict([X_new])

#         return render(request, 'your_template.html', {'prediction': prediction})

#     return render(request, 'your_template.html')



from django.shortcuts import render
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load your pre-trained model (This should be loaded once when the server starts)
# If you need to reload or retrain, include the logic for that
label_encoders = {}
rf_model = None

def load_model():
    global rf_model, label_encoders
    # Load the synthesized dataset (used for label encoding)
    data = pd.read_csv('vscode/synthesized_accident_data.csv')

    # Encode categorical variables
    for column in ['road_name_in_googleMap', 'vehicle_type', 'road_type']:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
        label_encoders[column] = le

    # Define features (X) and the target variable (y)
    X = data[['road_name_in_googleMap', 'vehicle_type', 'road_type']]
    y = data['death']

    # Train the Random Forest model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X, y)

load_model()

# Define the view to handle the form submission
def predict_accident(request):
    if request.method == 'POST':
        road_name_in_googleMap = request.POST['road_name_in_googleMap']
        vehicle_type = request.POST['vehicle_type']
        road_type = request.POST['road_type']

        # Prepare the input data
        input_data = pd.DataFrame({
            'road_name_in_googleMap': [label_encoders['road_name_in_googleMap'].transform([road_name_in_googleMap])[0]],
            'vehicle_type': [label_encoders['vehicle_type'].transform([vehicle_type])[0]],
            'road_type': [label_encoders['road_type'].transform([road_type])[0]]
        })

        # Predict the probability
        probability = rf_model.predict_proba(input_data)[:, 1][0]
        risk1="lOW RISK"
        risk2="HIGH RISK"
        if probability>0.4:
             return render(request, 'userdash.html', {
            'probability': risk1,
            'road_name': road_name_in_googleMap,
            'vehicle_type': vehicle_type,
            'road_type': road_type
        })
        else:
            return render(request, 'userdash.html', {
            'probability': risk2,
            'road_name': road_name_in_googleMap,
            'vehicle_type': vehicle_type,
            'road_type': road_type
        })


        # # Render the result back to the template
        # return render(request, 'userdash.html', {
        #     'probability': probability,
        #     # 'road_name': road_name,
        #     # 'vehicle_type': vehicle_type,
        #     # 'road_type': road_type
        # })

    return render(request, 'userdash.html')
