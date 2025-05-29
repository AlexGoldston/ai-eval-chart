import pandas as pd
import random

# Set a random seed for reproducibility
random.seed(42)

# Generate sample use case names
usecase_names = [f"Use Case {i+1}" for i in range(50)]

# Function to generate randomized use case data
def generate_usecase_data(name):
    cost = random.randint(10, 100)
    speed = random.randint(10, 100)
    culture = random.randint(10, 100)
    quality = random.randint(10, 100)
    long_term = random.randint(10, 100)
    complexity = random.randint(10, 100)
    time = random.randint(10, 100)

    impact_score = (cost + speed + culture + quality + long_term) / 5
    effort_score = (complexity + time) / 2
    overall_score = round(impact_score / effort_score, 2)

    if complexity >= 50 and time < 50:
        quadrant = "HIGH EFFORT, QUICK WINS"
    elif complexity >= 50 and time >= 50:
        quadrant = "STRATEGIC INVESTMENTS"
    elif complexity < 50 and time < 50:
        quadrant = "QUICK WINS"
    else:
        quadrant = "LONG TERM LOW EFFORT"

    return {
        "Use Case": name,
        "Cost": cost,
        "Speed": speed,
        "Culture": culture,
        "Quality": quality,
        "Long-term Value": long_term,
        "Complexity": complexity,
        "Time": time,
        "Overall Score": overall_score,
        "Quadrant": quadrant
    }

# Generate the data and save to CSV
sample_data = pd.DataFrame([generate_usecase_data(name) for name in usecase_names])
sample_data.to_csv("sample_usecases.csv", index=False)

print("Sample use case data saved to 'sample_usecases.csv'")
