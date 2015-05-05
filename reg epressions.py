def main():

    x = (input("Enter a value consisting of zeros and ones:"))
    a = x
    print("\n")
    print("Checking if your input has only 2 consecutive zeros...")
    counter = 0
    for i in x:
        if i == '0':
            counter = counter + 1
            if counter == 3:
                counter = 0
        elif i == '1':
            if counter == 2 and i == '1':
                print("Your input has 2 consecutive zeros!")
                break
            elif counter == 1 and i == '1':
                counter = 0
            else:
                continue
    if counter < 2:
        print("Your input does not have 2 consecutive zeros.")

    elif counter == 2:
        print("Your input has 2 consecutive zeros!")


    print("\n")
    print("Checking if your input has 2 consecutive zeros or more...")

    count = 0
    for i in a:
        if i == '0':
            count = count + 1

        elif i == '1':
            if count >= 2:
                print("Your input has 2 consecutive zeros!")
                break
            else:
                count = 0

    if count < 2:
        print("Your input does not have 2 consecutive zeros.")
        
    elif count >= 2:
        print("Your input has 2 consecutive zeros or more!")


main()
