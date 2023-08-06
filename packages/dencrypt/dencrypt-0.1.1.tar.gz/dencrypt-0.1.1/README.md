# DENcrypt
#### **v.0.1.1**

Módulo criado com o objetivo de facilitar a criptografia/descriptografia de textos e arquivos.

Utiliza como base as criptografias: 
- RSA (Assimétrica)
  - Encrypt (Chave Pública)/Decrypt (Chave Privada)
  - Lento; Uso recomendado em conteúdo com tamanho máximo de 256 bytes

- Fernet (Simétrica)
  - EncryptFile (Chave Única)/DecryptFile (Chave Única)
  - Rápido; Uso recomendado para arquivos



# Requisitos

```python
python = "^3.9"
rsa = "^4.7.2"
cryptography = "^35.0.0"
```



# Instalação

```
pip install dencrypt
```



# Como Funciona - Via Código

`config. inicial do projeto`

```
exemplo/
├─ arquivos/
   ├─ dados1.txt
   ├─ dados2.csv
├─ arquivos-crip/
├─ keys/
├─ main.py
```
`main.py`
```python
from dencrypt import (
    Crypt, # Gera Chaves Pública/Privada RSA e Simétrica Fernet 
    Encrypt, Decrypt, # Realiza En/Decriptação RSA
    EncryptFile, DecryptFile # Realiza En/Decriptação Fernet
)

# 1. Gerando as Chaves
cr = Crypt().generate_all_keys()
cr.pubkey       # b'-----BEGIN RSA PUBLIC KEY-----  MIIBCgKCAQEAhBF7c...'
cr.privkey      # b'-----BEGIN RSA PRIVATE KEY----- MIIEqQIBAAKCAQEAd...'
cr.symmetrickey # b'KqqI5Ncke0TSzBJFrE0SM3xuHz11tv689A1PhmkewkE='

# 1.1. Salvando arquivos das chaves
cr.save_all_keys(location="keys/")
```
```
exemplo/
├─ arquivos/
   ├─ dados1.txt
   ├─ dados2.csv
├─ arquivos-crip/
├─ keys/
   ├─ privatekey.key
   ├─ publickey.key
   ├─ symmetrickey.key
├─ main.py
```
```python
# 2. Criptografando Arquivos com a Chave Simétrica

# 2.1. Arquivo dados1.txt
encr = EncryptFile("arquivos/dados1.txt", key="keys/symmetrickey.key")
encr.content # Conteúdo Original: b'Teste 1\nTeste 2\nTest...'
encr.get()   # Conteúdo Criptog.: b'\xc3\x8a\xc3\xa2\xc3\xaa\xc3\xae...'

# Salvando arquivo com conteúdo criptografado
encr.save("arquivos-crip/dados1.txt.dencrypt") 

# 2.2. Arquivo dados2.csv
encr = EncryptFile("arquivos/dados2.csv", key="keys/symmetrickey.key")
encr.save("arquivos-crip/dados2.csv.dencrypt")
```
```
exemplo/
├─ arquivos/
   ├─ dados1.txt
   ├─ dados2.csv
├─ arquivos-crip/
   ├─ dados1.txt.dencrypt
   ├─ dados2.csv.dencrypt
├─ keys/
   ├─ privatekey.key
   ├─ publickey.key
   ├─ symmetrickey.key
├─ main.py
```
```python
# 3. Criptografando Chave Simétrica com Chave Pública RSA
encr = Encrypt("keys/symmetrickey.key", pubkey="keys/publickey.key")
encr.save("arquivos-crip/secreta.key")
```
```
├─ arquivos-crip/
   ├─ secreta.key
   ├─ dados1.txt.dencrypt
   ├─ dados2.csv.dencrypt
```
```python
# 4. Descriptografando Arquivos

# 4.1. Descriptografando Chave Simétrica com Chave Privada RSA
skey = Decrypt("arquivos-crip/secreta.key", privkey="keys/privatekey.key")
skey = skey.get() # b'KqqI5Ncke0TSzBJFrE0SM3xuHz11tv689A1PhmkewkE='

#  4.2. Descriptografando dados1.txt.dencrypt
decr = DecryptFile("arquivos-crip/dados1.txt.dencrypt", key=skey)
decr.save("arquivos-crip/dados1.txt")

#  4.3. Descriptografando dados2.csv.dencrypt
decr = DecryptFile("arquivos-crip/dados2.csv.dencrypt", key=skey)
decr.save("arquivos-crip/dados2.csv")
```
```
exemplo/
├─ arquivos/
   ├─ dados1.txt
   ├─ dados2.csv
├─ arquivos-crip/
   ├─ secreta.key
   ├─ dados1.txt
   ├─ dados1.txt.dencrypt
   ├─ dados2.csv
   ├─ dados2.csv.dencrypt
├─ keys/
   ├─ privatekey.key
   ├─ publickey.key
   ├─ symmetrickey.key
├─ main.py
```
```python
# 5. Realizando comparação de conteúdo
with (
    open("arquivos/dados1.txt") as d1_original,
    open("arquivos/dados2.csv") as d2_original,
    open("arquivos-crip/dados1.txt.dencrypt") as d1_crip,
    open("arquivos-crip/dados2.csv.dencrypt") as d2_crip,
    open("arquivos-crip/dados1.txt") as d1_decrip,
    open("arquivos-crip/dados2.csv") as d2_decrip
):
    # Reads
    d1_original_read = d1_original.read()
    d2_original_read = d2_original.read()
    d1_crip_read = d1_crip.read()
    d2_crip_read = d2_crip.read()
    d1_decrip_read = d1_decrip.read()
    d2_decrip_read = d2_decrip.read()

    # Original com Criptografado
    d1_original_read == d1_crip_read # False
    d2_original_read == d2_crip_read # False

    # Original com Descriptografado
    d1_original_read == d1_decrip_read # True
    d2_original_read == d2_decrip_read # True

```

Download: [examples/exemplo.zip](examples/exemplo.zip)



# Como Funciona - Via CLI

```
Exemplos de uso:
    + Verificando Versão
        > dencrypt --version | > dencrypt -v

    + Gerando chaves
        - Pública RSA (2048), Privada RSA (2048) e Simétrica Fernet
            > dencrypt --keys | > dencrypt -k

        - Apenas Simétrica Fernet
            > dencrypt --keys --norsa | > dencrypt -k -nr

        - Apenas Pública/Privada RSA (Tamanho 1024)
            > dencrypt --keys --nofer -size 1024 | > dencrypt -k -nf -s 1024
        
        - Pública/Privada RSA (2048) e Simétrica Fernet escolhendo local para salvar
            > dencrypt --keys --location "C:/user/User/Desktop" | > dencrypt -l "C:/user/User/Desktop"
        
        - Pú./Pr. RSA (2048) e Sim. Fer. adicionando prefixo e sufixo e alterando 
          extensão nos nomes dos arquivos das chaves
            > dencrypt --keys --prefix "B1_" --sufix "_1B" --ext ".chave" 
            > dencrypt -k -px "B1_" -sx "_1B" -e ".chave"
            
            Exemplo de resultado padrão sem aplicar "-px", "-sx" e "-e"
                - privatekey.key
                - publickey.key
                - symmetrickey.key
            
            Exemplo de resultado aplicando "-px", "-sx" e "-e"
                - B1_privatekey_1B.chave
                - B1_publickey_1B.chave
                - B1_symmetrickey_1B.chave

    + Encriptando arquivos/conteúdo
        - Com chave Simétrica Fernet
            > dencrypt --encrypt --input "arquivo.jpg" --skey "symmetrickey.key"
                        -enc      -i                    -sk
            Será gerado um novo arquivo chamado "arquivo.jpg.dencrypt"

        - Com chave Pública RSA
            > dencrypt -enc -i "arquivo.jpg" --pkey "publickey.key"
                                              -pk
            Será gerado um novo arquivo chamado "arquivo.jpg.dencrypt"
            ! Esta encriptação é limitada ao seu tamanho. Caso a chave seja de 
              2048 bits (Padrão), suportará um conteúdo de no máximo 256 bytes

        - Texto
            > ... -i "Texto Secreto" -sk ... --forcetext 
                                              -ft
            Será gerado um novo arquivo chamado "Texto Secreto.dencrypt" com o texto 
              criptografado de conteúdo
            Porém como podemos observar, o nome do arquivo se mantém com o do conteúdo
              secreto, abaixo veja exemplos de como renomear o arquivo com `output`      
        
        - Utilizando `--ext` e `--output` para salvar arquivo com nome diferente
            ? DICA: `--output` possui alguns format strings
                %FILENAME = Retorna o nome completo do arquivo original - Ex: "arquivo.jpg"
                %FILEEXT  = Retorna apenas a extensão do arquivo original - Ex: ".jpg"
                %FILE     = Retorna o nome do arquivo original - Ex: "arquivo"
                %EXT"     = Retorna a extensão enviada através do `--ext` - Por padrão é ".dencrypt"
                %DATETIME = Retorna a data do momento, seguinto o formado: ddmmaaaahhmmss 
                %RAND"    = Retorna um número aleatório entre 100.000 e 999.999
            
            > ... --ext ".louco" --output "a"
                   -e             -o
            Será gerado um novo arquivo chamado "a.louco" em vez de "arquivo.jpg.dencrypt"
            
            > ... -e ".louco" -o "%FILENAME%EXT"  |  > ... -e ".teste" -o "%FILE_%DATETIME%EXT"
            Resultará em "arquivo.jpg.louco"      |  Resultará em "arquivo_281020210252.teste"
            
            > ... --ext ".abcabc" --output "%RAND%EXT"  |  > ... --ext ".abcabc"
            Resultará em "734582.abcabc"                |  Resultará em "arquivo.jpg.abcabc" 
        
        - Múltiplos arquivos
          > dencrypt --encrypt --allfiles --skey "symmetrickey.key"
                                -af
          Todos arquivos da pasta atual serão criptografados e salvos em uma 
          nova pasta (criada no mesmo diretório) chamada "dencrypt_encrypt_202110280323" 
          com a data atual no final
          O nome dos novos arquivos seguirá o formato "nome.ext.dencrypt", Ex: "imagem.jpg.dencrypt"
          ! Os arquivos originais ainda serão mantidos

          > ... --allfiles ... --extignore "jpg, png, py"
                                -eig
          Realizará o mesmo processo anterior, porém ignorando arquivos com as extensões informadas
          .jpg, .png e .py

        - Comandos persistentes
          --replace ou -r = Força a substituição de qualquer arquivo existente com o mesmo nome
          --force ou -f   = Ignora qualquer aviso, e avança automaticamente 

    + Decriptando arquivos/conteúdo
      - Funcionamento semelhante ao `--encrypt`, porém, agora deve ser passado via `--input`
        o arquivo já criptografado

      - Com chave Simétrica Fernet
        > dencrypt --decrypt --input "arquivo.jpg.dencrypt" --skey "symmetrickey.key"
                    -dec      -i                    -sk
        Será gerado um novo arquivo chamado "arquivo.jpg"

      - Com chave PRIVADA RSA
        > dencrypt -dec -i "arquivo.jpg.dencrypt" --pkey "privatekey.key"
                                                   -pk
        Será gerado um novo arquivo chamado "arquivo.jpg"

      ...
```
