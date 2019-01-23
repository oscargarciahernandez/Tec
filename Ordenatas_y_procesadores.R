library(RSelenium)
library(here)
library(stringr)
library(lubridate)
library(rlist)
library(XML)


url<- "https://us.rebusfarm.net/en/tempbench?view=benchmark"

rD<- rsDriver(browser = "firefox",verbose = FALSE) 

remDr<- rD$client

remDr$navigate(url) 

setting_name<- function(ch_list){
  x<- which(nchar(ch_list)==1)
  if(length(x)!=1){
    x<- x[1]
  }
  name<- str_flatten(ch_list[1:x-1],"-")
  other<-ifelse(nchar(ch_list[x:length(ch_list)])==0,NA,ch_list[x:length(ch_list)])
  other<- other[complete.cases(other)]
  return(c(name,other))
}
lista_completa<- list()

for (pags in 1:45) {
  a<-remDr$findElements(using = "css selector",
                        value =".tablesorter")
  
  tabla<- a[[1]]$getElementText()
  tabla_1<- str_split(tabla,"\n")[[1]]
  tabla_2<- tabla_1[6:length(tabla_1)]
  tabla_3<- str_split(tabla_2, " ")
  

  lista_4<-lapply(tabla_3, setting_name)
  
  tabla_4<-as.data.frame(matrix(unlist(lista_4),byrow=T,ncol=8))
  colnames(tabla_4)<-c("name", "cpus",
                       "cores","ghz", 
                       "single11.5", "multi11.5",
                       "single15", "multi15")
  
  
  lista_completa[[pags]]<- tabla_4
  a<-  remDr$findElements(using = "css selector",
                          value =".next")
  remDr$executeScript("arguments[0].click();",a)
}

list.save(lista_completa,here::here('list_benchmark.Rdata'))






url<- "https://www.cpubenchmark.net/cpu_list.php"
rD<- rsDriver(browser = "firefox",verbose = FALSE) 
remDr$navigate(url)
html_sucio<-remDr$getPageSource()[[1]]
x<-readHTMLTable(htmlParse(html_sucio), rm_nodata_cols = F)
list.save(x,here::here('list_benchmark_2.Rdata'))






url<- "https://benchmarks.ul.com/compare/best-cpus"
remDr$navigate(url)
html_sucio<-remDr$getPageSource()[[1]]
x<-readHTMLTable(htmlParse(html_sucio), rm_nodata_cols = F)
list.save(x,here::here('list_benchmark_3.Rdata'))







url<- "https://www.cpu-monkey.com/es/cpu_benchmark-cinebench_r15_multi_core-8"
remDr$navigate(url)
html_sucio<-remDr$getPageSource()[[1]]
x<-readHTMLTable(htmlParse(html_sucio), rm_nodata_cols = F)
list.save(x,here::here('list_benchmark_4_multicore.Rdata'))




url<- "https://www.cpu-monkey.com/en/cpu_benchmark-cinebench_r15_single_core-7"
remDr$navigate(url)
html_sucio<-remDr$getPageSource()[[1]]
x<-readHTMLTable(htmlParse(html_sucio), rm_nodata_cols = F)
list.save(x,here::here('list_benchmark_4_singlecore.Rdata'))

