library(readr)
require(mratios)

args = commandArgs(trailingOnly = TRUE)

fileName <- "ftp.csv"
output <- "ftp_table.csv"
if (length(args) == 2) {
    fileName <- args[1]
    output <- args[2]
}

ftp <- read_csv(fileName, col_types = cols(config = col_factor(levels = c("crochet-baseline",
"native", "restart", "crochet"))))

simpleMean = function(con)
{
    if (nrow(subset(ftp, config == con)) >= 10) {
        ret <- t.test(subset(ftp, config == con)$elapsed)
        return(t(list(avg = ret$estimate, ci0 = ret$conf.int[1], ci1 = ret$conf.int[2],
        slowAvg = 0, slowCi0 = 0, slowCI1 = 0
        )))
    }
    else {
        return(t(list(avg = mean(subset(ftp, config == con)$elapsed), ci0 = 0, ci1 = 0,
        slowAvg = 0, slowCi0 = 0, slowCI1 = 0
        )))
    }
}

calcMean = function(con){
    if (nrow(subset(ftp, config == con)) >= 10) {
        ret <- t.test.ratio(x = subset(ftp, (config == con))$elapsed, y = subset(ftp, (config == "native"))$elapsed)
        ret2 <- t.test(subset(ftp, config == con)$elapsed)

        return(t(list(
        avg = as.numeric(ret2$estimate),
        ci0 = as.numeric(ret2$conf.int[1]),
        ci1 = as.numeric(ret2$conf.int[2]),
        slowAvg = as.numeric(ret$estimate[3]),
        slowCi0 = as.numeric(ret$conf.int[1]),
        slowCi1 = as.numeric(ret$conf.int[2])
        )))
    }
    else {
        return(t(list(
        avg = mean(subset(ftp, config == con)$elapsed), ci0 = 0, ci1 = 0,
        slowAvg = mean(subset(ftp, config == con)$elapsed)/mean(subset(ftp, config == "native")$elapsed), slowCi0 = 0, slowCI1 = 0
        )))
    }
}

native <- simpleMean("native")
row.names(native) <- c("native")

cb <- calcMean("crochet-baseline")
row.names(cb) <- c("crochet-baseline")
crochet <- calcMean("crochet")
row.names(crochet) <- c("crochet")
restart <- calcMean("restart")
row.names(restart) <- c("restart")
all <- rbind(native, cb, crochet, restart)
all <- as.matrix(all)
write.csv(all, file = output)