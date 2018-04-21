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
col_types = cols(benchmark = col_factor(levels = c(
"h2")), mode = col_factor(levels = c("native-sql",
"crochet-sql", "crochet"))))
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
    return(list(avg = mean(subset(data, benchmark == bm & mode == con)$time), var = sd(subset(data, benchmark == bm & mode == con)$time)))
}
buildTable = function(mode){
    t(sapply(levels(data$benchmark), simpleMean, con = mode))
}
buildAvgTable = function(mode){
    t(sapply(levels(data$benchmark), simpleMean, con = mode))
}

crijcb <- buildTable("crochet")
crij <- buildTable("crochet-sql")
normal <- buildAvgTable("native-sql")
allData <- merge(normal, crij, by = "row.names", all = TRUE, suffixes = c(".normal", ".crochet-no-checkpoint"))
row.names(allData) <- t(allData["Row.names"])
allData <- allData[, - 1]
# colnames(allData)[4] <- "ci0.crij"

allData <- merge(allData, crijcb, by = "row.names", all = TRUE, suffixes = c(".crochet-no-checkpoint", ".crochet-cb"))
row.names(allData) <- t(allData["Row.names"])
colnames(allData)[6] <- "avg.crochet"
colnames(allData)[7] <- "var.crochet"
allData <- allData[, - 1]
allData <- as.matrix(allData)
write.csv(allData, file = output)