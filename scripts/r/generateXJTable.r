library(readr)
require(mratios)

xj <- read_csv("xj.csv", col_types = cols(config = col_factor(levels = c("xj.log", 
                                                                         "crochet-xj.log", "crochet.log", "native.log", "native-xj.log"))))
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
write.csv(all,file="xj-res.csv")
