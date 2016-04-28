library(tm)
library(leaps)
library(pROC)
library(glmnet)
library(MASS)
library(dplyr)
library(car)
library(randomForest)
library(RTextTools)
library(tm)
library(RWeka)
library(RColorBrewer)
library(wordcloud)

# This file creates a logistic regression model for predicting counterfactuals
# based on the features we previously identified.

rm(list=ls())
dir <- "/Users/joeraso/Desktop/senior-design/python"
setwd(dir)

data <- read.csv("features.csv")

data$tweet <- as.character(data$tweet)
data$CF <- as.factor(data$CF)
data$ifMod <- as.factor(data$ifMod)
data$modIf <- as.factor(data$modIf)
data$wish <- as.factor(data$wish)
data$conjNorm <- as.factor(data$conjNorm)
data$modNorm <- as.factor(data$modNorm)
data$vbIn <- as.factor(data$vbIn)
data$mdHave <- as.factor(data$mdHave)

CF <- data[data$CF == 1,]

### GLM
data <- read.csv("features.csv")
fit <- glm(CF~ifMod + wish + modNorm + vbIn, data, family="binomial")
summary(fit)
fit.predict <- predict(fit, data, type="response")
fit.predict[fit.predict < 0.5] <- 0
fit.predict[fit.predict > 0.5] <- 1
results <- data.frame(data$tweet, data$CF, fit.predict)
sum(data$CF != fit.predict)


### Elastic net
X <- model.matrix(CF~., data)[,-1]
Y <- data$CF
set.seed(1)
fit.lasso <- cv.glmnet(X, Y, alpha=1, family="binomial", nfolds = 10)  
plot(fit.lasso)
lasso.predict <- predict(fit.lasso, X,  s="lambda.min", type="class")
sum(lasso.predict != data$CF)

results <- data.frame(data.all$tweet, data$CF, lasso.predict)
results[results[,2] == 1 & results[,3] != 1,1]
sum(results[,2] == 1 & results[,3] == 1) / sum(results[,2] == 1)


### Text mining - Create a word cloud
text <- read.csv("/Users/joeraso/Desktop/counterfactual_messages.csv")
text <- CF$tweet
mycorpus1 <- VCorpus( VectorSource(text))
mycorpus1<- tm_map(mycorpus1, removeWords, stopwords("english"))


dtm1 <- DocumentTermMatrix(mycorpus1)
dtm.10.2 <- removeSparseTerms(dtm1, .99)
colnames(dtm.10.2)

threshold=.01*length(mycorpus1)
words.10 <- findFreqTerms(dtm1, lowfreq=1600)
words.10

colnames(dtm1)
freqs <- c()
cols <- colnames(dtm1)
for (i in 1:795) {
  freqs[i] <- (sum(as.matrix(dtm1[,i])))
}

val <- data.frame(freqs, cols)
cor.special=brewer.pal(8,"Dark2")  
wordcloud(val$cols, val$freqs, colors=cor.special, ordered.colors=F)
write.table(results, file = "results.csv", append = FALSE, quote=FALSE, sep=",", row.names=FALSE)

