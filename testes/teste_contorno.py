import cv2

imagem = cv2.imread(
    "/home/paulomelo/Documentos/desafio_visaocomputacional/testes/mascara1.jpg",
    cv2.IMREAD_GRAYSCALE
)

if imagem is None:
    print("Erro: não foi possível carregar mascara1.jpg")
    exit()

kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (7, 7)
)

imagem = cv2.morphologyEx(
    imagem,
    cv2.MORPH_CLOSE,
    kernel,
    iterations=2
)

contornos, hierarquia = cv2.findContours(
    imagem,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

print("Quantidade de contornos encontrados:", len(contornos))

imagem_colorida = cv2.cvtColor(imagem, cv2.COLOR_GRAY2BGR)

for contorno in contornos:
    area = cv2.contourArea(contorno)

    x, y, largura, altura = cv2.boundingRect(contorno)

    if largura >= 80 and altura >= 70:
        print(
            "CANDIDATO A GARRAFA:",
            "Área:", area,
            "| x:", x,
            "| y:", y,
            "| largura:", largura,
            "| altura:", altura
        )

        cv2.rectangle(
            imagem_colorida,
            (x, y),
            (x + largura, y + altura),
            (0, 0, 255),
            2
        )

        cv2.putText(
            imagem_colorida,
            str(round(area, 1)),
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 0, 255),
            1
        )

cv2.imwrite(
    "/home/paulomelo/Documentos/desafio_visaocomputacional/testes/contornos.jpg",
    imagem_colorida
)

print("Imagem salva como contornos.jpg")
