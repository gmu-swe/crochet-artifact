library(readr)
require(mratios)

args = commandArgs(trailingOnly = TRUE)

fileName <- "data.csv"
output <- "dacapo_table.csv"
if (length(args) == 2) {
    fileName <- args[1]
    output <- args[2]
}


data <- read_csv(fileName,
col_types = cols(benchmark = col_factor(levels = c("avrora",
"batik", "eclipse", "fop", "jython", "h2"
, "luindex", "lusearch", "pmd",
"sunflow", "tomcat", "tradebeans", "tradesoap",
"xalan")), mode = col_factor(levels = c("native",
"crochet", "crochet-callback", "CRIU"))))
require(mratios)

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
    if (nrow(subset(data, benchmark == bm & mode == con)) >= 10) {
        ret <- t.test(subset(data, benchmark == bm & mode == con)$time)
        return(list(ci0 = ret$conf.int[1], ci1 = ret$conf.int[2], avg = ret$estimate))
    }
    else {
        if((nrow(subset(data, benchmark == bm & mode == con)) > 0))
        return(list(ci0 = 0, ci1 = 0, avg = mean(subset(data, benchmark == bm & mode == con)$time)))

        return(list(ci0 = 0, ci1 = 0, avg = 0))
    }
}
calcMean = function(bm, con){
    if (nrow(subset(data, benchmark == bm & mode == con)) >= 10
    && nrow(subset(data, benchmark == bm & mode == "native")) >= 10) {
        ret <- t.test.ratio(x = subset(data, benchmark == bm & mode == con)$time, y = subset(data, benchmark == bm & mode == "native")$time, base = 1, na.rm = TRUE)
        return(list(ci0 = as.numeric(ret$conf.int[1]), ci1 = as.numeric(ret$conf.int[2]), avg = as.numeric(ret$estimate[3])))
    }
    else
    {
        if (nrow(subset(data, benchmark == bm & mode == con))> 0
         && nrow(subset(data, benchmark == bm & mode == "native"))> 0) {
            return(list(ci0 = 0, ci1 = 0, avg = mean(subset(data, benchmark == bm & mode == con)$time)/mean(subset(data, benchmark == bm & mode == "native")$time)))
        }
        else
            return(list(ci0 = 0, ci1 = 0, avg = 0))
    }
}
buildTable = function(mode){
    t(sapply(levels(data$benchmark), calcMean, con = mode))
}
buildAvgTable = function(mode){
    t(sapply(levels(data$benchmark), simpleMean, con = mode))
}

criu <- buildTable("CRIU")
crij <- buildTable("crochet")
crijcb <- buildTable("crochet-callback")
normal <- buildAvgTable("native")
allData <- merge(normal, crij, by = "row.names", all = TRUE, suffixes = c(".normal", ".crij"))
row.names(allData) <- t(allData["Row.names"])
allData <- allData[, - 1]
colnames(allData)[4] <- "ci0.crij"
colnames(allData)[5] <- "ci1.crij"
colnames(allData)[6] <- "avg.crij"

allData <- merge(allData, crijcb, by = "row.names", all = TRUE, suffixes = c(".crij", ".crijcb"))
row.names(allData) <- t(allData["Row.names"])
allData <- allData[, - 1]
allData <- merge(allData, criu, all = TRUE, by = "row.names", suffixes = c(".crijcb", ".criu"))
row.names(allData) <- t(allData["Row.names"])
allData <- allData[, - 1]
allData <- as.matrix(allData)
write.csv(allData, file = output)