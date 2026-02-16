# multi-language/r/ucd.R
ucd_analyze <- function(data) {
  if (nrow(data) > 1) {
    corr_mat <- abs(cor(t(data)))
    C <- (sum(corr_mat) - nrow(data)) / (nrow(data) * (nrow(data) - 1))
  } else {
    C <- 0.5
  }
  F <- 1.0 - C
  return(list(C = C, F = F, conservation = (abs(C + F - 1.0) < 1e-10)))
}

data <- matrix(c(1,2,3,4, 2,3,4,5, 5,6,7,8), nrow=3, byrow=TRUE)
print(ucd_analyze(data))
