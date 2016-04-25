library(shiny)

library(data.table)
library(lubridate)
library(ggplot2)

data <- read.csv("C:/Users/Sugandha/PycharmProjects/SandersSentiment/dataNew.csv")
data <- data.table(data)
data[, X:=NULL, ]
#str(data)

#turn time from factor -> character -> r datetime
data[,roundedHourTime:=as.character(roundedHourTime),]
data[,roundedHourTime:=parse_date_time(roundedHourTime, 'm/d/y H!:M!'),]

# Define server logic required to draw a histogram
shinyServer(function(input, output) {

  # Expression that generates a histogram. The expression is
  # wrapped in a call to renderPlot to indicate that:
  #
  #  1) It is "reactive" and therefore should re-execute automatically
  #     when inputs change
  #  2) Its output type is a plot

  output$distPlot <- renderPlot({
    subdata <- data[Topic==input$topic,.(NumericalPredictedSentiment=mean(NumericalPredictedSentiment)),by=roundedHourTime]
    
    ggplot(subdata, aes(x=roundedHourTime, y=NumericalPredictedSentiment)) +
      geom_line(color="#4682B4", size=0.8) + theme(axis.title.x = element_text(colour = "#4682B4"),
                                                   axis.title.y = element_text(colour = "#4682B4"),text = element_text(size=15))
  })
})