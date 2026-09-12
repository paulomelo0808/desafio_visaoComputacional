import cv2

imagem = cv2.imread("/mnt/wdc/desafio_visaoComputacional/frame.jpeg")

if imagem is None:
    print("Erro: não foi possivel carregar frame.jpg")
    exit()

hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

#Teste 1
mascara1 = cv2.inRange(
    hsv,
    (0, 100, 100),
    (10, 255, 255)
)

#Teste 2 - maior saturação e brilho
mascara2 = cv2.inRange(
    hsv,
    (0, 110, 110),
    (10, 255, 255)
)

#teste3 - ainda maior saturação e brilho
mascara3 = cv2.inRange(
    hsv,
    (0, 120, 120),
    (10, 255, 255)
)

cv2.imwrite("mascara1.jpg", mascara1)
cv2.imwrite("mascara2.jpg", mascara2)
cv2.imwrite("mascara3.jpg", mascara3)

print("Máscaras criadas!")