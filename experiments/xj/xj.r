library(readr)
require(mratios)
# crochet-xj.csv
# crochet.csv
# native-xj.csv
# native.csv
# xj.csv

xj <- read_csv("xj.csv")
native <- read_csv("native.csv")
nativexj <- read_csv("native-xj.csv")
crochet <- read_csv("crochet.csv")
crochetxj <- read_csv("crochet-xj.csv")
xj$mode <- 'xj.log'
native$mode <- 'native.log'
nativexj$mode <- 'native-xj.log'
crochet$mode <- 'crochet.log'
crochetxj$mode <- 'crochet-xj.log'

xj <- rbind(xj,native)
xj <- rbind(xj,nativexj)
xj <- rbind(xj,crochet)
xj <- rbind(xj,crochetxj)
xj$bm<-sub("[^-]+-(.*)","\\1",xj$config)

xj$config<-xj$mode


# View(xj)

simpleMean =function(con)
{
  ret<- t.test(subset(xj,config==con)$new_throughput)
  return(t(list(avg=ret$estimate,ci0=ret$conf.int[1],ci1=ret$conf.int[2])))
}

calcMean=function(con){
  ret <- t.test.ratio(x=subset(xj,(config==con))$new_throughput,y=subset(xj,(config=="native.log"))$new_throughput)

  return(t(list(
    avg=as.numeric(ret$estimate[3]),
    ci0=as.numeric(ret$conf.int[1]),
    ci1=as.numeric(ret$conf.int[2])
    )))
}

calcMeanxj=function(con){
  ret <- t.test.ratio(x=subset(xj,(config==con))$new_throughput,y=subset(xj,(config=="native-xj.log"))$new_throughput)
  
  return(t(list(
    avg=as.numeric(ret$estimate[3]),
    ci0=as.numeric(ret$conf.int[1]),
    ci1=as.numeric(ret$conf.int[2])
  )))
}

native <- simpleMean("native.log")
native<-merge(native,calcMean("crochet.log"), by = "row.names", all = TRUE, suffixes=c(".normal",".crochet"))
native<-native[,-1]
native<-merge(native,calcMean("crochet.log"), by = "row.names", all = TRUE, suffixes=c(".crochet",".xj"))
native<-native[,-1]
row.names(native) <- c("native")

xjd <- simpleMean("native-xj.log")
xjd<-merge(xjd,calcMeanxj("crochet-xj.log"), by = "row.names", all = TRUE, suffixes=c(".normal",".crochet"))
xjd<-xjd[,-1]
xjd<-merge(xjd,calcMeanxj("xj.log"), by = "row.names", all = TRUE, suffixes=c(".crochet",".xj"))
xjd<-xjd[,-1]
row.names(xjd) <- c("xj")
all <- rbind(native,xjd)
all<-as.matrix(all)
write.csv(all,file="xj-out.csv")
