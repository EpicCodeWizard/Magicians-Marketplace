import deso

desoMedia = deso.Media(publicKey="BC1YLgCpXwXsWQDwaXdodrRSgHrQaj5YUbfED13Syk2BCXNCQkrYzr2", seedHex="268767f212f12f4629b4d220ffa63350b1f225ef5d173f022af09d5a73e16815")

def upload_to_deso(openFile):
  urlResponse = desoMedia.uploadImage([("file", (openFile.name, openFile, "image/png"))])
  return urlResponse.json()["ImageURL"]