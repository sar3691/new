#function for get and store a student information 
def student():
    detail={}
    a=[]
    rno=input("enter the student roll number\n\t\t")
    name=input("enter the student name\n\t\t")
    for i in range(1,4):
        a.append(int(input(f"enter the sub one mark{i}\n\t\t")))
    avg=round((sum(a)/len(a)),2)
    
    #calculation
    rank= "A+" if avg>90 else "A" if avg>85 else "B+" if avg>80 else "B" if avg>70 else "C" if avg>50 else "D"
    res= "pass" if all(i>50 for i in a) else "fail"
    b="average mark ="+str(avg)+" rank = "+rank+" result ="+res
    detail[rno]=name,a,b
    
    return detail


li=[]
for j in range(0,int(input("how many details you want to enter \n\n\t"))):
    detail=student()
    li.append(detail)
    
#convert to tuple for read only
tup=tuple(li)
for i in tup:
    print(i)

