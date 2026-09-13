import cv2
from pathlib import Path

PASTA_TESTES = Path(__file__).resolve().parent
PASTA_PROJETO = PASTA_TESTES.parent

caminho_video = Path(
    "/home/paulomelo/Documentos/desafio_visaocomputacional/Minicurso Visão Computacional - 2026/esteira.mp4"
)

caminho_saida = Path(
    "/home/paulomelo/Documentos/desafio_visaocomputacional/testes/teste_deteccao.mp4"
)


video = cv2.VideoCapture(str(caminho_video))

if not video.isOpened():
    print("Erro: não foi possível abrir o vídeo.")
    print("Caminho:", caminho_video)
    exit()


largura_video = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
altura_video = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

saida = cv2.VideoWriter(
    str(caminho_saida),
    fourcc,
    fps,
    (largura_video, altura_video)
)


kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (7, 7)
)


numero_frame = 0

while True:
    sucesso, frame = video.read()

    if not sucesso:
        break

    numero_frame += 1

    # Converte o frame para HSV
    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2HSV
    )

    # Segmentação da cor vermelha
    mascara = cv2.inRange(
        hsv,
        (0, 100, 100),
        (10, 255, 255)
    )

    # Une regiões próximas da máscara
    mascara = cv2.morphologyEx(
        mascara,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    # Procura os contornos
    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    candidatos = 0

    for contorno in contornos:
        area = cv2.contourArea(contorno)

        x, y, largura, altura = cv2.boundingRect(contorno)

        # Filtro provisório
        if largura >= 80 and altura >= 70:
            candidatos += 1

            cv2.rectangle(
                frame,
                (x, y),
                (x + largura, y + altura),
                (0, 255, 0),
                2
            )

            centro_x = x + largura // 2
            centro_y = y + altura // 2

            cv2.circle(
                frame,
                (centro_x, centro_y),
                5,
                (255, 0, 0),
                -1
            )

            cv2.putText(
                frame,
                f"A:{round(area)}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

    cv2.putText(
        frame,
        f"Detectadas: {candidatos}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    linha_x = int(largura_video * 0.70)

    cv2.line(
        frame,
        (linha_x, 0),
        (linha_x, altura_video),
        (255, 255, 0),
        2
    )

    saida.write(frame)

video.release()
saida.release()

print("Processamento concluído.")
print("Frames processados:", numero_frame)
print("Vídeo salvo em:", caminho_saida)
