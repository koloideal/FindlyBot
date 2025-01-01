import hashlib


def req_to_hash(req: str) -> str:
    hash_object = hashlib.sha256()
    hash_object.update(req.encode("utf-8"))
    hex_dig: str = hash_object.hexdigest()

    return hex_dig


s = req_to_hash('http://127.0.0.1:5050/api/search?q=realme+q5&ms=40&on=on&nf=on&pf=on')
print(s)
print(len(s))
