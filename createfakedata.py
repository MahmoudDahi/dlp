import pandas as pd
import random

# Generate fake data
def generate_fake_data(num_rows):
    data = {
        'Name': [],
        'Age': [],
        'Email': [],
        'Identification Number': [],
        'Credit Card': []
    }

    for _ in range(num_rows):
        name = random.choice(['John', 'Alice', 'Bob', 'Emily', 'Michael'])
        age = random.randint(20, 60)
        email = f'{name.lower()}_{random.randint(100, 999)}@example.com'
        identification_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        credit_card = ''.join([str(random.randint(0, 9)) for _ in range(16)])

        data['Name'].append(name)
        data['Age'].append(age)
        data['Email'].append(email)
        data['Identification Number'].append(identification_number)
        data['Credit Card'].append(credit_card)

    return data

# Function to format numbers
def format_numbers(number):
    if len(number) == 16:
        return f'{number[:4]} {number[4:8]} {number[8:12]} {number[12:]}'
    return number

# Create DataFrame
num_rows = 20  # Number of rows of fake data
fake_data = generate_fake_data(num_rows)
df = pd.DataFrame(fake_data)

# Apply formatting to identification numbers and credit cards
df['Credit Card'] = df['Credit Card'].apply(format_numbers)

# Shuffle DataFrame rows
df = df.sample(frac=1).reset_index(drop=True)

# Save DataFrame to Excel file
file_path = '/home/dahi/Downloads/dlp12.xlsx'     
df.to_excel(file_path, index=False)

print(f"Excel file with fake data saved to: {file_path}")
    