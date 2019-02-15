import subprocess
from datetime import datetime

import boto3


def takePicture():
    filename = datetime.now().strftime('%Y_%m_%d__%H_%M_%S') + ".jpg"
    subprocess.call("fswebcam -r 1280x720 --no-banner " + filename, shell=True)
    return filename


def uploadToS3(filepath):
    s3 = boto3.resource('s3')
    uploadPath = "pickups/" + filepath.split("/")[-1]
    s3.meta.client.upload_file(filepath, 'amazotgo', uploadPath)
    return uploadPath


def recognize(filepath):
    bucket = 'amazotgo'
    collectionId = 'amazotgo_users'
    threshold = 70
    maxFaces = 2
    client = boto3.client('rekognition')
    s3 = boto3.client('s3')

    response = client.search_faces_by_image(CollectionId=collectionId,
                                            Image={'S3Object': {'Bucket': bucket, 'Name': filepath}},
                                            FaceMatchThreshold=threshold,
                                            MaxFaces=maxFaces)

    faceMatches = response['FaceMatches']

    print('Matching faces')
    for match in faceMatches:
        print('FaceId:' + match['Face']['FaceId'])
        print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        print('FaceId:' + match['Face']['FaceId'])
        key = match['Face']['ExternalImageId']

        response = s3.get_object_tagging(Bucket=bucket, Key=key)

        print(response)
        print(response['TagSet'])
        if response['TagSet']["name"]:
            print("Found user ---------> ", response['TagSet']["name"])


if __name__ == '__main__':
    while True:
        a = raw_input("Press enter to take a pic")
        picture = takePicture()
        if picture:
            print(picture)
            s3Filepath = uploadToS3(picture)
            print(s3Filepath)
            id = recognize(s3Filepath)

        else:
            print("Failed to take picture")
