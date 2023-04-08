import numpy as np
import cv2


def NMS(boxes, class_ids, confidences, overlapThresh = 0.5):

    boxes = np.asarray(boxes)
    class_ids = np.asarray(class_ids)
    confidences = np.asarray(confidences)

    # Return empty lists, if no boxes given
    if len(boxes) == 0:
        return [], [], []

    x1 = boxes[:, 0] - (boxes[:, 2] / 2)  # x coordinate of the top-left corner
    y1 = boxes[:, 1] - (boxes[:, 3] / 2)  # y coordinate of the top-left corner
    x2 = boxes[:, 0] + (boxes[:, 2] / 2)  # x coordinate of the bottom-right corner
    y2 = boxes[:, 1] + (boxes[:, 3] / 2)  # y coordinate of the bottom-right corner

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)

    indices = np.arange(len(x1))
    for i, box in enumerate(boxes):
        # Create temporary indices
        temp_indices = indices[indices != i]
        # Find out the coordinates of the intersection box
        xx1 = np.maximum(box[0] - (box[2] / 2), boxes[temp_indices, 0] - (boxes[temp_indices, 2] / 2))
        yy1 = np.maximum(box[1] - (box[3] / 2), boxes[temp_indices, 1] - (boxes[temp_indices, 3] / 2))
        xx2 = np.minimum(box[0] + (box[2] / 2), boxes[temp_indices, 0] + (boxes[temp_indices, 2] / 2))
        yy2 = np.minimum(box[1] + (box[3] / 2), boxes[temp_indices, 1] + (boxes[temp_indices, 3] / 2))

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # compute the ratio of overlap
        overlap = (w * h) / areas[temp_indices]
        # if overlapping greater than our threshold, remove the bounding box
        if np.any(overlap) > overlapThresh:
            indices = indices[indices != i]

    # return only the boxes at the remaining indices
    return boxes[indices], class_ids[indices], confidences[indices]


def get_outputs(net):

    layer_names = net.getLayerNames()

    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    outs = net.forward(output_layers)

    outs = [c for out in outs for c in out if c[4] > 0.1]

    return outs


def draw(bbox, img):

    xc, yc, w, h = bbox
    img = cv2.rectangle(img,
                        (xc - int(w / 2), yc - int(h / 2)),
                        (xc + int(w / 2), yc + int(h / 2)),
                        (0, 255, 0), 20)

    return img



from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage 
import os
import threading
from django.conf import settings
from app.settings import BASE_DIR
from decouple import config
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()


    @staticmethod
    def otp_keygen(email):
        return f"{email}-{settings.SECRET_KEY}"

    @staticmethod
    def send_email(email, subject, message,instance=None,img_path=None):
        if(instance.created_by==None):
            try:
                body_html = f'''
                <html>
                    <body>
                        <h2>Admin Survelliance</h2>
                        <p>License plate text : {instance.license_plate_text}</p>
                        <p>Entry time : {instance.created_at}</p>
                    </body>
                </html>
                '''
            except : 
                body_html = f'''
                <html>
                    <body>
                        <h2>Admin Survelliance</h2>
                        <p>License plate text : {instance.license_plate_text}</p>
                        <p>Entry time : {instance.created_at}</p>
                    </body>
                </html>
                '''
        else:
            try:
                body_html = f'''
                <html>
                    <body>
                        <h2>Admin Survelliance</h2>
                        <p>License plate text : {instance.license_plate_text}</p>
                        <p>Entry time : {instance.created_at}</p>
                      
                    </body>
                </html>
                '''
            except:
                body_html = f'''
            <html>
                <body>
                    <h2>Admin Survelliance</h2>
                    <p>License plate text : {instance.license_plate_text}</p>
                    <p>Entry time : {instance.created_at}</p>
                </body>
            </html>
            '''

        msg = EmailMultiAlternatives(
            to=[email], 
            body=message, 
            subject=subject, 
            from_email=config('EMAIL_HOST_USER')
        )

        msg.mixed_subtype = 'related'
        msg.attach_alternative(body_html, "text/html")
        if img_path :
            image_name=img_path.split("/")[-1]
            
            with open(img_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<{name}>'.format(name=image_name))
                img.add_header('Content-Disposition', 'inline', filename=image_name)
            msg.attach(img)

        EmailThread(msg).start()
    
