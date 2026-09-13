import cv2
from pathlib import Path

PASTA_TESTES = Path(__file__).resolve().parent
PASTA_PROJETO = PASTA_TESTES.parent

CAMINHO_VIDEO = (
    PASTA_PROJETO
    / "Minicurso Visão Computacional - 2026"
    / "esteira.mp4"
)

LARGURA_MINIMA = 80
ALTURA_MINIMA = 70

FRAMES_PARA_REARMAR = 2

video = cv2.VideoCapture(str(CAMINHO_VIDEO))

if not video.isOpened():
    print("Erro: não foi possível abrir o vídeo.")
    print(f"Verifique se 'esteira.mp4' está em: {PASTA_SCRIPT}")
    exit()


largura_video = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
altura_video = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

linha_x = largura_video // 2

kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (7, 7)
)

contador_total = 0

contador_inicio = 0
contador_cruzamentos = 0
contador_fim = 0

linha_ocupada = False
frames_livres = 0

primeiro_frame = True
ultimas_deteccoes = []

numero_frame = 0

while True:

    sucesso, frame = video.read()

    if not sucesso:
        break

    numero_frame += 1

    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2HSV
    )

    mascara = cv2.inRange(
        hsv,
        (0, 100, 100),
        (10, 255, 255)
    )

    mascara = cv2.morphologyEx(
        mascara,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    deteccoes = []

    for contorno in contornos:

        area = cv2.contourArea(contorno)

        x, y, largura, altura = cv2.boundingRect(contorno)


        if (
            largura >= LARGURA_MINIMA
            and altura >= ALTURA_MINIMA
        ):

            deteccoes.append(
                {
                    "bbox": (
                        x,
                        y,
                        largura,
                        altura
                    ),
                    "area": area
                }
            )

    if primeiro_frame:

        for deteccao in deteccoes:

            x, y, largura, altura = deteccao["bbox"]

            if x > linha_x:

                contador_total += 1
                contador_inicio += 1

        primeiro_frame = False

    tem_garrafa_na_linha = False


    for deteccao in deteccoes:

        x, y, largura, altura = deteccao["bbox"]

        if x <= linha_x <= x + largura:

            tem_garrafa_na_linha = True
            break

    if tem_garrafa_na_linha:

        frames_livres = 0


        if not linha_ocupada:

            contador_total += 1
            contador_cruzamentos += 1

            linha_ocupada = True

            print(
                f"Garrafa cruzou a linha. "
                f"Total: {contador_total}"
            )

    else:

        if linha_ocupada:

            frames_livres += 1


            if frames_livres >= FRAMES_PARA_REARMAR:

                linha_ocupada = False
                frames_livres = 0

    ultimas_deteccoes = deteccoes.copy()

for deteccao in ultimas_deteccoes:

    x, y, largura, altura = deteccao["bbox"]


    if x + largura < linha_x:

        contador_total += 1
        contador_fim += 1

video.release()


print()
print("Processamento concluído.")
print(f"Frames processados: {numero_frame}")

print(
    f"Garrafas presentes após a linha no início: "
    f"{contador_inicio}"
)

print(
    f"Garrafas que cruzaram a linha: "
    f"{contador_cruzamentos}"
)

print(
    f"Garrafas ainda antes da linha no final: "
    f"{contador_fim}"
)

print()
print(
    f"Total de garrafas contadas: "
    f"{contador_total}"
)
