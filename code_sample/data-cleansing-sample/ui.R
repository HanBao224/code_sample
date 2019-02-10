# File: ui.R (do not submit)
# Setting: CMU MSP 36611, Shiny Extra Credit Homework
# Author: H. Seltman
# Date: Dec. 8, 2017

# Goal: Explore polynomial regression vs. regression splines
# Users upload a data file and choose x and y variables ("d1.csv" and "d2.csv"
# are test files.)  One tab shows polynomial regression, one shows use of
# regression splines, and the third compares the final models.
# For polynomials, the user can choose the order of the polynomial.  For
# spline the number of knots is chosen.
# Output shows a fitted and observed value plot and a residual vs. fit plot.

library(shiny)
library(shinyjs, warn.conflicts=FALSE, quietly=TRUE)

fluidPage(
  useShinyjs(),
  titlePanel("Regression for Curves"),

  sidebarLayout(
    sidebarPanel(
      h4("Csv file and variables"),
      fileInput("fileinfo", "Upload csv file", accept="text/csv"),
      uiOutput("xDropdown"),
      uiOutput("yDropdown"),
      shinyjs::hidden(verbatimTextOutput("dataDetails"))
    ),
    
    mainPanel(
      tabsetPanel(
        tabPanel("Regression Splines",
          sidebarLayout(
            sidebarPanel(
              sliderInput("df", "degrees of freedom:", min=3, max=7, value=3, step=1)
            ),
            mainPanel(
              verbatimTextOutput("splineText")
            )
          ),
          fluidRow(column(6, plotOutput("splinePlot")),
                   column(6, plotOutput("splineResFit")))
        ),
        
        tabPanel("Polynomial Regression",
          sidebarLayout(
            sidebarPanel(
              sliderInput("degree", "Polynomial degree:", min=1, max=7, value=1,
                          step=1)
            ),
            mainPanel(
              verbatimTextOutput("polyText")
            )
          ),
          fluidRow(column(6, plotOutput("polyPlot")),
                   column(6, plotOutput("polyResFit")))
        ),
        
        tabPanel("Comparison",
          verbatimTextOutput("comparisons"),
          fluidRow(column(2, p("Spline:")),
                   column(2, actionButton("downDf", "Lower d.f.")),
                   column(2, actionButton("upDf", "Raise d.f."))),
          p(),
          fluidRow(column(2, p("Polynomial:")),
                   column(2, actionButton("downDeg", "Lower degree")),
                   column(2, actionButton("upDeg", "Raise degree")))
        )  # end "Comparison tabPanel
      )  # end tabsetPanel
    )  # end (main) Main Panel
  )  # end (main) sidebarLayout
)  # end fluidPage
