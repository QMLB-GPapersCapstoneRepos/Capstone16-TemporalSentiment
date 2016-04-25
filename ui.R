library(shiny)

# Define UI for application that draws a histogram
shinyUI(fluidPage(

  # Application title
  titlePanel("Sentiment Analysis!"),

  # Sidebar with a slider input for the number of bins
  sidebarLayout(
    sidebarPanel(
      selectInput("topic",
                  label="Select a topic",
                  choices=list("Apple"="apple", "Google"="google",
                               "Twitter"="twitter", "Microsoft"="microsoft"),      
                  selected="apple")
    ),

    # Show a plot of the generated distribution
    mainPanel(
      plotOutput("distPlot")
    )
  )
))