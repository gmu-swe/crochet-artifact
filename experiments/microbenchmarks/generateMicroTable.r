library(readr)
require(mratios)

args = commandArgs(trailingOnly = TRUE)

fileName <- "micro.csv"
output <- "micro_table.csv"
if (length(args) == 2) {
    fileName <- args[1]
    output <- args[2]
}

data <- read_csv(fileName, col_types = cols(benchmark = col_factor(levels = c("ConcurrentHashMap 10",
"ConcurrentHashMap 25", "ConcurrentHashMap 50",
"ConcurrentHashMap 100", "HashMap 10",
"HashMap 25", "HashMap 50", "HashMap 100",
"LinkedHashMap 10", "LinkedHashMap 25",
"LinkedHashMap 50", "LinkedHashMap 100",
"TreeMap 10", "TreeMap 25", "TreeMap 50",
"TreeMap 100")), mode = col_factor(levels = c(
"check-no-sum-crochet",
"check-no-sum-serial",
"check-sum-criu",
"check-sum-crochet",
"check-sum-mapcloner",
"check-sum-serial",
"no-check-no-sum-crochet",
"no-check-no-sum-native",
"no-check-sum-crochet",
"no-check-sum-native"
))))


fieller = function(x, y) {
    x.mean = mean(x)
    y.mean = mean(y)
    x.sd = sd(x)
    y.sd = sd(y)
    xy.cov = cov(x, y)

    print(sprintf("x has mean %s, y has mean %s", x.mean, y.mean))
    print(sprintf("ratio of means is %s", x.mean / y.mean))

    g = pt(.05, length(y) - 1) ^ 2 * (y.sd ^ 2) / (y.mean ^ 2)

    lower = (1 / (1 - g)) * ((x.mean / y.mean) -
        g * xy.cov / (y.sd ^ 2) -
        pt(.05, length(y) - 1) / y.mean * sqrt (x.sd ^ 2 - 2 * x.mean / y.mean * xy.cov + x.mean ^ 2 / y.mean ^ 2 * y.sd ^ 2 - g * (x.sd ^ 2 - xy.cov ^ 2 / y.sd ^ 2)))
    upper = (1 / (1 - g)) * ((x.mean / y.mean) - g * xy.cov / (y.sd ^ 2) + pt(.05, length(y) - 1) / y.mean * sqrt (x.sd ^ 2 - 2 * x.mean / y.mean * xy.cov + x.mean ^ 2 / y.mean ^ 2 * y.sd ^ 2 - g * (x.sd ^ 2 - xy.cov ^ 2 / y.sd ^ 2)))
    list(lower, upper)
}
simpleMean = function(bm, con)
{
    if (nrow(subset(data, benchmark == bm & mode == con)) > 0) {
        ret <- t.test(subset(data, benchmark == bm & mode == con)$time)
        return(list(avg = ret$estimate/1000000, ci0 = ret$conf.int[1]/1000000, ci1 = ret$conf.int[2]/1000000))
    }else {
        return(list(ci0 = 0, ci1 = 0, avg = 0))
    }
}
calcMean = function(bm, con){
    if (nrow(subset(data, benchmark == bm & mode == con)) > 0) {
        ret <- t.test.ratio(x = subset(data, benchmark == bm & (mode == con))$time, y = subset(data, benchmark == bm & (mode == "no-check-sum-native"))$time)
        return(list(avg = as.numeric(ret$estimate[3]), ci0 = as.numeric(ret$conf.int[1]), ci1 = as.numeric(ret$conf.int[2])))
    }
    else {
        return(list(ci0 = 0, ci1 = 0, avg = 0))
    }
}
buildTable = function(mode){
    t(sapply(levels(data$benchmark), calcMean, con = mode))
}
buildAvgTable = function(mode){
    t(sapply(levels(data$benchmark), simpleMean, con = mode))
}

normal <- buildAvgTable("no-check-sum-native")

crij <- buildTable("no-check-sum-crochet")
crijcb <- buildTable("check-sum-crochet")
cloner <- buildTable("check-sum-cloner")
criu <- buildTable("check-sum-criu")

allData <- merge(normal, crij, by = "row.names", all = TRUE, suffixes = c(".normal", ".crij"))
row.names(allData) <- t(allData["Row.names"])
allData <- allData[, - 1]
colnames(allData)[4] <- "avg.crij"
colnames(allData)[5] <- "ci0.crij"
colnames(allData)[6] <- "ci1.crij"

allData <- merge(allData, crijcb, by = "row.names", all = TRUE, suffixes = c(".crij", ".crijcb"))
row.names(allData) <- t(allData["Row.names"])
allData <- allData[, - 1]
allData <- merge(allData, cloner, all = TRUE, by = "row.names", suffixes = c(".crijcb", ".cloner"))
row.names(allData) <- t(allData["Row.names"])
allData <- allData[, - 1]
allData <- merge(allData, criu, all = TRUE, by = "row.names", suffixes = c(".cloner", ".criu"))
row.names(allData) <- t(allData["Row.names"])
allData <- allData[, - 1]
allData <- as.matrix(allData)

write.csv(allData, file = output)