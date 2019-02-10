# File: server.R
# Setting: CMU MSP 36611, Shiny Extra Credit Homework
# Author: Han Bao
# Date:18/12/2017

# Goal: Explore polynomial regression vs. regression splines
# Users upload a data file and choose x and y variables ("d1.csv" and "d2.csv"
# are test files.)  One tab shows polynomial regression, one shows use of
# regression splines, and the third compares the final models.
# For polynomials, the user can choose the order of the polynomial.  For
# spline the degrees of freedom (df) is chosen.
# Output shows a fitted and observed value plot and a residual vs. fit plot.
# The comparison tab compares the models, showing df and order, as well as
# BICs.  (Note that BIC is calculated as AIC(model, k=log(n)).)  The
# comparison tab has buttons to change the df and order.

library(shiny)
library(shinyjs)
require(splines)  # for bs()

# Main server function
function(input, output, session) {
  ### Reactive functions ###

  # Make a data.frame from the chosen file's contents.  Discard
  # non-numeric variables.  If read.csv() fails return a string
  # with the error message.  If there are not at least two numeric
  # variables, return a string with that message.  Otherwise,
  # return the data.frame.
  dataset = reactive({
    fileinfo = input$fileinfo
    req(fileinfo)
    dtf = try(read.csv(fileinfo$datapath))
    if (is(dtf, "try-error")) 
      return(as.character(attr(dtf, "condition")))
    dtf = dtf[, sapply(dtf, is.numeric), drop=FALSE]
    if (ncol(dtf) < 2) return("2 numeric variables required")
    dtf
  })

  # Write a reactive expression (function) to return a 2-column
  # data.frame containing only the specified columns, with column
  # names set to "x" and "y".  If x and y are the same, return
  # the string "'x' and 'y' must differ".
  xyDataset = reactive({
    dtf = dataset()
    x = input$xvar
    y = input$yvar
    req(dtf, x, y)
    if (x == y)
      return("variabels should differ")
    data = data.frame(dtf[,x], dtf[,y])
    colnames(data) = c("x", "y")
    data
  })
  
  # Perform spline regression of y on x with a regression spline of
  # the specified degrees of freedom
  splineReg = reactive({
    dtf = xyDataset()
    df = input$df
    if (is.character(dtf)) return(dtf)  # x/y differ message
    req(dtf, df, is.data.frame(dtf))
    formula = paste0("y ~ bs(x, df=", df, ")", sep="")
    rslt = try(lm(formula, data=dtf), silent=TRUE)
    if (is(rslt, "try-error")) 
      return(as.character(attr(rslt, "condition")))
    return(rslt)
  })
  

  # Write a reactive to mirror splineReg(), but for polynomial
  # regression
  polyReg = reactive({
    dtf = xyDataset()
    degree = input$degree
    if (is.character(dtf)) return(dtf)  # x/y differ message
    req(dtf, degree, is.data.frame(dtf))
    formula = paste0("y ~ poly(x, degree=", degree,")", sep="")
    rslt = try(lm(formula, data=dtf), silent=TRUE)
    if (is(rslt, "try-error")) 
      return(as.character(attr(rslt, "condition")))
    return(rslt)
  })
  
  ### Widget manipulation ###

  # In the "xDropdown" position of the UI, insert a "selectInput"
  # dropdown box called "xvar" that contains the variable names of
  # the current dataset, and defaults to the first variable.
  output$xDropdown = renderUI(selectInput("xvar", "Select 'x' variable",
                                          choices=names(dataset())))

  # Write code to create "yvar" in the "yDropdown" positions.  Default to
  # the second variable.
  output$yDropdown = renderUI(selectInput("yvar", "Select 'y' variable",
                                          choices=names(dataset())))
  
  # Allow user to change the spline df from the "comparison" tab
  # using push buttons.
  observeEvent(input$downDf, {
    df = input$df
    updateSliderInput(session, "df", value=df-1)
  })
  
  observeEvent(input$upDf, {
    df = input$df
    updateSliderInput(session, "df", value=df+1)
  })
  
  # Write code to allow the user to change the polynomial degree from
  # the "comparison" tab using push buttons.
  observeEvent(input$downDeg, {
    degree = input$degree
    updateSliderInput(session, "degree", value=degree-1)
  })
  
  observeEvent(input$upDeg, {
    degree = input$degree
    updateSliderInput(session, "degree", value=degree+1)
  })
  
  # Unhide the "dataDetails" if an xyDataset() is available.
  # Re-hide it if xyDataset() becomes unavailable, e.g., a
  # dataset with <2 numeric variables is loaded
  
  observe({
    dtf = xyDataset()
    if (is.character(dtf))
      shinyjs::hide("dataDetails")
    else
      shinyjs::show("dataDetails")
  })
  
  ### Rendering ###
  output$dataDetails = renderPrint({
    dataset = dataset()
    validate(need(dataset, "no dataset loaded yet"))
    validate(need(is.data.frame(dataset), dataset))
    cat(nrow(dataset), "rows and", ncol(dataset), "columns\n")
  })
  
  output$splineText = renderPrint({
    m = splineReg()
    validate(need(m, "no dataset loaded yet"))
    validate(need(is(m, "lm"), m))
    df = input$df
    cat("Regression spline with", df, "df:\n")
    print(coef(summary(m)))
  })
  
  output$splinePlot = renderPlot({
    m = splineReg()
    validate(need(m, "no dataset loaded yet"))
    validate(need(is(m, "lm"), m))
    dtf = xyDataset()
    with(dtf, plot(y ~ x, pch=16,
                   main=paste0("Observed and Fitted Plot for df=", input$df)))
    Seq = seq(min(dtf$x), max(dtf$x), length.out=100)
    fake = data.frame(x=Seq)
    fit = suppressWarnings(predict(m, fake))
    lines(Seq, fit, col=2)
  })

  output$splineResFit = renderPlot({
    m = splineReg()
    validate(need(m, "no dataset loaded yet"))
    validate(need(is(m, "lm"), m))
    plot(resid(m) ~ fitted(m), xlab="Fitted", ylab="Residual", pch=16,
         main=paste0("Residual vs. Fit for df=", input$df))
    abline(h=0, col="gray")
  })
  
  output$polyText = renderPrint({
    m = polyReg()
    validate(need(m, "no dataset loaded yet"))
    validate(need(is(m, "lm"), m))
    d = input$degree
    cat("Polynomial regrssion with degree", d, ":\n", sep="")
    print(coef(summary(m)))
  })
  
  output$polyPlot = renderPlot({
    m = polyReg()
    validate(need(m, "no dataset loaded yet"))
    validate(need(is(m, "lm"), m))
    dtf = xyDataset()
    with(dtf, plot(y ~ x, pch=16,
                   main=paste0("Observed and Fitted Plot for degree=", input$degree)))
    Seq = seq(min(dtf$x), max(dtf$x), length.out=100)
    fake = data.frame(x=Seq)
    fit = suppressWarnings(predict(m, fake))
    lines(Seq, fit, col=2)
  })
  
  output$polyResFit = renderPlot({
    m = polyReg()
    validate(need(m, "no dataset loaded yet"))
    validate(need(is(m, "lm"), m))
    plot(resid(m) ~ fitted(m), xlab="Fitted", ylab="Residual", pch=16,
         main=paste0("Residual vs. Fit for degree=", input$degree))
    abline(h=0, col="gray")
  })
  

  output$comparisons = renderPrint({
    splineReg = splineReg()
    polyReg = polyReg()
    validate(need(splineReg, polyReg, "nothing to compare"))
    validate(need(is(splineReg, "lm"), splineReg))
    validate(need(is(polyReg, "lm"), polyReg))
    cat("Compare Spline to Polynomial\n")
    cat("Sample size =", nrow(xyDataset()), "\n")
    cat("Spline df =", input$df, "polynomial degree =", input$degree, "\n")
    cat("Parameter count:", length(splineReg$coefficients), "vs.",
        length(polyReg$coefficients), "\n")
    logn = log(length(polyReg$residuals))
    cat("BICs: ", round(AIC(splineReg, k=logn), digits=1), "vs.", 
        round(AIC(polyReg, k=logn), digits=1), "\n")
  })
} # end server function
