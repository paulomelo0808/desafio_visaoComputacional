import cv2

video = cv2.VideoCapture("/mnt/wdc/desafio_visaoComputacional/Minicurso Visão Computacional - 2026/esteira.mp4")

sucesso, frame = video.read()

if sucesso:
    cv2.imwrite("frame.jpeg", frame)
    print("Frame salvo com sucesso!")
else:
    print("Não foi possivel ler video.")

video.release()