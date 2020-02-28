# Encyrption using Vigenere cryptosystem.
# The cryptanalylsis is based exclusively on probabilities, therefore human intervention is required for a more accurate interpretation.
# Key length computed using the index of coincidence (still, probabilistic).
import sys
import string

alphabet = string.ascii_lowercase
alphabet = list(alphabet)
file = open("result.txt", "w+")
data = open("in.txt", "r+")
keyFile = open("key.txt", "r+")
plainText = data.read()
data.seek(len(plainText))
key = keyFile.read()
englishFrequencies = [8.04, 1.5, 3.34, 3.79, 12.5, 2.2, 2, 5, 7.6, 0.15, 0.75, 4, 2.5, 7.23, 8, 2, 0.1, 6.196, 6.5, 9,
                      2.73, 1, 1.65, 0.15, 2, 0.074];
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]


def filter(originalText):
    new = originalText.casefold()
    new = new.replace(' ', '')
    new = new.replace('.', '')
    new = new.replace(',', '')
    new = new.replace('!', '')
    new = new.replace('?', '')
    new = new.replace('-', '')
    new = new.replace(':', '')
    new = new.replace('(', '')
    new = new.replace(')', '')
    return new


def getLetter(index):
    return alphabet[index]


def getOrd(letter):
    for index in range(0, 26):
        if (letter == alphabet[index]):
            return index


def translate(plainText):
    encoding = []
    for i in range(0, len(plainText) - 1):
        encoding.append(getOrd(plainText[i]))
    return encoding


def repeatUntil(s, wanted):
    return (s * (wanted // len(s) + 1))[:wanted]


def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1


def encrypt(trText, trKey):
    tempText = []
    for i in range(0, len(trText)):
        tempText.append((trText[i] + trKey[i]) % 26)
    return tempText


def formatEnc(tempText):
    encryptedText = []
    for j in range(0, len(tempText)):
        encryptedText.append(getLetter(tempText[j]))
    return encryptedText


# decrypts using a known key
def decrypt(encText, key):
    decryptedText = []
    for i in range(0, len(encText)):
        decryptedText.append((encText[i] - key[i]) % 26)
    for j in range(0, len(decryptedText)):
        decryptedText[j] = getLetter(decryptedText[j])
    return decryptedText


def extract(text, start, number):
    new = []
    for i in range(start, len(text), number):
        new.append(text[i])
    # file.write(new)
    return new


# computes the index of coincidence for a given sequence
def indexOfCoincidence(self):
    num = 0.0
    occurs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for val in range(0, len(self)):
        occurs[getOrd(self[val])] += 1
    # file.write(occurs)
    for i in range(0, len(occurs)):
        sums[i] = occurs[i] * (occurs[i] - 1)
    # file.write(sums)
    den = sum(occurs)
    num = sum(sums)
    if den == 0.0:
        return 0.0
    else:
        return num / (den * (den - 1))


# tries sequences until it reaches the maximum index of coincidence (looks for keys with a length at most $seek)
def getKeyLength(text, seek):
    maximum = 0.0
    length = 0
    for i in range(1, seek):
        for j in range(1, seek - 1):
            temp = extract(text, j, i)
            ic = indexOfCoincidence(temp)
            if ic > maximum:
                maximum = ic
                length = i
    return length


def shift(text, number):
    visited = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for index in range(0, len(text)):
        if visited[getOrd(text[index])] == 0:
            text = text.replace(text[index], alphabet[getOrd(text[index]) - number])
            visited[getOrd(text[index])] = 1
    return text


def getMaxRatio(sequence):
    occurs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    newSequence = []
    for val in range(0, len(sequence)):
        occurs[getOrd(sequence[val])] += 1
    for k in range(0, len(englishFrequencies)):
        newSequence.append(englishFrequencies[k] * occurs[k] / len(occurs) * 0.01)
    occurs.clear()
    return sum(newSequence)


def translateBack(sequence):
    maxTotal = 0
    sequence = listToString(sequence)
    copy = sequence
    index = 0
    for i in range(0, 25):
        if maxTotal < getMaxRatio(sequence):
            maxTotal = getMaxRatio(sequence)
            sequence = shift(sequence, 1)
            index = i
        else:
            sequence = shift(sequence, 1)
    print(maxTotal)
    print(index)
    return shift(copy, index)


def main():
    file.write("Original text:\n")
    file.write(plainText)
    trText = translate(filter(plainText))
    trKey = translate(repeatUntil(key, len(filter(plainText))))
    encText = formatEnc(encrypt(trText, trKey))
    file.write("\nEncrypted text:\n")
    file.write(listToString(encText))
    file.write("\nDecrypted text:\n")
    file.write(listToString(decrypt(encrypt(trText, trKey), trKey)))
    file.write("\nMost likely length of the key:\n")
    file.write(str(getKeyLength(encText, 10)))
    file.write("\nCaesar code (should be read by columns rather than lines):\n")
    # for i in range(0, getKeyLength(encText, 10)):
    # translateBack(extract(encText, i, getKeyLength(encText, 10)))
    # file.write('\n')
    temp = extract(encText, 0, 8)
    temp = translateBack(temp)
    file.write(temp)
    file.write("\n")
    for i in range(1, getKeyLength(encText, 10)):
        temp = extract(encText, i, 8)
        temp = translateBack(temp)
        file.write(temp)
        file.write("\n")
    file.close()


main()
