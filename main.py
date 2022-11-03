import io
import random as rd
import time

import PySimpleGUI as sg
import numpy as np
from PIL import Image, ImageTk


def get_img_data(f, maxsize=(1200, 850), first=False):
    """Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:  # tkinter is inactive the first time
        cur_width, cur_height = img.size
        new_width = cur_width * 2.5
        new_height = cur_height * 2.5
        scale = min(new_height / cur_height, new_width / cur_width)
        img = img.resize((int(cur_width * scale), int(cur_height * scale)), Image.ANTIALIAS)
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)


def method1(sample, photo, number):
    points = [rd.randint(0, sample.size) for i in range(int(sample.size / number))]
    # for i in range(len(points)):
    # print(points[i])
    # print(points[i]//sample.shape[0])
    # print(points[i]%sample.shape[0])
    sample_points = np.array([sample[i // sample.shape[0]][i % sample.shape[1]] for i in points])
    photo_points = np.array([photo[i // sample.shape[0]][i % sample.shape[1]] for i in points])
    return (np.absolute(sample_points - photo_points))


def hist(photo, number):
    hist = [0] * number
    step = 256 / number
    for i in range(photo.shape[0]):
        for j in range(photo.shape[1]):
            hist[int(photo[i][j] // step)] += 1
    return (np.array(hist))


def result_method(sample_hist, photo_hist):
    return (np.absolute(sample_hist - photo_hist))


def scaling(photo):
    new_photo = []
    for i in range(0, photo.shape[0] - 30, 20):
        for j in range(0, photo.shape[1] - 30, 20):
            temp = 0
            for k in range(i, i + 30):
                for l in range(j, j + 30):
                    temp += photo[k][l]
            new_photo.append(round(temp / 900))
    return (np.array(new_photo))


def scaling2(photo):
    new_photo = []
    for i in range(0, photo.shape[0] - 10, 10):
        for j in range(0, photo.shape[1] - 10, 10):
            temp = 0
            for k in range(i, i + 10):
                for l in range(j, j + 10):
                    temp += photo[k][l]
            new_photo.append(round(temp / 100))
    return (np.array(new_photo))


def read_pgm(path):
    pgmf = open(path, 'rb')
    assert pgmf.readline() == b'P5\n'
    (width, height) = [int(i) for i in pgmf.readline().split()]
    depth = int(pgmf.readline())
    assert depth <= 255

    raster = []
    for y in range(height):
        row = []
        for y in range(width):
            row.append(ord(pgmf.read(1)))
        raster.append(row)
    pgmf.close()
    im = np.array(raster)
    return im


def parallel_hist(photo, samples_hist, number):
    hist = [0] * number
    step = 256 / number
    for i in range(photo.shape[0]):
        for j in range(photo.shape[1]):
            hist[int(photo[i][j] // step)] += 1
    dif = []
    for sample_hist in samples_hist:
        dif.append(sum(np.absolute(sample_hist - np.array(hist))))
    temp = sorted(dif)[:3]
    for i in range(0, 3):
        temp[i] = dif.index(temp[i])
    return (temp)


def parallel_method1(samples, photo):
    points = [rd.randint(0, samples[0].size) for i in range(int(samples[0].size / 150))]
    photo_points = np.array([photo[i // samples[0].shape[0]][i % samples[0].shape[1]] for i in points])
    dif = []
    for sample in samples:
        dif.append(sum(np.absolute(
            np.array([sample[i // sample.shape[0]][i % sample.shape[1]] for i in points]) - photo_points)))
    temp = np.sort(dif)[:3]
    for i in range(0, 3):
        temp[i] = dif.index(temp[i])
    return (temp)


def parallel_scaling2(photo, samples_scaling2):
    new_photo = []
    for i in range(0, photo.shape[0] - 10, 10):
        for j in range(0, photo.shape[1] - 10, 10):
            temp = 0
            for k in range(i, i + 10):
                for l in range(j, j + 10):
                    temp += photo[k][l]
            new_photo.append(round(temp / 100))
    dif = []
    for sample in samples_scaling2:
        dif.append(sum(np.absolute(np.array(new_photo) - sample)))
    temp = sorted(dif)[:3]
    for i in range(0, 3):
        temp[i] = dif.index(temp[i])
    return (temp)


def parallel_scaling(photo, samples_scaling):
    new_photo = []
    for i in range(0, photo.shape[0] - 30, 20):
        for j in range(0, photo.shape[1] - 30, 20):
            temp = 0
            for k in range(i, i + 30):
                for l in range(j, j + 30):
                    temp += photo[k][l]
            new_photo.append(round(temp / 900))
    dif = []
    for sample in samples_scaling:
        dif.append(sum(np.absolute(np.array(new_photo) - sample)))
    temp = sorted(dif)[:3]
    for i in range(0, 3):
        temp[i] = dif.index(temp[i])
    return (temp)


def parallel_difference(photo, samples_difference):
    new_photo = []
    pic_before = 0
    for k in range(0, 10):
        for l in range(0, 10):
            pic_before += photo[k][l]
    pic_before = round(pic_before / 100)
    for i in range(10, photo.shape[0] - 10, 10):
        for j in range(10, photo.shape[1] - 10, 10):
            temp = 0
            for k in range(i, i + 10):
                for l in range(j, j + 10):
                    temp += photo[k][l]
            temp = round(temp / 100)
            new_photo.append(temp - pic_before)
            pic_before = temp
    dif = []
    for sample in samples_scaling2:
        dif.append(sum(np.absolute(np.array(new_photo) - sample)))
    temp = sorted(dif)[:3]
    for i in range(0, 3):
        temp[i] = dif.index(temp[i])
    return (temp)


all_photo = []
for j in range(1, 41):
    for i in range(1, 11):
        all_photo.append(
            read_pgm("/home/victor21/PycharmProjects/pythonProject2/Arch/s" + str(j) + '/' + str(i) + '.pgm'))

number = 2
samples = []
samples_adress = []
for k in range(0, 40):
    first = rd.randint(0, 9)
    second = rd.randint(0, 9)
    while first == second:
        second = rd.randint(0, 9)
    samples.append(all_photo[k * 10 + first])
    samples.append(all_photo[k * 10 + second])
    samples_adress.append('s' + str(k + 1) + '/' + str(first + 1))
    samples_adress.append('s' + str(k + 1) + '/' + str(second + 1))

samples_hist8 = []
for i in range(len(samples)):
    samples_hist8.append(hist(samples[i], 8))

samples_hist64 = []
for i in range(len(samples)):
    samples_hist64.append(hist(samples[i], 64))

samples_scaling = []
for i in range(len(samples)):
    samples_scaling.append(scaling(samples[i]))

samples_scaling2 = []
for i in range(len(samples)):
    samples_scaling2.append(scaling2(samples[i]))

layout = [[sg.Button('Start first method'), sg.Button('Start second method')]]
window = sg.Window('Face detection', layout, finalize=True)
while True:  # The Event Loop
    event, values = window.read()
    print(event, values)  # debug
    if event == sg.WIN_CLOSED:
        window.close()
        break
    if event == "Start first method":
        window.close()
        Flag = "False"
        iterable = 1
        true_iter = 0
        image_elem2 = sg.Image(get_img_data('Arch/s1/1.pgm', first=True), key='result')
        image_elem3 = sg.Image(get_img_data('Arch/' + samples_adress[(iterable - 1) // 10 * 2] + '.pgm', first=True),
                               key='True sample')
        image_elem1 = sg.Image(
            get_img_data('Arch/s' + str((iterable - 1) // 10 + 1) + '/' + str((iterable - 1) % 10 + 1) + '.pgm',
                         first=True), key='photo')
        textelem1 = sg.Text('s' + str((iterable - 1) // 10 + 1), font=88)
        textelem2 = sg.Text(Flag, font=88)
        textelem3 = sg.Text("Current accuracy: " + str(true_iter / iterable), font=88)
        layout = [[textelem1, textelem2],
                  [sg.Text("TEST                                                             "),
                   sg.Text(" ANSWER                                         "), sg.Text("TRUE ANSWER")],
                  [image_elem1,
                   image_elem2,
                   image_elem3],
                  [textelem3]
                  ]
        window = sg.Window('Face detection', layout, finalize=True, resizable=True, location=(700, 300))
        iterable -= 1
        for photo in all_photo:
            Flag = "False"
            iterable += 1
            first = parallel_hist(photo, samples_hist8, 8)
            second = parallel_hist(photo, samples_hist64, 64)
            third = parallel_scaling2(photo, samples_scaling2)
            agreement = dict()
            agreement[first[0]] = 3
            agreement[first[1]] = 2
            agreement[first[2]] = 1
            if second[0] in agreement:
                agreement[second[0]] += 3
            else:
                agreement[second[0]] = 3
            if second[1] in agreement:
                agreement[second[1]] += 2
            else:
                agreement[second[1]] = 2
            if second[2] in agreement:
                agreement[second[2]] += 1
            else:
                agreement[second[2]] = 1
            if third[0] in agreement:
                agreement[third[0]] += 3.03
            else:
                agreement[third[0]] = 3.03
            if third[1] in agreement:
                agreement[third[1]] += 2.02
            else:
                agreement[third[1]] = 2.02
            if third[2] in agreement:
                agreement[third[2]] += 1.01
            else:
                agreement[third[2]] = 1.01
            max_value = max(agreement.values())
            for k, v in agreement.items():
                if v == max_value:
                    result = k
                    break
            if str(((iterable - 1) // 10) + 1) == samples_adress[result][1:samples_adress[result].index('/')]:
                Flag = "True"
                true_iter += 1
            time.sleep(0.2)
            image_elem1.update(data=get_img_data(
                'Arch/s' + str((iterable - 1) // 10 + 1) + '/' + str((iterable - 1) % 10 + 1) + '.pgm', first=True))
            image_elem2.update(data=get_img_data('Arch/' + samples_adress[result] + '.pgm', first=True))
            image_elem3.update(
                data=get_img_data('Arch/' + samples_adress[(iterable - 1) // 10 * 2] + '.pgm', first=True))
            textelem1.update(value='s' + str((iterable - 1) // 10 + 1))
            textelem2.update(value=Flag)
            textelem3.update(value="Current accuracy: " + str(true_iter / iterable))
            window.Refresh()
        layout = [[sg.Text("Final accuracy: " + str(true_iter / iterable))], [sg.Button("Close")]
                  ]
        window = sg.Window('Face detection', layout, finalize=True)
        window.Refresh()
    if event == "Start second method":
        window.close()
        Flag = "False"
        iterable = 1
        true_iter = 0
        image_elem2 = sg.Image(get_img_data('Arch/s1/1.pgm', first=True), key='result')
        image_elem3 = sg.Image(get_img_data('Arch/' + samples_adress[(iterable - 1) // 10 * 2] + '.pgm', first=True),
                               key='True sample')
        image_elem1 = sg.Image(
            get_img_data('Arch/s' + str((iterable - 1) // 10 + 1) + '/' + str((iterable - 1) % 10 + 1) + '.pgm',
                         first=True), key='photo')
        textelem1 = sg.Text('s' + str((iterable - 1) // 10 + 1), font=88)
        textelem2 = sg.Text(Flag, font=88)
        textelem3 = sg.Text("Current accuracy: " + str(true_iter / iterable), font=88)
        layout = [[textelem1, textelem2],
                  [sg.Text("TEST                                                             "),
                   sg.Text(" ANSWER                                         "), sg.Text("TRUE ANSWER")],
                  [image_elem1,
                   image_elem2,
                   image_elem3],
                  [textelem3]
                  ]
        window = sg.Window('Face detection', layout, finalize=True, resizable=True, location=(700, 300))
        iterable -= 1
        for photo in all_photo:
            Flag = "False"
            iterable += 1
            first = parallel_method1(samples, photo)
            second = parallel_hist(photo, samples_hist64, 64)
            third = parallel_scaling2(photo, samples_scaling2)
            agreement = dict()
            agreement[first[0]] = 3
            agreement[first[1]] = 2
            agreement[first[2]] = 1
            if second[0] in agreement:
                agreement[second[0]] += 3
            else:
                agreement[second[0]] = 3
            if second[1] in agreement:
                agreement[second[1]] += 2
            else:
                agreement[second[1]] = 2
            if second[2] in agreement:
                agreement[second[2]] += 1
            else:
                agreement[second[2]] = 1
            if third[0] in agreement:
                agreement[third[0]] += 3.01
            else:
                agreement[third[0]] = 3.01
            if third[1] in agreement:
                agreement[third[1]] += 2.01
            else:
                agreement[third[1]] = 2.01
            if third[2] in agreement:
                agreement[third[2]] += 1.01
            else:
                agreement[third[2]] = 1.01
            max_value = max(agreement.values())
            for k, v in agreement.items():
                if v == max_value:
                    result = k
                    break
            if str(((iterable - 1) // 10) + 1) == samples_adress[result][1:samples_adress[result].index('/')]:
                Flag = "True"
                true_iter += 1
            time.sleep(0.2)
            image_elem1.update(data=get_img_data(
                'Arch/s' + str((iterable - 1) // 10 + 1) + '/' + str((iterable - 1) % 10 + 1) + '.pgm', first=True))
            image_elem2.update(data=get_img_data('Arch/' + samples_adress[result] + '.pgm', first=True))
            image_elem3.update(
                data=get_img_data('Arch/' + samples_adress[(iterable - 1) // 10 * 2] + '.pgm', first=True))
            textelem1.update(value='s' + str((iterable - 1) // 10 + 1))
            textelem2.update(value=Flag)
            textelem3.update(value="Current accuracy: " + str(true_iter / iterable))
            window.Refresh()
        layout = [[sg.Text("Final accuracy: " + str((true_iter - 80) / (iterable - 80)))], [sg.Button("Close")]
                  ]
        window = sg.Window('Face detection', layout, finalize=True)
        window.Refresh()
    if event == 'Close':
        window.close()
