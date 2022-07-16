# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 18:40:36 2020

@author: Utilizador
"""

import matplotlib.image as mpimg
import numpy as np
import scipy.io.wavfile as spiowf
import matplotlib.pyplot as plt
import huffmancodec

def histograma(fonte, alfabeto):
    # Vai receber uma fonte de informação com um alfabeto e mostra o histograma de ocorrência dos seus símbolos
    ocorrencia=ocorrencias(fonte, alfabeto)
        
    plt.xlabel("Alfabeto")
    plt.ylabel("Número de Ocorrências")
    plt.bar(alfabeto, ocorrencia.values(), color='skyblue')    # Mostra o histograma -> no eixo dos Xx os símbolos do alfabeto e no eixo dos Yy o número de ocorrências destes na fonte
    

def ocorrencias(fonte, alfabeto):
    ocorrencias=dict()
    for alf in alfabeto:
        ocorrencias.update({alf:0})
    for i in fonte:
        if (i in ocorrencias.keys()):
            ocorrencias[i]+=1   
    return ocorrencias
      
def entropia(fonte, alfabeto):
    ocorrencia = ocorrencias(fonte, alfabeto)
    prob=probabilidade(ocorrencia)    
    entr=np.sum(prob*np.log2(1/prob))
  
    return entr
 
def probabilidade(ocorrencias):
    valores=np.array(list(ocorrencias.values()))
    valores = valores[valores>0]
    
    no_total=np.sum(valores)

    prob=valores/no_total
    return prob
    
def canais_img(img):
    if (len(img.shape)>2):
        img=img[:,:,0]
    return img

def canais_som(som):
    if (len(som.shape)>1):
        som=som[:,0]
    return som 
       
def alfa_txt():
    alfabeto=list()
    for i in range(ord('A'),ord('Z')+1):
        alfabeto.append(chr(i)) 
    for i in range(ord('a'),ord('z')+1):
        alfabeto.append(chr(i))    
    return alfabeto

def alfa_img_som():
    alfabeto=np.arange(0,256)
    return alfabeto


def mediabits_variancia(dados, prob):
    codec = huffmancodec.HuffmanCodec.from_data(dados)
    s, l = codec.get_code_len()  

    media = np.sum(prob * l)
    print("Média dos bits: ",media)
    
    var = np.sum(prob*((l-media)**2))
    print("Variância: ",var)
        
def entropiaPar(dados, alfabeto):
    elem = list()     
    alfabeto = np.array(alfabeto)

    for i in range (0, len(dados)-1 ,2):
        elem.append(str(dados[i]) +"/"+ str(dados[i+1]))
    
    entr=entropia(elem, alfabeto)
    entr=entr/2
    
    print("Entropia agrupada: ",entr)
    
def alfa_som_img_par():
    alfabeto = list()
    for i in range (256):
            for j in range(256):
                alfabeto.append(str(i)+"/"+str(j))
    return alfabeto
    
def alfa_txt_par(alfabeto_ant):
    novo=list()
    for i in range (len(alfabeto_ant)):
            for j in range(len(alfabeto_ant)):
                novo.append(str(alfabeto_ant[i])+"/"+str(alfabeto_ant[j]))
    return novo


def infoMutua(query, target, alfabeto, passo):
    
    janela = np.zeros(len(query), dtype='int')
    
    entr_query = entropia(query, alfabeto)
    
    Lista_infomutua = np.zeros(int(((len(target)-len(query))/passo)+1))
    
    alfab = list()
    
    for alfa in alfabeto:
        for alfa2 in alfabeto:
            alfab.append(str(alfa)+"/"+str(alfa2))
    
    for i in range(0, int(((len(target)-len(query))/passo)+1)):
        listaMutua=list()
        for j in range (len(query)):
            janela[j] = target[i*passo+j]
            listaMutua.append(str(janela[j])+"/"+str(query[j]))
            
        entr_conj = entropia(listaMutua,alfab)
        
        entr_janela = entropia(janela, alfabeto)
        Lista_infomutua[i] = entr_query + entr_janela - entr_conj    
          
    return Lista_infomutua
   
  
def leitura_img(file):
    print(file)
    plt.title(file)
    img=mpimg.imread(file)
    img=canais_img(img)
    img = img.flatten()
    histograma(img, alfa_img_som())
    entr = entropia(img, alfa_img_som())
    print("Entropia: ",entr)
    prob=probabilidade(ocorrencias(img, alfa_img_som()))
    mediabits_variancia(img, prob)
    entropiaPar(img, alfa_som_img_par())
    
    print("---------------------------------------------")
    

if __name__ == "__main__":
    
    fonte = [0, 0, 3, 0, 1, 0, 2, 3]
    alfabeto = [0, 1, 2, 3, 4, 5, 10]
    
    #----Ex01-----
    histograma(fonte, alfabeto)
    
    #----Ex02-----
    entr = entropia(fonte, alfabeto)  
    print("Entropia: ",entr)
    print("---------------------------------------------")
    
    
    #----Ex03 / Ex04 / Ex05-----
    
    plt.subplot(3, 2, 1)
    file="lena.bmp"
    leitura_img(file)
    
    plt.subplot(3, 2, 2)
    file="CT1.bmp"
    leitura_img(file)
    
    plt.subplot(3, 2, 3)
    file="binaria.bmp"
    leitura_img(file)
    
    plt.subplot(3, 2, 4)
    print("saxriff.wav")
    plt.title("saxriff.wav")
    fName = "saxriff.wav"
    [fs, data] = spiowf.read(fName)
    data=canais_som(data)
    histograma(data, alfa_img_som())
    lista_som = ocorrencias(data, alfa_img_som())
    entr = entropia(data, alfa_img_som())
    print("Entropia: ",entr)
    prob=probabilidade(lista_som)
    mediabits_variancia(data, prob)
    entropiaPar(data, alfa_som_img_par())
    print("---------------------------------------------")
    
    plt.subplot2grid((3, 2), (2, 0), colspan=2)
    print("texto.txt")
    plt.title("texto.txt")
    fName= "texto.txt"
    ficheiro=open(fName, 'r')
    conteudo=ficheiro.read()
    cont=[]
    alfabeto=alfa_txt()
    for i in range(len(conteudo)):
        if (conteudo[i] in alfabeto):
            cont.append(conteudo[i])   
    histograma(cont,alfabeto)
    lista_txt = ocorrencias(cont, alfa_txt())
    entr = entropia(cont, alfa_txt())
    print("Entropia: ",entr)
    prob=probabilidade(lista_txt)
    mediabits_variancia(cont, prob)
    entropiaPar(cont,alfa_txt_par(alfabeto))
    ficheiro.close()
    print("---------------------------------------------")

    #----Ex06a----
    query = [2, 6, 4, 10, 5, 9, 5, 8, 0, 8]
    target = [6, 8, 9, 7, 2, 4, 9, 9, 4, 9, 1, 4, 8, 0, 1, 2, 2, 6, 3, 2, 0, 7, 4, 9, 5, 4, 8, 5, 2, 7, 8, 0, 7, 4, 8, 5, 7, 4, 3, 2, 2, 7, 3, 5, 2, 7, 4, 9, 9, 6]
    alfabeto = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9 , 10]
    passo = 1
    infoMutua(query, target, alfabeto, passo)
    
    
    #----Ex06b----
    plt.title('Variação da Informação mútua')
    plt.ylabel('Valor da Informação mútua')
    plt.xlabel('Janela da target')
    
    fName1 = "target01 - repeat.wav"
    [fs1, data1] = spiowf.read(fName1)
    data1=canais_som(data1)
    infomutua = infoMutua(data, data1, alfa_img_som(), int(len(data)/4))
    print(infomutua)
    plt.plot(infomutua)
    fName2 = "target02 - repeatNoise.wav"
    [fs1, data2] = spiowf.read(fName2)
    data2=canais_som(data2)
    infomutua = infoMutua(data, data2, alfa_img_som(), int(len(data)/4))
    print(infomutua)
    plt.plot(infomutua)
    plt.legend([fName1,fName2])
    print("---------------------------------------------")
    
    #----Ex06c----
    
    dicio = dict()
    
    print("Song01.wav")
    plt.subplot(13, 1, 1)
    fName1 = "Song01.wav"
    [fs1, data1] = spiowf.read(fName1)
    data1=canais_som(data1)
    infomutua = infoMutua(data, data1, alfa_img_som(), int(len(data)/4))
    dicio["Song01.wav"] = infomutua.max()
    plt.plot(infomutua)
    print("Vetor Informação mútua: {0}{1}Informação mútua máxima: {2}".format(infomutua, '\n', infomutua.max()))
    print("---------------------------------------------")
    
    print("Song02.wav")
    plt.subplot(13, 1, 3)
    fName2 = "Song02.wav"
    [fs2, data2] = spiowf.read(fName2)
    data2=canais_som(data2)
    infomutua = infoMutua(data, data2, alfa_img_som(), int(len(data)/4))
    dicio["Song02.wav"] = infomutua.max()
    plt.plot(infomutua)
    print("Vetor Informação mútua: {0}{1}Informação mútua máxima: {2}".format(infomutua, '\n', infomutua.max()))
    print("---------------------------------------------")
    
    print("Song03.wav")
    plt.subplot(13, 1, 5)
    fName3 = "Song03.wav"
    [fs3, data3] = spiowf.read(fName3)
    data3=canais_som(data3)
    infomutua = infoMutua(data, data3, alfa_img_som(), int(len(data)/4))
    dicio["Song03.wav"] = infomutua.max()
    plt.plot(infomutua)
    print("Vetor Informação mútua: {0}{1}Informação mútua máxima: {2}".format(infomutua, '\n', infomutua.max()))
    print("---------------------------------------------")
    
    print("Song04.wav")
    plt.subplot(13, 1, 7)
    fName4 = "Song04.wav"
    [fs4, data4] = spiowf.read(fName4)
    data4=canais_som(data4)
    infomutua = infoMutua(data, data4, alfa_img_som(), int(len(data)/4))
    dicio["Song04.wav"] = infomutua.max()
    plt.plot(infomutua)
    print("Vetor Informação mútua: {0}{1}Informação mútua máxima: {2}".format(infomutua, '\n', infomutua.max()))
    print("---------------------------------------------")
    
    print("Song05.wav")
    plt.subplot(13, 1, 9)
    fName5 = "Song05.wav"
    [fs5, data5] = spiowf.read(fName5)
    data5=canais_som(data5)
    infomutua = infoMutua(data, data5, alfa_img_som(), int(len(data)/4))
    dicio["Song05.wav"] = infomutua.max()
    plt.plot(infomutua)
    print("Vetor Informação mútua: {0}{1}Informação mútua máxima: {2}".format(infomutua, '\n', infomutua.max()))
    print("---------------------------------------------")
    
    print("Song06.wav")
    plt.subplot(13, 1, 11)
    fName6 = "Song06.wav"
    [fs6, data6] = spiowf.read(fName6)
    data6=canais_som(data6)
    infomutua = infoMutua(data, data6, alfa_img_som(), int(len(data)/4))
    dicio["Song06.wav"] = infomutua.max()
    plt.plot(infomutua)
    print("Vetor Informação mútua: {0}{1}Informação mútua máxima: {2}".format(infomutua, '\n', infomutua.max())) 
    print("---------------------------------------------")
    
    print("Song07.wav")
    plt.subplot(13, 1, 13)
    fName7 = "Song07.wav"
    [fs7, data7] = spiowf.read(fName7)
    data7=canais_som(data7)
    infomutua = infoMutua(data, data7, alfa_img_som(), int(len(data)/4))
    dicio["Song07.wav"] = infomutua.max()
    plt.plot(infomutua)
    print("Vetor Informação mútua: {0}{1}Informação mútua máxima: {2}".format(infomutua, '\n', infomutua.max())) 
    print("---------------------------------------------")
     
    dicio_ord = dict()
    
    for song in sorted(dicio, key = dicio.get, reverse=True):
        dicio_ord[song]=dicio[song]
        
    print(dicio_ord)