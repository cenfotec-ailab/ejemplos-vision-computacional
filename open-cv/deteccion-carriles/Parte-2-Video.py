import numpy as np
import cv2

def lane_draw(_frame):
    # imagen en b/n
    frame_bn = _frame[:,:,0]
    # se crea un arreglo de ceros basado en la imagen en blanco y negro
    stencil = np.zeros_like(frame_bn)
    # se define el poligono de interes.
    polygon = np.array([[0,250], [100,150], [200,150], [350,250]])
    # se llena la imagen de ceros con el poligono creado en blanco (unos)
    cv2.fillConvexPoly(stencil, polygon, 1)
    # se aplica la mascara a la imagen en blanco y negro
    img = cv2.bitwise_and(frame_bn, frame_bn, mask=stencil)
    # Se usa cv2.threshold para convertir la imagen anterior en blanco y negro puro
    # esto causa que las lineas blancas sean las unicas que queden en blanco.
    ret, thresh = cv2.threshold(img, 200, 50, cv2.THRESH_BINARY)
    # cv2.HoughLinesP nos permite encontrar lineas en una imagen. En este caso estas son
    # las de las divisiones de los carriles.
    lines = cv2.HoughLinesP(thresh, 1, np.pi/180, 30, maxLineGap=40)
    if (lines is not None):
        # se dibujan las lineas en la imagen original (frame) con color azul
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    return _frame

cap = cv2.VideoCapture('general.mp4')
count = 0
while(cap.isOpened()):
    ret, frame = cap.read()

    try:
        frame = lane_draw(frame)
    except Exception as e:
        print(str(e))

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
