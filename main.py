import os
import cv2
import numpy as np
import face_recognition
import requests

from client import JwtClient
from datetime import datetime


'''
Get Encodings
Return face encoding for each image
'''
def get_encodings(images):
    encoded_list = []
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encoded_image = face_recognition.face_encodings(image)[0]
        encoded_list.append(encoded_image)
    return encoded_list


'''
Mark Attendance
Write attendance to a csv file by dates
'''
def mark_attendance(name):
    day, names = datetime.now().strftime('%d_%m'), set()
    datapath = os.path.dirname(__file__) + '\\data'
    filepath = datapath + f'\\attendance_{day}.csv'
    try:
        with open(filepath, 'r+') as file:
            content = file.readlines()
            if not content: file.write('Name,Time')
            for line in content:
                entry = line.split(',')
                names.add(entry[0])
            if name not in names:
                time = datetime.now().strftime('%H:%M:%S')
                file.writelines(f'\n{name},{time}')
    except Exception as e:
        with open(filepath, 'w') as file:
            file.write('Name,Time')
    return filepath


'''
Open Webcam
Open camera to start face detection and mark attendance
'''
def open_webcam():
    PATH = os.path.dirname(__file__) + '\\img'
    FILE_LIST = os.listdir(PATH)

    images, labels = [], []
    for filename in FILE_LIST:
        current_image = cv2.imread(f'{PATH}/{filename}')
        labels.append(os.path.splitext(filename)[0])
        images.append(current_image)
    
    encoding_list = get_encodings(images=images)
    print('Encoding complete\nOpening webcam...')

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print('Can\'t receive frame (stream end?). Exiting ...')
            break

        # Resize frame (image) and convert from BGR to RGB
        frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get face location and face encoding from the frame (image)
        face_loc_frame = face_recognition.face_locations(frame)
        face_enc_frame = face_recognition.face_encodings(frame, face_loc_frame)

        for face_enc, face_loc in zip(face_enc_frame, face_loc_frame):
            result = face_recognition.compare_faces(encoding_list, face_enc)
            face_distance = face_recognition.face_distance(encoding_list, face_enc)

            # Get the index of the minimum value of the distance
            # Smaller value means the face is tend to be more similar
            i = np.argmin(face_distance)
            if result[i]:
                label = labels[i].upper()
                y1, x2, y2, x1 = [i*4 for i in face_loc]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, label, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                label = label[:label.index('_')]
                print(f'{label} detected.')
                
                # Write attendance and get the file
                src = mark_attendance(label)
        
        cv2.imshow('Webcam', frame)
        cv2.waitKey(1)

        # Close webcam by clicking 'Q' three times
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return src


# Main Program / Driver
if __name__ == '__main__':
    try:
        # Perform authentication
        # If creds.json does not exist, user need to log in
        client = JwtClient()
        cc = input('Enter course code: ')

        # Set headers
        headers = {
            'Authorization': f'Bearer {client.access}'
        }

        # Request list of attendance
        endpoint = {
            'attendance-list': 'http://localhost:8000/api/attendance',
        }
        attendance_list = requests.get(endpoint['attendance-list'])
        attendance_list = attendance_list.json()['results']

        # Open webcam and write attendance into csv
        src = open_webcam()

        with open(src, 'r') as file:
            # Read each line
            content = file.readlines()[1:]
            for line in content:
                student = int(line.split(',')[0])

                # Search for related student
                for attendance in attendance_list:
                    if attendance['info_url'].endswith(f'/{cc}/{student}/'):
                        data = {
                            'status': True
                        }
                        response = requests.put(attendance['info_url'], json=data, headers=headers)
                        print(f'[{response.status_code}] {student} marked.')

    except Exception as e:
        print(e)
