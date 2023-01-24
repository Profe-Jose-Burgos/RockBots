import json 
import pickle 
import nltk
import numpy as np

from tensorflow.keras.models import load_model
from nltk.stem import SnowballStemmer
import random



ignore_words= ["?","¿","!","¡","."]
model=load_model('bot_model.h5')
biblioteca=json.loads(open('intents.json').read())
bolsaPalabras=pickle.load(open('bolsaPalabras.pkl','rb'))
clases=pickle.load(open('clases.pkl','rb'))


def limpiarentrada(entradaUsuario):
    entradaUsuario = nltk.word_tokenize(entradaUsuario)
    entradaUsuario = [stemmer.stem(w.lower()) for w in entradaUsuario if w not in ignore_words]
    return entradaUsuario

def convVector(entradaUsuario, bolsaPalabras):
    
    entradaUsuario = limpiarentrada(entradaUsuario)
    
    vectorentrada = [0]*len(bolsaPalabras)    
    for palabra in entradaUsuario:              
        
        if palabra in bolsaPalabras:         
            
            indice = bolsaPalabras.index(palabra)   
            vectorentrada[indice] = 1                  
            
    vectorentrada = np.array(vectorentrada)            
    return vectorentrada


def obt_tag(vectorentrada,LIMITE=0):
    vector_salida=model.predict(np.array([vectorentrada]))[0]

    vector_salida=[[i,r] for i,r in enumerate(vector_salida) if r > LIMITE]

    vector_salida.sort(key=lambda x: x[1],reverse=True)
    print(vector_salida)

    list_etiquetas=[]

    for r in vector_salida:
        list_etiquetas.append({'intent':clases[r[0]],'probability':str(r[1])})
   
    return list_etiquetas


def obt_respuesta(list_etiquetas,biblioteca):
    etiqueta=list_etiquetas[0]['intent']

    lista_diccionarios=biblioteca['intents']

    for diccionario in lista_diccionarios:

        if etiqueta==diccionario['tag']:
            list_respuestas=diccionario['responses']
            respuesta=random.choice(list_respuestas)

            break
    
    return respuesta

def chatbot_respuesta(entradaUsuario):
    vector_entrada=convVector(entradaUsuario,bolsaPalabras)
    list_etiquetas=obt_tag(vector_entrada,LIMITE=0)
    respuesta=obt_respuesta(list_etiquetas,biblioteca)
    intencion=list_etiquetas[0]['intent']
    return respuesta,intencion