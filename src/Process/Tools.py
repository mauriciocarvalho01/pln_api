import base64

class Tools:
    def encodeBase64(text):
        text = text.encode("ascii", 'ignore')
        hash = base64.b64encode(text)
        hash = hash.decode("ascii")
        return hash.replace("/", "")