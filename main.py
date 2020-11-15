from Neural import *
from Robot import Track
from Robot import Truck
from Robot import Manipulator
IsActive = True
a = ''


# main loop
while True:
    success, img = cap.read()

    blob = cv2.dnn.blobFromImage(img,1/255,(whT,whT),[0,0,0],1,crop=False)  # ? to blob conv
    net.setInput(blob)

    layerNames = net.getLayerNames()
    outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]

    outputs = net.forward(outputNames)
    Neural.findObjects(outputs, img)  # Используем нейронку
    if not Manipulator.busy:  # Если манипулятор
        # свободен
        Track.findBottle(Neural.n_ame)  # Ищем бутылку
        if Track.bottlefound and Truck.IsTurnedToTheTarget() and Neural.BottleRange > 35:  # Если бутыла
            # найдена, тележка направлена на нёё и расстояние между тележкой и обьектом >35 см
            Truck.Move(Neural.BottleRange)  # Двигаемся к обьекту
    if Neural.n_ame == 'BOTTLE' and Neural.BottleRange < 35:  # Если расстояние
        # меньше 35 см, берем предмет
        Manipulator.Lock()
        Manipulator.busy = True
    if Manipulator.busy:  # Если манипулятор занят
        Track.findHuman(Neural.n_ame)  # Поиск человека
    if Manipulator.busy and Track.humanfound and Truck.IsTurnedToTheTarget():
        Truck.Move(Neural.HumanRange)
    if Neural.n_ame == 'PERSON' and Neural.BottleRange < 35 and Wannamore.dontwant:
        Manipulator.Unlock()
        Manipulator.busy = False
        while True:
            print('Робот доставил обьект. Хотите продолжить? (yes или no)')
            a = input('Введите ответ: ')
            if a == 'yes' or a == 'YES' or a == 'Yes' or a == 'y' or a == 'Y':
                IsActive = True
                Wannamore.dontwant = False
                break
            elif a == 'no' or a == 'NO' or a == 'No':
                IsActive = False
                break
            else:
                print('Некорректный ввод')
    if not IsActive:
        break

    cv2.imshow('Image', img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break