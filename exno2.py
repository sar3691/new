#detail collector using control statement & loops 
voters=[]
while True:
    #name
    while True:
        fname=input("enter the first name\n\t" )
        if fname !="":
            break
        else:
            print("enter the first name  \n\t")
    mname=input("enter the mid name \n\t")
    while True:
        lname=input("enter the last name \n\t")
        if lname !="":
            break
        else:
            print("enter the last name  \n\t")
    name=fname+mname+lname
    #age
    age =input("enter the age\n\t")
    if int(age)<18:
        print("not ablicable\n\t")
        continue
    #address
    addr=input("enter the address\n\t")
    #mobile number
    while True:
        phono=input("enter the mobile number \n\t")
        if len(phono)!= 10:
            print("wrong mobile number please re enter \n\t")
        else:
            break
    #aadhar id
    aadhar=input("enter the aadhar number  \n\t")
    #email
    email=input("enter the email id \n\t")
    #append to voters
    b=[name,age,addr,phono,aadhar,email]
    voters.append(b)
    if input("do you want to break yes/no ?\n\t").lower()=="yes":
        print("\n\n\n\n")
        break
        
info=["name","age","address","aadhar","email"]
f=open("new.txt",'a')
for voter in voters:
    for inf,detail in zip(info,voter):
        print(inf.center(10),":\t",detail)
        f.write(inf.center(10)+":\t"+detail+"\t,")
    f.write("\n")

    print("\n\n","----------"*5,"\n\n")
f.close()

if input("do you want to see the all details ye / no ? \n\t").lower()=="yes":
    f=open("new.txt","r")
    for i in f.read():
        print(i,end="")
    f.close()
