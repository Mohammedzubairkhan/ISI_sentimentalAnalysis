Sentimental Analysis is carried out in two methods. 

Method 1: textblob module (ML)

Method 2: LSTM (DL)

To install dependencies
pip install -r requirements.txt

Notes

1.Analysis of both the methods are presented individually in Summary_sentimental.pdf


2. The scrapped data is present in data.json and its respective code is in sentimental_analysis_textblob.py/ipynb


3. .py and .ipynb files are present for both the methods


4. To run textblob
python sentimental_analysis_textblob.py
(Open sentimental_analysis_textblob.ipynb in jupyter notebook if needed)
Execution time: ~170sec

5. To run LSTM
A. The code first trains the network internally and then uses its weights and biasis to analyze the statement
B. The network is trained on Tweets.csv(Airline review data)
Execution time: ~320sec (Training + Prediciton)

python sentimental_analysis_LSTM.py
(Open sentimental_analysis_LSTM.ipynb in jupyter notebook if needed)

6. Results
A. Screenshot of textblob
Folder 1: polarity_textBLOB
Folder 2: subjectivity_textBLOB

B. Screenshot of LSTM
Folder 1: lstm_Screenshot
