import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from tqdm import tqdm
import os

_BADGES = ["Introduction to Image Generation", 
        "Attention Mechanism", 
        "Encoder-Decoder Architecture",
        "Transformer Models and BERT Model",
        "Create Image Captioning Models",
        "Introduction to Generative AI Studio",
        "Generative AI Explorer - Vertex AI",
        "Explore and Evaluate Models using Model Garden",
        "Prompt Design using PaLM"] 


def scrape_badges(input_file="urls.xlsx"):

    # Load the Excel sheet
    df = pd.read_excel(input_file)

    # Prepare the output DataFrame
    output = pd.DataFrame(columns=['URL', 'Name', 'Error/Badge Info'] + _BADGES + ["Badge Count"] + ['Date Checked'])

    # Function to check URL format
    def is_valid_url(url):
        return bool(re.match(r'https://www\.cloudskillsboost\.google/public_profiles/.+', url))

    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        url = row[0]
        url = url.strip()
        badge_count = 0
        if is_valid_url(url):
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract H1 innerHTML
                h1_innerHTML = soup.find('h1', class_='ql-display-small').get_text(strip=True)

                # Check for profile badges
                badges_found = soup.find_all('div', class_='profile-badge')
                badge_info = {badge: False for badge in _BADGES}
                if not badges_found:
                    error_info = "No badges"
                else:
                    error_info = ""
                    for badge_div in badges_found:
                        span = badge_div.find('span', class_='ql-title-medium')
                        if span:
                            badge_name = span.get_text(strip=True)
                            if badge_name in _BADGES:
                                badge_info[badge_name] = True
                                badge_count += 1

                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                # Append row to the output DataFrame
                row_data = [url, h1_innerHTML, error_info] + [badge_info[badge] for badge in _BADGES]+ [badge_count] + [time]
                output = pd.concat([output, pd.DataFrame([row_data], columns=output.columns)], ignore_index=True)

            except Exception as e:
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                output = pd.concat([output, pd.DataFrame([[url, '', 'Error fetching page'] +  [False] * len(_BADGES) + [badge_count] + [time]], columns=output.columns)], ignore_index=True)
        else:
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            output = pd.concat([output, pd.DataFrame([[url, '', 'Invalid URL format'] +  [False] * len(_BADGES)+ [badge_count] + [time]], columns=output.columns)], ignore_index=True)

    # Append a row
    # In this row, only have a single column with the value "Total Badges"
    # It should have the sum of integers in the second last column for all rows
    output = pd.concat([output, pd.DataFrame([['Total Badges'] + [''] * (len(output.columns) - 2) + [output.iloc[:, -2].sum()]], columns=output.columns)], ignore_index=True)

    current_dir = os.getcwd()
    file_name = "output.xlsx"
    file_path = os.path.join(current_dir, file_name)
    # Write the output DataFrame to a new Excel file
    output.to_excel(file_path, index=False)
    return file_path
