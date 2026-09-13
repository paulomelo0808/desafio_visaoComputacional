import cv2
from pathlib import Path

PASTA_SCRIPT = Path(__file__).resolve().parent
CAMINHO_VIDEO = PASTA_SCRIPT / "esteira.mp4"

LARGURA_MINIMA = 80
ALTURA_MINIMA = 70

FRAMES_PARA_REARMAR = 2

video = cv2.VideoCapture(str(CAMINHO_VIDEO))

if not video.isOpened():
    print("Erro: não foi possível abrir o vídeo 'esteira.mp4'.")
    print(f"Diretório esperado: {PASTA_SCRIPT}")
    raise SystemExit(1)

largura_video = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

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

        x, y, largura, altura = cv2.boundingRect(contorno)

        if largura >= LARGURA_MINIMA and altura >= ALTURA_MINIMA:

            deteccoes.append(
                {
                    "bbox": (x, y, largura, altura)
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

print(f"Total de garrafas contadas: {contador_total}")
