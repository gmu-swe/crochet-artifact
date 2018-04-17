library(readr)
require(mratios)
args = commandArgs(trailingOnly = TRUE)

fileName <- "stm.csv"
output <- "stm_table.csv"
if (length(args) == 2) {
    fileName <- args[1]
    output <- args[2]
}

stm <- read_csv(fileName, col_types = cols(
    config = col_factor(levels = c("native-nolock-jdk7", "native-nolock-jdk8","deuce-lsa-notx", 
        "deuce-tl2", "deuce-tl2-notx", "deuce-tl2-checkpoint", 
        "crochet-nolock", "deuce-lsa",  
        "jvstm-notx", "jvstm", "deuce-lsa-checkpoint", 
        "jvstm-checkpoint", "crochet-nolock-checkpoint"
       ))))
simpleMean =function(con)
{
  ret<- t.test(subset(stm,config==con)$n)
  return(t(list(avg=ret$estimate,ci0=ret$conf.int[1],ci1=ret$conf.int[2])))
}

calcMean7=function(con){
  ret <- t.test.ratio(x=subset(stm,(config==con))$n,y=subset(stm,(config=="native-nolock-jdk7"))$n)
  return(t(list(avg=as.numeric(ret$estimate[3]), ci0=as.numeric(ret$conf.int[1]), ci1=as.numeric(ret$conf.int[2]))))
}
calcMean8=function(con){
  ret <- t.test.ratio(x=subset(stm,(config==con))$n,y=subset(stm,(config=="native-nolock-jdk8"))$n)
  return(t(list(avg=as.numeric(ret$estimate[3]),ci0=as.numeric(ret$conf.int[1]), ci1=as.numeric(ret$conf.int[2]))))
}

crochet<-simpleMean("native-nolock-jdk8")
crochet<-merge(crochet,calcMean8("crochet-nolock"), by = "row.names", all = TRUE, suffixes=c(".normal",".notx"))
crochet<-crochet[,-1]
crochet<-merge(crochet,calcMean8("crochet-nolock-checkpoint"), by = "row.names", all = TRUE, suffixes=c(".notx",".onetx"))
crochet<-crochet[,-1]
crochet<-merge(crochet,calcMean8("crochet-nolock-checkpoint"), by = "row.names", all = TRUE, suffixes=c(".onetx",".manytx"))
crochet<-crochet[,-1]
row.names(crochet) <- c("crochet")

deucetl2<-simpleMean("native-nolock-jdk7")
deucetl2<-merge(deucetl2,calcMean7("deuce-tl2-notx"), by = "row.names", all = TRUE, suffixes=c(".normal",".notx"))
deucetl2<-deucetl2[,-1]
deucetl2<-merge(deucetl2,calcMean7("deuce-tl2-checkpoint"), by = "row.names", all = TRUE, suffixes=c(".notx",".onetx"))
deucetl2<-deucetl2[,-1]
deucetl2<-merge(deucetl2,calcMean7("deuce-tl2"), by = "row.names", all = TRUE, suffixes=c(".onetx",".manytx"))
deucetl2<-deucetl2[,-1]
row.names(deucetl2) <- c("deuce-tl2")

deucelsa<-simpleMean("native-nolock-jdk7")
deucelsa<-merge(deucelsa,calcMean7("deuce-lsa-notx"), by = "row.names", all = TRUE, suffixes=c(".normal",".notx"))
deucelsa<-deucelsa[,-1]
deucelsa<-merge(deucelsa,calcMean7("deuce-lsa-checkpoint"), by = "row.names", all = TRUE, suffixes=c(".notx",".onetx"))
deucelsa<-deucelsa[,-1]
deucelsa<-merge(deucelsa,calcMean7("deuce-lsa"), by = "row.names", all = TRUE, suffixes=c(".onetx",".manytx"))
deucelsa<-deucelsa[,-1]
row.names(deucelsa) <- c("deuce-lsa")

jvstm<-simpleMean("native-nolock-jdk7")
jvstm<-merge(jvstm,calcMean7("jvstm-notx"), by = "row.names", all = TRUE, suffixes=c(".normal",".notx"))
jvstm<-jvstm[,-1]
jvstm<-merge(jvstm,calcMean7("jvstm-checkpoint"), by = "row.names", all = TRUE, suffixes=c(".notx",".onetx"))
jvstm<-jvstm[,-1]
jvstm<-merge(jvstm,calcMean7("jvstm"), by = "row.names", all = TRUE, suffixes=c(".onetx",".manytx"))
jvstm<-jvstm[,-1]
row.names(jvstm) <- c("jvstm")

all <- rbind(crochet,deucelsa,deucetl2,jvstm)
all<-as.matrix(all)
write.csv(all,file=output)