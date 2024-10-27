import cv2

def process_frame(frame):
    """
    Крис хочет квадратик пока центру ну ок
    Заглушка нейросети: рисует квадратик в центре экрана.
    
    :param frame: исходный фрейм
    :return: фрейм с нарисованным квадратиком
    """
    height, width, _ = frame.shape
    # Координаты квадрата (центр экрана)
    top_left = (width // 2 - 50, height // 2 - 50)
    bottom_right = (width // 2 + 50, height // 2 + 50)
    color = (0, 255, 0)  # Зелененький square
    thickness = 2  # Толщина линии
    
    # Рисуем квадрат на фрейме
    cv2.rectangle(frame, top_left, bottom_right, color, thickness)
    
    return frame
