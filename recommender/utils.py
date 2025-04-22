# recommender/utils.py
import os
import pandas as pd
import joblib
import google.generativeai as genai
from django.conf import settings

class VaccineRecommender:
    def __init__(self):
        # Paths to model files
        model_dir = settings.MODEL_FILES_DIR
        self.model_path = os.path.join(model_dir, 'C:/Users/pardh/OneDrive/Desktop/vaccination/vaccine_recommender/models/vaccine_clustering_model (1).pkl')
        self.vaccine_encoder_path = os.path.join(model_dir, 'C:/Users/pardh/OneDrive/Desktop/vaccination/vaccine_recommender/models/vaccine_encoder (1).pkl')
        self.dose_encoder_path = os.path.join(model_dir, 'C:/Users/pardh/OneDrive/Desktop/vaccination/vaccine_recommender/models/dose_encoder (1).pkl')
        self.csv_path = os.path.join(model_dir, 'C:/Users/pardh/OneDrive/Desktop/vaccination/vaccine_recommender/models/vaccine_doses (1) (1).csv')
        
        # Load the models and dataset
        self.load_models()
        self.load_dataset()
        
        # Configure Gemma API - You should use environment variables for API keys in production
        self.api_key = os.environ.get('GEMMA_API_KEY', '')
        genai.configure(api_key=self.api_key)
    
    def load_models(self):
        """Load trained models and encoders"""
        try:
            self.model = joblib.load(self.model_path)
            self.vaccine_encoder = joblib.load(self.vaccine_encoder_path)
            self.dose_encoder = joblib.load(self.dose_encoder_path)
        except (FileNotFoundError, IOError) as e:
            raise Exception(f"Failed to load models: {str(e)}")
    
    def load_dataset(self):
        """Load and prepare the vaccine dataset"""
        try:
            # Load data
            self.data = pd.read_csv(self.csv_path)
            
            # Clean column names
            self.data = self.data.rename(columns=lambda x: x.strip())
            
            # Convert age ranges to weeks
            self.data[['Min_Age_Weeks', 'Max_Age_Weeks']] = self.data['Applicable Age'].apply(
                lambda x: pd.Series(self.convert_age_range_to_weeks(x))
            )
            
            # Drop rows where age conversion failed
            self.data = self.data.dropna(subset=['Min_Age_Weeks', 'Max_Age_Weeks'])
            
            # Encode categorical features
            self.data['Vaccine_encoded'] = self.vaccine_encoder.transform(self.data['Vaccine'])
            self.data['Dose_encoded'] = self.dose_encoder.transform(self.data['Dose'])
            
        except Exception as e:
            raise Exception(f"Failed to load or process the dataset: {str(e)}")
    
    def convert_age_range_to_weeks(self, label):
        """Convert age range labels to weeks"""
        try:
            if pd.isna(label):
                return None, None
                
            label = str(label).lower()
            
            if '-' in label:
                lower, upper = label.split('-')
                lower_value = int(lower.strip().split()[0])
                upper_value = int(upper.strip().split()[0])
                
                if 'week' in label:
                    return lower_value, upper_value
                elif 'month' in label:
                    return lower_value * 4, upper_value * 4
                elif 'year' in label:
                    return lower_value * 52, upper_value * 52
            else:
                value = int(label.split()[0].strip())
                if 'week' in label:
                    return value, value
                elif 'month' in label:
                    return value * 4, value * 4
                elif 'year' in label:
                    return value * 52, value * 52
        
        except (ValueError, IndexError):
            return None, None
    
    def convert_age_to_weeks(self, age, unit):
        """Convert user input age to weeks"""
        unit = unit.lower()
        if unit == "weeks":
            return age
        elif unit == "months":
            return age * 4
        elif unit == "years":
            return age * 52
        else:
            return None
    
    def next_vaccine_info(self, user_age_in_weeks):
        """Get information about the next scheduled vaccine"""
        future_vaccines = self.data[self.data['Min_Age_Weeks'] > user_age_in_weeks]
        
        if not future_vaccines.empty:
            next_vaccine = future_vaccines.sort_values('Min_Age_Weeks').iloc[0]
            next_age = next_vaccine['Min_Age_Weeks']
            weeks_remaining = next_age - user_age_in_weeks
            
            if weeks_remaining >= 52:
                time_remaining = f"{weeks_remaining // 52} years"
            elif weeks_remaining >= 4:
                time_remaining = f"{weeks_remaining // 4} months"
            else:
                time_remaining = f"{weeks_remaining} weeks"
                
            return next_vaccine['Vaccine'], time_remaining
        else:
            return "No future vaccines available.", "N/A"
    
    def llm_analysis(self, age, unit, applicable_vaccines, next_vaccine, time_remaining):
         prompt = f"""
                    You are an AI healthcare assistant. Analyze the vaccine dataset and provide the most accurate vaccine recommendation.
                    Given the dataset, provide a detailed explanation of the vaccines required for a {age} {unit}-old child.
                    Mention the applicable vaccines, doses, and when the next vaccine is due.

                    Applicable Vaccines: {', '.join(applicable_vaccines['Vaccine'].tolist()) if not applicable_vaccines.empty else 'None'}
                    Doses: {', '.join(applicable_vaccines['Dose'].tolist()) if not applicable_vaccines.empty else 'None'}
                    Next Vaccine: {next_vaccine}, Available in: {time_remaining}.
               """

         # Generate natural language response using Gemma LLM
         model = genai.GenerativeModel('gemini-1.5-pro')
         response = model.generate_content(prompt)

         return response.text
            #  """Alternative LLM analysis using Gemma"""
           # """Generate a natural language response using Gemma LLM"""
        
        
        # try:
        #     # Create appropriate message based on available vaccines
        #     if applicable_vaccines.empty:
        #         message = f"The user aged {age} {unit} is not eligible for any vaccine currently. " \
        #                 f"The next applicable vaccine will be {next_vaccine}, available in {time_remaining}."
        #     else:
        #         vaccines = ", ".join(applicable_vaccines['Vaccine'].tolist())
        #         doses = ", ".join(applicable_vaccines['Dose'].tolist())
        #         message = f"For the age of {age} {unit}, the recommended vaccines are: {vaccines} with doses: {doses}. " \
        #                 f"The next vaccine will be {next_vaccine}, available in {time_remaining}."
            
        #     # Skip LLM generation if API key is not available
        #     if not self.api_key:
        #         return message
                
        #     # Generate natural language response using Gemma LLM
        #     model = genai.GenerativeModel('gemini-1.5-pro')
        #     response = model.generate_content(message)
        #     return response.text
            
        # except Exception as e:
        #     # Fallback to basic message if LLM fails
        #     return message
    
    def recommend_vaccine(self, age, unit):
        """Main function to get vaccine recommendations"""
        # Convert age to weeks
        age_in_weeks = self.convert_age_to_weeks(age, unit)
        if age_in_weeks is None:
            return {
                'error': f"Invalid age unit: {unit}. Please use 'weeks', 'months', or 'years'."
            }
        
        # Filter applicable vaccines
        applicable_vaccines = self.data[
            (self.data['Min_Age_Weeks'] <= age_in_weeks) & 
            (self.data['Max_Age_Weeks'] >= age_in_weeks)
        ]
        
        # Get next vaccine info
        next_vaccine, time_remaining = self.next_vaccine_info(age_in_weeks)
        
        # Get LLM analysis
        analysis = self.llm_analysis(age, unit, applicable_vaccines, next_vaccine, time_remaining)
        
        # Prepare result
        result = {
            'age': age,
            'unit': unit,
            'applicable_vaccines': applicable_vaccines.to_dict('records') if not applicable_vaccines.empty else [],
            'next_vaccine': next_vaccine,
            'time_remaining': time_remaining,
            'analysis': analysis
        }
        
        return result

