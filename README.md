# lu-darbi
Šajā repo glabājas Edgara Laķa (el23102) darbi


## Lietišķā Kriptogrāfija. 1. mājasdarbs - **Block Ciphers and Chaining Modes**
Darbs sagatavots 1.06.2024, izstrādājot Python 3.10.13 versijā
[Google Colab vidē](https://colab.research.google.com/drive/1ZkdVpOyzT0fQ1PF_miPOyYXtQZZXlawF?usp=sharing)

###Palaišanas instrukcija:

1. Izveidojiet ziņojuma failu input.txt ar šifrējamo ziņu vai izmainiet doto piemēra faila tekstu.
2. Ģenerējiet šifrēšanas un MAC atslēgas ar Python skriptu generate_keys.py.
`python generate_keys.py`
 Tiek izveidots key.bin fails, kurš satur abas atslēgas heksidecimālā formātā.
3. Šifrēšanas skripts jāpalaiž ar četriem komandas rindas karogiem:
    Šifrēšanai vai atšifrēšanai lietot: "encrypt" vai "decrypt"
    Chaining veidam lietot: "cbc" vai "cfb"
    Atslēgu fails: key.bin
    Izejas faila nosaukums ar .bin papildinājumu šifrēšanas komandai vai .txt atšifrēšanas komandai.

Piemēri:
Šifrēšana **CBC** veidā
`python script.py encrypt cbc input.txt key.bin encrypted_cbc.bin`

Atšifrēšana**CBC** veidā
`python script.py decrypt cbc encrypted_cbc.bin key.bin decrypted_cbc.txt`

Šifrēšana **CFB** veidā
`python script.py encrypt cfb input.txt key.bin encrypted_cfb.bin`

Atšifrēšana **CFB**  veidā
`python script.py decrypt cfb encrypted_cfb.bin key.bin decrypted_cfb.txt`


