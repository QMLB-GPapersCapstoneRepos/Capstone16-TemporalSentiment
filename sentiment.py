import csv
import random
import nltk
import tweet_features
import datetime

from bokeh.plotting import Figure, show, output_server
from bokeh.models import DatetimeTickFormatter
from math import pi
import pandas as pd
from bokeh.models.widgets import Select
from bokeh.models import ColumnDataSource, HBox, VBoxForm
from bokeh.io import curdoc


tweets = []
months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
count = 0

# read all tweets and labels
with open('data.csv', newline='', encoding='utf-8') as csvFile:
    reader = csv.reader(csvFile, delimiter=',', quotechar='"', escapechar='\\')
    for row in reader:
        if count != 0:
            date_array = row[3].split()
            date_month = months.get(date_array[1])
            date_time_array = date_array[3].split(':')
            date = datetime.datetime(year=int(date_array[5]), month=date_month, day=int(date_array[2]), hour=int(date_time_array[0]), minute=int(date_time_array[1]), second=int(date_time_array[2]))
            tweets.append([[row[4], row[1]], [row[0], date]])
        else:
            count = 1

# treat neutral and irrelevant the same
for t in tweets:
    if t[0][1] == 'irrelevant':
        t[0][1] = 'neutral'

# split into training and test sets
random.shuffle(tweets)
tweets_modified = [(t, s) for ((t, s), (i, time)) in tweets]
tweets_half = tweets[2500:]

fvecs = [(tweet_features.make_tweet_dict(t), s) for (t, s) in tweets_modified]
v_train = fvecs[:2500]
v_test = fvecs[2500:]

# train classifier
classifier = nltk.NaiveBayesClassifier.train(v_train)

print('\nAccuracy %f\n' % nltk.classify.accuracy(classifier, v_test))
print(classifier.show_most_informative_features(10))

# build confusion matrix over test set
test_truth = [s for (t, s) in v_test]
test_predict = [classifier.classify(t) for (t, s) in v_test]

print('Confusion Matrix')
print(nltk.ConfusionMatrix( test_truth, test_predict))
print((nltk.ConfusionMatrix( test_truth, test_predict).pretty_format(sort_by_count=True, show_percents=True, truncate=9)))

x = [time for ((t, s), (i, time)) in tweets_half]

# quantify sentiment results
test_predict_num = []
for value in test_predict:
    if value == 'positive':
        test_predict_num.append(1)
    elif value == 'negative':
        test_predict_num.append(-1)
    else:
        test_predict_num.append(0)

time_series = pd.Series(data=x)
time_series = pd.to_datetime(time_series)

#Create a pandas dataframe from results
dict_df = {'Time': x, 'Topic': [i for ((t, s), (i, time)) in tweets_half],
        'Tweet': [t for ((t, s), (i, time)) in tweets_half],
        'TrueSentiment': [s for ((t, s), (i, time)) in tweets_half],
        'PredictedSentiment': test_predict, 'NumericalPredictedSentiment': test_predict_num
        }

df = pd.DataFrame(dict_df, columns=['Time', 'Topic', 'Tweet', 'TrueSentiment', 'PredictedSentiment', 'NumericalPredictedSentiment'])

df['Time'] = pd.to_datetime(df['Time'])
df['Topic'].astype(str)
df['roundedHourTime'] = [datetime.datetime(year=r.year, month=r.month, day=r.day, hour=r.hour) for r in df['Time']]

#Save results for visualization
df.to_csv('data1.csv', encoding='utf-8')


#----------STATIC VISUALIZATION----------#

# Create Input controls
topics = Select(title="Topic", value="microsoft", width=200 ,options=["All", "apple", "microsoft", "google", "twitter"])

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[]))

plot = Figure(title="", plot_width=800, plot_height=600, toolbar_location=None)
plot.line(x="x", y="y", source=source)
plot.xaxis.formatter = DatetimeTickFormatter(formats=dict(
        hours=["%H, %d %B %Y"],
        days=["%H, %d %B %Y"],
        months=["%H, %d %B %Y"],
        years=["%H, %d %B %Y"],
    ))

plot.xaxis.major_label_orientation = pi/2

def update(attrname, old, new):
    df_updated = df.loc[df['Topic'] == topics.value]
    df_subset = df_updated[['roundedHourTime', 'NumericalPredictedSentiment']]
    df_binned = df_subset.groupby(['roundedHourTime']).mean()
    df_indexed = df_binned.reset_index()

    plot.xaxis.axis_label = "Time of day (by the hour)"
    plot.yaxis.axis_label = "Sentiment score"
    plot.title = "Sentiment of %s tweets" % topics.value

    source.data = dict(
        x=df_indexed['roundedHourTime'],
        y=df_indexed['NumericalPredictedSentiment']
    )

topics.on_change('value', update)
update(None, None, None)


# Set up layouts and add to document
inputs = VBoxForm(children=[topics])

curdoc().add_root(HBox(children=[inputs, plot], width=500))
