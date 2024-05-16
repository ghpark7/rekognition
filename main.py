import boto3

def detect_faces(image):
    rekognition = boto3.client("rekognition")
    response = rekognition.detect_faces(
        Image={
            "S3Object": {
                "Bucket": "ghprekognition",
                "Name": image,
            }
        },
        Attributes=['ALL'],
    )

    return response['FaceDetails']

def get_face_features(face_details):
    features = {}
    for detail in face_details:
        features['Mustache'] = 1 if detail['Mustache']['Value'] else 0
        features['Beard'] = 1 if detail['Beard']['Value'] else 0
    return features

# S3 버킷에서 이미지 리스트를 가져옵니다.
s3 = boto3.resource('s3')
bucket = s3.Bucket('ghprekognition')

images = [obj.key for obj in bucket.objects.filter(Prefix='Tom Hanks/')]

# 각 이미지에 대해 얼굴을 감지하고 특징을 출력합니다.
for image in images:
    face_details = detect_faces(image)
    features = get_face_features(face_details)
    print(f"{image} - Mustache: {features['Mustache']}, Beard: {features['Beard']}")