import base64

decoded_data = base64.b64decode("S3pjZ0tEUTVPU2tnTmpRNUxUQXlMVGcxXw==")
decoded_data_1 = base64.b64decode(decoded_data)


print(decoded_data)
print(decoded_data_1)
