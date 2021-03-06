library(RSelenium)
library(here)
library(stringr)
library(lubridate)
library(rlist)


url<- "https://www.electrobuzz.net/category/techno/"
fprof <- makeFirefoxProfile(list(browser.download.folderList="2",
                                 browser.download.manager.showWhenStarting= "false",
                                 browser.download.dir = "C:/titititit/Descargas/",
                                 browser.helperApps.neverAsk.saveToDisk = "application/zip"))
#remDr <- remoteDriver(extraCapabilities = fprof, browserName= "firefox")
 


rD<- rsDriver(browser = "firefox",verbose = FALSE,
              extraCapabilities = fprof) 

remDr<- rD$client

remDr$navigate(url) 


a<-remDr$findElements(using = "css selector",
                      value ="div:nth-child(1) > h2:nth-child(2) > a:nth-child(1)")



b<-sapply(a, function(x) x$getElementAttribute('href'))
#### En b tenemos guardada todos los linkks de la página. 
url2<- b[[1]]
rD2<- rsDriver(browser = "firefox",verbose = FALSE, extraCapabilities = fprof) 

remDr2<- rD2$client

remDr2$navigate(url2)

#pinchamos boton de download en cosmobox

remDr2$findElement(using = "css selector",
                      value ="a.dl-btn:nth-child(2)")$sendKeysToElement(list(key = "end"))


remDr2$findElement(using = "css selector",
                   value ="a.dl-btn:nth-child(2)")$sendKeysToElement(list(key = "down_arrow"))




remDr2$findElement(using = "css selector",
                   value ="a.dl-btn:nth-child(2)")$clickElement()

#dentro de cosmobox pinchamos descargar zip.

remDr2$findElement(using = "css selector",
                   value ="div.col-md-12:nth-child(10) > button:nth-child(1)")$clickElement()


# Login Cosmobox, una vez estamos dentro de cosmobox.org ------------------

login_cosmobox<- function(){
  remDr2$findElement(using = "css selector",
                     value =".zmdi-accounts-add")$clickElement()
  
  
  
  user<- remDr2$findElement(using = "css selector",
                            value ="div.form-group:nth-child(5) > div:nth-child(1) > input:nth-child(1)")
  
  user$clearElement()  
  user$sendKeysToElement(list("oscargarciahernandez"))
  pass<- remDr2$findElement(using = "css selector",
                            value ="div.form-group:nth-child(6) > div:nth-child(1) > input:nth-child(1)")
  
  pass$clearElement()  
  pass$sendKeysToElement(list("hernandez1"))
  remDr2$findElement(using = "css selector",
                     value =".btn-custom")$clickElement()
}


# Función_Sensors_ID's ----------------------------------------------------


#Función para obtener todos los id's de los sensores
#linkeados a nuestro telefono
Get_sensor_ID<- function(phoneid){
  
  
  url<- paste0("https://measurements.mobile-alerts.eu/Home/SensorsOverview?phoneid=",phoneid)
  rD<- rsDriver(browser = "firefox",verbose = FALSE) 
  
  remDr<- rD$client      
  remDr$navigate(url) 
  
  sensor_elem<-unlist(lapply(remDr$findElements(using = 'class name',
                                                value ="sensor-component"),
                             function(x) x$getElementText()))
  sensor_elem<- sensor_elem[str_detect(sensor_elem,"ID")]
  sensor_elem<- str_remove(sensor_elem,"ID\n")
  remDr$close()
  
  return(sensor_elem)
  
}




# Cojer informacion de la página ------------------------------------------

get_page_table<- function(remDR_selenium){
  remDr<- remDR_selenium
  tabla<- remDr$findElement(using = 'css selector', 
                            value = ".table > tbody:nth-child(2)")$getElementText() #
  
  split_newline<- str_split(tabla[[1]],pattern = "\n")      
  split_newline_matrix<- t(rbind(unlist(split_newline)))    
  lista_datos<-str_split(split_newline_matrix,pattern = " ") 
  matriz_datos<-matrix(unlist(lista_datos),ncol = 8,byrow = TRUE)      
  dataframe_datos<-as.data.frame(matriz_datos)                         
  dataframe_datos[,1]<-mdy_hms(paste(dataframe_datos[,1],dataframe_datos[,2],dataframe_datos[,3],sep = " "))  
  dataframe_datos<-dataframe_datos[,c(1,4,6,8)]                
  dataframe_datos[,4]<-as.character(dataframe_datos[,4])
  for (i in 1:length(dataframe_datos[,4])) {
    yy<-dataframe_datos[,4][i]
    dataframe_datos[i,5]<- ifelse(yy=="North", 0, ifelse(yy=="North-northeast",20,
                                                         ifelse(yy=="Northeast",45, ifelse(yy=="East-northeast",65,
                                                                                           ifelse(yy=="East", 90, 
                                                                                                  ifelse(yy=="East-southeast", 110,
                                                                                                         ifelse(yy=="Southeast", 135,
                                                                                                                ifelse(yy=="South-Southeast", 155, 
                                                                                                                       ifelse(yy=="South", 180, 
                                                                                                                              ifelse(yy=="South-southwest", 200, 
                                                                                                                                     ifelse(yy=="Southwest", 225,
                                                                                                                                            ifelse(yy=="West-southwest", 245, 
                                                                                                                                                   ifelse(yy=="West", 270, 
                                                                                                                                                          ifelse(yy=="West-northwest",290,
                                                                                                                                                                 ifelse(yy=="Northwest", 315,
                                                                                                                                                                        ifelse(yy=="North-northwest", 335, 
                                                                                                                                                                               ifelse(yy=='-31',NA)))))))))))))))))
  }
  colnames(dataframe_datos)<- c("Date","Mean","Max","Dir_ch","Dir_deg")   
  return(dataframe_datos)
  
}


# Función Get_Data --------------------------------------------------------
#La función Get_Data necesita que exista Datos_anemometros

Get_sensor_Data<- function(sensorID){
  
  url=paste0("https://measurements.mobile-alerts.eu/Home/MeasurementDetails?deviceid=",
             sensorID,
             "&vendorid=f193c634-2611-475b-ba7a-27b0ead33c6f&appbundle=eu.mobile_alerts.mobilealerts")
  
  rD<- rsDriver(browser = "firefox",verbose = FALSE) 
  remDr<- rD$client      
  remDr$navigate(url) 
  
  #Buscar en la lista los datos del anemometro correspondiente
  Datos_anemo<- Datos_anemometros[str_detect(names(Datos_anemometros),pattern=sensorID)]
  
  #Este es el periodo que queremos 
  fecha_ini1<- format(max(Datos_anemo[[1]]$Date),"%m/%d/%Y %I-%M-%S" )
  fecha_ini<- ifelse(pm(max(Datos_anemo[[1]]$Date)), paste0(fecha_ini1," PM"),paste0(fecha_ini1," AM"))
  fechainicio= fecha_ini
  fechafinal= format(Sys.Date()+1,"%m/%d/%Y")  
  
  
  #buscamos cajetines
  cajatexto_fechainicio=remDr$findElement(using = 'css selector', 
                                          value = "#from")  
  cajatexto_fechafinal=remDr$findElement(using = 'css selector',
                                         value = "#to")    
  
  #limpiamos cajetines porsiaca
  cajatexto_fechainicio$clearElement()  
  cajatexto_fechafinal$clearElement()  
  
  #Introducimos fechas
  cajatexto_fechainicio$sendKeysToElement(list(fechainicio))  
  cajatexto_fechafinal$sendKeysToElement(list(fechafinal))   
  
  
  
  #refresh baatonn¡
  remDr$findElement(using = 'css selector',
                    value = "button.btn:nth-child(9)")$clickElement()
  
  
  
  #Buscamos el boton de 250 elements por página y pulsamos
  remDr$findElement(using = 'css selector',
                    value = "label.btn:nth-child(3)")$clickElement()
  
  
  #Buscamos el boton refresh y pulsamos
  remDr$findElement(using = 'css selector',
                    value = "#pagesizebutton")$clickElement()
  
  
  #Buscamos última página buscando el boton de Skip-to-last
  #De esta manera podemos saber cuantas páginas 
  #habrá que recorrer con el bucle. 
  
  #Este if es capaz de diferenciar cuantas páginas hay
  #independientemente de si existe o no el botón skip to last.
  
  #Esto no creo que lo utilicemos, se puede hacer directamente 
  #con un bucle WHILE
  text_pag<-unlist(remDr$findElement(using = "css selector",value=".pagination")$getElementText())
  if(str_detect(text_pag, pattern = "»»")){
    url_last<- unlist(remDr$findElement(using = "css selector", value=".PagedList-skipToLast > a:nth-child(1)")$getElementAttribute('href'))
    numero_pags<- str_remove(str_extract(url_last,
                                         pattern = "page=[:digit:]+"),
                             "page=")
  }else{numero_pags<- max(as.numeric(unlist(str_extract_all(text_pag,pattern = "[:digit:]+"))))}
  
  
  #E aquí el bucle while del que hablaba
  data_frame_1<-get_page_table(remDr)
  data_frame<- data.frame()
  text_pag<-unlist(remDr$findElement(using = "css selector", 
                                     value=".pagination")$getElementText())
  while (str_detect(text_pag, pattern = "»")) {
    remDr$findElement(using = 'css selector',
                      value = ".PagedList-skipToNext > a:nth-child(1)")$clickElement()
    data_frame<- rbind(data_frame,get_page_table(remDr))
    
    
    text_pag<-unlist(remDr$findElement(using = "css selector", 
                                       value=".pagination")$getElementText())
    
  }
  
  
  
  data_frame<-rbind(data_frame,data_frame_1)
  data_frame<-data_frame[!data_frame$Date%in%Datos_anemo[[1]]$Date,]
  data_frame[,2]<- as.numeric(as.character(data_frame[,2]))
  data_frame[,3]<- as.numeric(as.character(data_frame[,3]))
  
  Tabla_actualizada<- rbind(data_frame, Datos_anemo[[1]])
  Tabla_actualizada<- Tabla_actualizada[order(Tabla_actualizada$Date,decreasing = TRUE),]
  remDr$close()
  
  return(Tabla_actualizada)
  
}



