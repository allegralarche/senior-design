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


### n-gram
tagged <- read.csv("POSTagged.csv", header=FALSE, stringsAsFactors=FALSE)

oneGram <- tdm.generate(tagged, 1)
biGram <- tdm.generate(tagged, 2)
triGram <- tdm.generate(tagged,3)

oneGram.matrix <- as.matrix(oneGram)
biGram.matrix <- as.matrix(biGram)
triGram.matrix <- as.matrix(triGram)

findFreqTerms(oneGram, lowfreq = 100)
findFreqTerms(biGram, lowfreq= 100)
findFreqTerms(triGram, lowfreq = 100)

tdm.generate <- function(string, ng){
  
  # tutorial on rweka - http://tm.r-forge.r-project.org/faq.html
  
  corpus <- Corpus(VectorSource(string)) # create corpus for TM processing
  corpus <- tm_map(corpus, content_transformer(tolower))
  corpus <- tm_map(corpus, removeNumbers) 
  corpus <- tm_map(corpus, removePunctuation)
  corpus <- tm_map(corpus, stripWhitespace)
  # corpus <- tm_map(corpus, removeWords, stopwords("english")) 
  options(mc.cores=1) # http://stackoverflow.com/questions/17703553/bigrams-instead-of-single-words-in-termdocument-matrix-using-r-and-rweka/20251039#20251039
  BigramTokenizer <- function(x) NGramTokenizer(x, Weka_control(min = ng, max = ng)) # create n-grams
  tdm <- TermDocumentMatrix(corpus, control = list(tokenize = BigramTokenizer)) # create tdm from n-grams
  tdm
}



### GLM
data <- read.csv("features.csv")
fit <- glm(CF~ifMod + wish + modNorm + vbIn, data, family="binomial")
summary(fit)
fit.predict <- predict(fit, data, type="response")
fit.predict[fit.predict < 0.5] <- 0
fit.predict[fit.predict > 0.5] <- 1
results <- data.frame(data$tweet, data$CF, fit.predict)
#counterfactuals <- results[results$data.CF == "1",]
#notCF <- results[results$data.CF == "0",]
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


### Text mining
text <- CF$tweet
mycorpus1 <- VCorpus( VectorSource(text))


write.table(results, file = "results.csv", append = FALSE, quote=FALSE, sep=",", row.names=FALSE)

