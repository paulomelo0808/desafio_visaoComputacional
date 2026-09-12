import cv2

imagem = cv2.imread("/mnt/wdc/desafio_visaoComputacional/frame.jpeg")

hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

cv2.imwrite("frame_hsv.jpg", hsv)

print("Imagem convertida para HSV!")