import base64

class CipherEngine:
    def __init__(self, key=None): # 👈 أصبح يتقبل أي نوع مفتاح
        self.key = key
        self.vocab = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # ================= CAESAR =================
    def caesar_encrypt(self, text):
        result = ""
        for c in text:
            if c in self.vocab:
                i = self.vocab.index(c)
                result += self.vocab[(i + int(self.key)) % len(self.vocab)]
            else:
                result += c
        return result

    def caesar_decrypt(self, text):
        result = ""
        for c in text:
            if c in self.vocab:
                i = self.vocab.index(c)
                result += self.vocab[(i - int(self.key)) % len(self.vocab)]
            else:
                result += c
        return result

    # ================= REVERSE =================
    def reverse_encrypt(self, text):
        return text[::-1]

    def reverse_decrypt(self, text):
        return text[::-1]

    # ================= XOR =================
    def xor(self, text):
        return ''.join(chr(ord(c) ^ int(self.key)) for c in text)

    # ================= ROT13 =================
    def rot13(self, text):
        result = ""
        for c in text:
            if 'a' <= c <= 'z':
                result += chr((ord(c) - 97 + 13) % 26 + 97)
            elif 'A' <= c <= 'Z':
                result += chr((ord(c) - 65 + 13) % 26 + 65)
            else:
                result += c
        return result

    # ================= BASE64 =================
    def base64_encode(self, text):
        return base64.b64encode(text.encode()).decode()

    def base64_decode(self, text):
        try:
            return base64.b64decode(text.encode()).decode()
        except:
            return "Invalid Base64 Data"

    # ================= VIGENERE =================
    # 👈 تم تعديل دالة فيجنير لتقرأ المفتاح من self.key مباشرة
    def vigenere_encrypt(self, text):
        k = str(self.key).lower()
        result = ""
        for i, c in enumerate(text):
            shift = ord(k[i % len(k)]) % 26
            result += chr((ord(c) + shift) % 256)
        return result

    def vigenere_decrypt(self, text):
        k = str(self.key).lower()
        result = ""
        for i, c in enumerate(text):
            shift = ord(k[i % len(k)]) % 26
            result += chr((ord(c) - shift) % 256)
        return result
