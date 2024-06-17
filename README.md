Šajā repo glabājas Edgara Laķa (el23102) darbi Python 3.10.13 vidē
## Datoru tīkli II 3. mājasdarbs. Tīkla lietotne: **Uzdevumu saraksts**
14.06.2024

Video demonstrācija https://youtu.be/snRZjjf7iFU
Uzdevumu saraksta lietotne veidota no diviem Python skriptiem - server.py un client.py. Tā nodrošina komunikāciju starp server un client uz 10101 porta. Client savienojas ar serveri caur "loopback" IPv4 adresi 127.0.0.1.

## Palaišanas instrukcija
1. Vispirms palaiž serveri ar `python server.py`, tad client `python client.py`. Tiek izveidots jauns TCP/IP socket ar TCP protokolu (Socket Kind - Stream)

2. Ar client komandas rindas ievadi var veikt sekojošas uzdevumu saraksta izmaiņas
    1. ADD pievieno uzdevumu

    `ADD Piezvanīt Andrim`

    1. DELETE dzēš uzdevumu
    
    `DELETE 0`

    1. LIST sarindo uzdevumus

    `LIST`



## Lietišķā Kriptogrāfija. 2. mājasdarbs - **X.509 sertifikāts un RSA**
10.06.2024

### Palaišanas instrukcija:

1. Izveidojiet ziņojuma teksta failu ar šifrējamo ziņu vai jebkādu baitu saturošu failu. Doti divi piemēri input.bin un input.txt.
2. Ģenerējiet izvēlētā izmēra baitu virkni un saglabāt to .bin failā:

`python generate_keys.py`
 
 Rezultātā tiek izveidots input.bin fails, kuru izmanto kā ievadi programmai 3_sifresana.py.

3. Veic trīs secīgus soļus - Python programmas:
    1. Izveido X.509 sertifikātu, balstoties uz informāciju, kura norādīta informacija.txt failā

    `python 1_izveido_X_509.py`

    1. Verificē X.509 saknes sertifikātu, pārbaudot, vai izdevējs un parakstītājs ir identisks, un sakrīt punliskās atslēgas. 

    `python 2_verifikacija.py`

    1. Faila šifrēšana un atšifrēšana ar RSA un OAEP padding metodi. Par ievadi tiek ņemts input.bin fails. 

    `python 3_sifresana.py`

    Rezultātā tiek izveidots šifrēts fails encrypted_message.bin, kurš tiek atšifrēts uz output.bin. Ja ieejas faila izmērs pārsniedz teorētiski pieļaujamo pēc atslēgas izmēra (šeit 2048 biti), tiek atgriezts paziņojums ar maksimālo ieejas faila izmēru. Jāņem vērā, ka SHA-256 hash aizņem 2*32 baitus un OAEP vēl 2 baitus.


## Lietišķā Kriptogrāfija. 1. mājasdarbs - **Block Ciphers and Chaining Modes**
1.06.2024

Alternatīva versija [Google Colab vidē](https://colab.research.google.com/drive/1ZkdVpOyzT0fQ1PF_miPOyYXtQZZXlawF?usp=sharing)

### Palaišanas instrukcija:

1. Izveidojiet ziņojuma teksta failu ar šifrējamo ziņu vai jebkādu baitu saturošu failu. Doti divi piemēri input.bin un input.txt.
2. Ģenerējiet šifrēšanas un MAC atslēgas ar Python skriptu generate_keys.py. Ar šo programmu iespējams ģenerēt arī izvēlētā izmēra baitu virkni un saglabāt to failā

`python generate_keys.py`
 
 Rezultātā tiek izveidots key.bin fails, kurš satur abas atslēgas heksidecimālā formātā, un input.bin fails.

3. Šifrēšanas skripts jāpalaiž ar četriem komandas rindas karogiem:
    - Šifrēšanai vai atšifrēšanai lietot: "encrypt" vai "decrypt"
    - Chaining veidam lietot: "cbc" vai "cfb"
    - Atslēgu fails: key.bin
    - Izejas un ieejas failu nosaukums (vēlams ar attiecīgu paplašinājumu, piemēram .bin vai .txt)

Piemēri:
Šifrēšana **CBC** veidā

`python AES.py encrypt cbc input.bin key.bin encrypted_cbc.bin`

Atšifrēšana **CBC** veidā

`python AES.py decrypt cbc encrypted_cbc.bin key.bin decrypted_cbc_file.bin`

Šifrēšana **CFB** veidā

`python AES.py encrypt cfb input.bin key.bin encrypted_cfb.bin`

Atšifrēšana **CFB**  veidā

`python AES.py decrypt cfb encrypted_cfb.bin key.bin decrypted_cfb_file.bin`


