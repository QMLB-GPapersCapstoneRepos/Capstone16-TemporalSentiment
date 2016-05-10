# Capstone16-TemporalSentiment

##How to run the app:
Downlowd all the source files into one directory, and open up RStudio. Create a project within RStudio, and add the server.R and ui.R files, making sure that the data file the two programs reference is in the correct place. 
Then simply run the app in RStudio, which will open up a browser displaying the sentiment tool.

...

##Results:
Running a naïve bayes classifier yielded an accuracy of 80% on average, whereas running a decision tree classifier from the NLTK library only yielded an accuracy of 73.7% on average. Multiple runs confirmed that naïve bayes performed better than decision trees. This is because simple decision trees tend to over fit the training data, which means that one has to employ sophisticated tree pruning techniques in order to improve the model. A confusion matrix showing the results in depicted in the figure below.

To gain a little more insight into the results, one can see the list of the most informative features used in any particular run through NLTK tools. The figrue below shows a list of such informative features for a particular run.

The predictions from the naïve bayes classifier were then fed into an R program where a server application was created that showed the sentiment over time for the four topics present in the dataset, depending on which topic was chosen from the interactive UI dropdown menu. The following four figures show the sentiment-time graph for the four topics in the dataset used. The results for Twitter and Google are strange due to the limited number of data records present. Twitter data for only given for a two hour window, out of which most of them were neutral, which is why the graph shows 0 as the sentiment from 2:00 to 3:00 am.
