x <- c(1, 3, 5, 7, 9, 6, 4, 2, 1, 4, 7, 9)
y <- append(2*x[-1], 3)

print(cor.test(y, x)$estimate)

sma <- function(x, h) {
  temp <- c(0,cumsum(x))
  res <- (temp[(h+1):length(temp)] - temp[1:(length(temp) - h)]) / h
  return(res)
}
window <- 3
x_ma <- sma(x, h=window)
y_ma <- sma(y, h=window)
print(cor.test(y_ma, x_ma)$estimate)

############################################
# 1D-timeframe correlations

get_path <- function(filename){
  PATH <- getwd()
  PATH <- substring(PATH, 1, nchar(PATH) - 2)
  PATH <- paste(PATH,"/data/",filename, sep="")
  return(PATH)
}

df_btc <- read.csv(
  get_path("Binance_BTCUSDT_1d_1 Jan, 2019-1 Mar, 2019.csv"), 
  sep='\t')
df_eth <- read.csv(
  get_path("Binance_ETHUSDT_1d_1 Jan, 2019-1 Mar, 2019.csv"), 
  sep='\t')
df_xrp <- read.csv(
  get_path("Binance_XRPUSDT_1d_1 Jan, 2019-1 Mar, 2019.csv"), 
  sep='\t')
df_eos <- read.csv(
  get_path("Binance_EOSUSDT_1d_1 Jan, 2019-1 Mar, 2019.csv"), 
  sep='\t')
df_xlm <- read.csv(
  get_path("Binance_XLMUSDT_1d_1 Jan, 2019-1 Mar, 2019.csv"), 
  sep='\t')

cor.test(df_btc$volume, df_eth$volume, method="spearman")$estimate
cor.test(df_btc$volume, df_xrp$volume, method="spearman")$estimate
cor.test(df_btc$volume, df_eos$volume, method="spearman")$estimate
cor.test(df_btc$volume, df_xlm$volume, method="spearman")$estimate
#'spearman' because correlation can be nonlinear

cor.test(df_btc$close, df_eth$close, method="spearman")$estimate
cor.test(df_btc$close, df_xrp$close, method="spearman")$estimate
cor.test(df_btc$close, df_eos$close, method="spearman")$estimate
cor.test(df_btc$close, df_xlm$close, method="spearman")$estimate

############################################
# Changes correlations
options(warn=-1)
df_changes <- data.frame(df_btc$open.time)
colnames(df_changes) <- "date"
df_changes$btc <- round(df_btc$close/df_btc$open * 100 - 100, digits = 2)
df_changes$eth <- round(df_eth$close/df_eth$open * 100 - 100, digits = 2)
df_changes$xrp <- round(df_xrp$close/df_xrp$open * 100 - 100, digits = 2)
df_changes$eos <- round(df_eos$close/df_eos$open * 100 - 100, digits = 2)
df_changes$xlm <- round(df_xlm$close/df_xlm$open * 100 - 100, digits = 2)

#'theoretical' leverage relatively to btc
get_leverage <- function(x, y){
  return(round(y/x, 1))
}
df_changes$l_eth <- get_leverage(df_changes$btc, df_changes$eth)
df_changes$l_xrp <- get_leverage(df_changes$btc, df_changes$xrp)
df_changes$l_eos <- get_leverage(df_changes$btc, df_changes$eos)
df_changes$l_xlm <- get_leverage(df_changes$btc, df_changes$xlm)

# btc_changes ~ %currency%_changes correlation
cor.test(df_changes$btc, df_changes$eth, method="spearman")$estimate
cor.test(df_changes$btc, df_changes$xrp, method="spearman")$estimate
cor.test(df_changes$btc, df_changes$eos, method="spearman")$estimate
cor.test(df_changes$btc, df_changes$xlm, method="spearman")$estimate

#volatility
cat(round(mean(abs(df_changes$btc)), 2), '%', sep='')
cat(round(mean(abs(df_changes$eth)), 2), '%', sep='')
cat(round(mean(abs(df_changes$xrp)), 2), '%', sep='')
cat(round(mean(abs(df_changes$eos)), 2), '%', sep='')
cat(round(mean(abs(df_changes$xlm)), 2), '%', sep='')
