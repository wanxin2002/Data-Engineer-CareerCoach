# Data-Engineer-CareerCoach
Assignment for Data Engineer Intern (2025) on data extraction and processing

## Introduction
**Case study scenario**  
Steven, a travel blogger, is embarking on a travel food series project. He intends to analyse data from Zomato to find restaurants with good user ratings and interesting past events. 
The task given is to assist Steven in extracting and analysing the necessary data from the provided JSON and Excel files.

**Data Sources**
1. Restaurant data: https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json
2. Country data: https://github.com/Papagoat/brain-assessment/blob/main/Country-Code.xlsx?raw=true (also in 'data' folder)

**Outputs from Tasks**  
The csv outputs for tasks 1 to 3 are in the 'output' folder

## Setup Instructions
1. Clone the repository:
```bash
git clone https://github.com/wanxin2002/Data-Engineer-CareerCoach.git
```
2. Navigate to the Repository:
```bash
cd Data-Engineer-CareerCoach
```
3. Set up the virtual environment (optional) and install dependencies:
```bash
python -m venv venv
source venv/bin/activate   # On macOS
venv\Scripts\activate      # On Windows
pip install -r requirements.txt
```
4. Run the code:
```bash
python main.py
```

## Considerations Made
1. **Task 1**: Event data extraction field includes the entire list of events (where their details are in dictionary format) so that event details can be easily extracted from the column by user to perform further analysis if needed. Additional column was added to see the number of events that has happened for each restaurant more directly.

2. **Task 2**: Events to be excluded can be generalised to 2 categories, those that start later than 30 April 2019 (last day of Apr 2019) and those that end before 1 Apr 2019.  Consequently, to consider only events that have occurred in April 2019, the condition is that event start date <= 30 April 2019 and ends >= 1 Apr 2019.

3. **Task 3**: As the rating texts includes texts that are of other languages, these are translated with the help of Google and categorised into the 5 given categories (Excellent, Very Good, Good, Average, Poor) unless the translated meaning for the text is ambiguous e.g. 'great' for 'Skvělé' (such text ratings are ignored).  
From the general statistics of aggregate rating for each rating text, the thresholds found are as follows:
    - Excellent: 4.5-5.0
    - Very Good: 4.0-4.4
    - Good: 3.5-3.9
    - Average: 2.5-3.4  
    - Poor: <2.5
