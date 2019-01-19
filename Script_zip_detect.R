library(stringr)
library(stringdist)
library(utils)


carpetas_ti<- list.dirs("c:/titititit/", recursive = F)

carpetas_unzip<- str_remove(carpetas_ti,pattern = "c:/titititit//")
carpetas_unzip<- str_remove(carpetas_unzip, pattern = "AA_")


#nos olvidamos de momento de los archivos .rar, no encuenro la manera de extraerlos
#rar_1<- str_remove(list.files("c:/titititit/",pattern = "rar"),pattern = ".rar")
#zip_1<-str_remove(list.files("c:/titititit/",pattern = "zip"),pattern = ".zip")
#carpetas_zip<- c(rar_1,zip_1)
carpetas_zip<- str_remove(list.files("c:/titititit/",pattern = "zip"),pattern = ".zip")


## Usamos agrep para ver cual es el más parecido
ziped_files<-vector()
vec_sim<-vector()
for (i in 1:length(carpetas_zip)) {
  unzip<- carpetas_unzip[agrep(carpetas_unzip,pattern = carpetas_zip[i])]
  zip<- carpetas_zip[i]
  if(length(stringsim(zip,unzip))==0){
    ziped_files[i]<- carpetas_zip[i]
  }else{
    vec_sim[i]<- stringsim(zip,unzip)
  }
}
ziped_files_vec<-carpetas_zip[!is.na(ziped_files)]
rm(unzip)

setwd("c:/titititit/")
for (i in 1:length(ziped_files_vec)) {
  unzip(paste0("c:/titititit/",ziped_files_vec[i],".zip"))
  
}

rm_file<-function(x){file.remove(paste0("c:/titititit/",x,".zip"))}
rm_file<-possibly(rm_file,otherwise = NA)



for (i in 1:length(carpetas_zip)) {
  rm_file(carpetas_zip[i])
  
  
}

