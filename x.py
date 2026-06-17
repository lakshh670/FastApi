arr=[1,2,3,4]
def rev_k(i,j,arr):
    while i<j:
        arr[i],arr[j]=arr[j],arr[i]
        i+=1
        j-=1
rev_k(0,1,arr)
rev_k(2,3,arr)
rev_k(0,3,arr)
print(arr)