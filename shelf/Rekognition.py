import boto3

from Face import *
from User import *


class Rekognition:
    def __init__(self, bucket='amazotgo', collection_id='amazotgo_users', threshold=70, max_faces=1):
        self.bucket = bucket
        self.collection_id = collection_id
        self.threshold = threshold
        self.max_faces = max_faces

        self.rekognition = boto3.client('rekognition')
        self.s3_resource = boto3.resource('s3')
        self.s3_client = boto3.client('s3')

    def upload(self, file_path):
        upload_path = "pickups/" + file_path.split("/")[-1]
        self.s3_client.upload_file(file_path, 'amazotgo', upload_path)

    def recognize_users(self, file_path):
        response = self.rekognition.search_faces_by_image(
            CollectionId=self.collection_id,
            Image={'S3Object': {'Bucket': self.bucket, 'Name': file_path}},
            FaceMatchThreshold=self.threshold,
            MaxFaces=self.max_faces)
        face_matches = response['FaceMatches']

        users = []
        for match in face_matches:
            face = Face(match['Face']['FaceId'], match['Similarity'], match['Face']['ExternalImageId'])
            response = self.s3_client.get_object_tagging(Bucket=self.bucket, Key=face.external_id)

            values = dict()
            for tag in response['TagSet']:
                values[tag['Key']] = tag['Value']

            if 'name' in values and 'user' in values:
                user = User(face, values["name"], values['user'])
                users.append(user)
        return users
