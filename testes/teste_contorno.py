import cv2

imagem = cv2.imread("/mnt/wdc/desafio_visaoComputacional/mascara1.jpg", cv2.IMREAD_GRAYSCALE)

if imagem is None:
    print("Erro: não foi possível carregar mascara1.jpg")
    exit()

contornos, hierarquia = cv2.findContours(
    imagem,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

print("Quantidade de contornos encontrados:", len(contornos))

for contorno in contornos:
    area = cv2.contourArea(contorno)

    if area >20:
        x, y, largura, altura = cv2.boundingRect(contorno)

        print(
            "Area:", area,
            "| x:", x,
            "| y:", y,
            "| largura:", largura,
            "| altura:", altura
        )

imagem_contornos = cv2.cvtColor(imagem, cv2.COLOR_GRAY2BGR)

cv2.drawContours(
    imagem_contornos,
    contornos,
    -1,
    (0, 255, 0),
    2
)

cv2.imwrite("contornos.jpg", imagem_contornos)