# This will generate a number with millions of digits
#huge_number = 999999999999999999 ** 100000  

# If you want to push it further in a loop:
n = 2
while True:
    n = n ** 2  # Grows super-exponentially until memory/CPU maxes out
    print(len(str(n))) # Prints the growing digit length
