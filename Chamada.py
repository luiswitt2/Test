import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time
import pandas as pd
import mysql.connector
from mysql.connector import Error


path = 'imagensChamada'
images = []
nomes = []
lista = os.listdir(path)
# ler cada imagem da lista
for im in lista:
    imgAtual = cv2.imread(f'{path}/{im}')
    images.append(imgAtual)
    # adiciona a imagem sem o .jpeg
    nomes.append(os.path.splitext(im)[0])
print(nomes)

def desenhar_rosto(frame, local):
    """

    :param frame: frame atual da camera
    :param local: coordenadas do rosto
    :return:
    """

    top, right, bottom, left = local
    top, right, bottom, left = top*4, right*4, bottom*4, left*4

    cor = (204, 204, 0)

    cv2.rectangle(frame, (left, top), (right, bottom), cor, 2)
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), cor, cv2.FILLED)
    cv2.putText(img, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)



def MarcarPresenca(nome):
    """
    Marca a presença e o horário de entrada do aluno no arquivo "listaChamada.csv" se já nao estiver presente
    :param nome: nome do aluno
    :return:
    """
    with open('listaChamada.csv', 'r+') as f:
        listaChamada = f.readlines()
        listaNomes = []
         
        for line in listaChamada:
            # separa data e hora
            entrada = line.split(',')
            listaNomes.append(entrada[0]) 
            
        if nome not in listaNomes:
      
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{nome}, {dtString}')    
                          
def findEncoding(images):
    """
    :param images:
    :return:
    """

    encodeList = []
    # converte todass as imagens da lista pra RGB
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList



#lista de todas as imagens conhecidas já convertidas
encodeListConhecido = findEncoding(images)


cam = cv2.VideoCapture(0)
count = 0
nomeAtt = ''
while count < 4:

    sucesso, img = cam.read()
    img = cv2.flip(img, 1)
    # diminui o tamanho da imagem para agilizar
    imgS = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesFrameAtt = face_recognition.face_locations(imgS)
    encodesFrameAtt = face_recognition.face_encodings(imgS, facesFrameAtt)


    for encodeFace, faceLoc in zip(encodesFrameAtt, facesFrameAtt):
        matches = face_recognition.compare_faces(encodeListConhecido, encodeFace)
        faceDis = face_recognition.face_distance(encodeListConhecido, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        # Desenha o retangulo no rosto se o rosto bater com algum da lista
        if matches[matchIndex]:
            name = nomes[matchIndex].upper()
            nomeAtt = nomes[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            desenhar_rosto(img, faceLoc)
            MarcarPresenca(name)
            count += 1

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
    
print(nomeAtt)
#teste = cv2.imread('imagensChamada/eduardo.jpg')
#testeS = cv2.resize(teste, (0, 0), None, 0.5, 0.5)

#cv2.imshow('image', testeS)

df = pd.read_csv(r'C:\Users\luisw\OneDrive\Área de Trabalho\FaceScan\listaChamada.csv')

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='db_teste',
                                         user='root',
                                         password='1234')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Conectado ao servidor MySQL: versão", db_Info)
except Error as e:
    print("Erro ao conectar ao MySQL", e)
cursor = connection.cursor()
for index, row in df.iterrows():
    sql = "INSERT INTO Pessoas (nome, horario) VALUES (%s, %s)"
    val = (row['Nome'], row['Hora'])
    cursor.execute(sql, val)
    connection.commit()
print(cursor.rowcount, "registros inseridos com sucesso.")
cursor.close()
connection.close()
print("Conexão com o MySQL encerrada.")

cv2.waitKey(3000)
cv2.destroyallwindows()
