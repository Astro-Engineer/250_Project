import matplotlib.pyplot as plt
import numpy as np

userinput = input('Choose a number 1-3:\n1 for: \n2 for: \n3 for: \n')

if userinput == "1":

    xpoints = np.array([0, 6])
    ypoints = np.array([0, 250])

    plt.plot(xpoints, ypoints)
    plt.ylim([0, 700])
    plt.xlabel("X-Label")
    plt.ylabel("Y-Label")
    plt.title("Title")
    plt.savefig("Sample One")
    print("ONE DONE")
    
elif userinput == "2":
    xpoints = np.array([0, 10])
    ypoints = np.array([0, 500])

    plt.plot(xpoints, ypoints)
    plt.ylim([0, 700])
    plt.xlabel("X-Label")
    plt.ylabel("Y-Label")
    plt.title("Title")
    plt.savefig("Sample Two")
    print("TWO COMPLETE")
    
elif userinput == "3":
    xpoints = np.array([0, 4])
    ypoints = np.array([0, 100])

    plt.plot(xpoints, ypoints)
    plt.ylim([0, 700])
    plt.xlabel("X-Label")
    plt.ylabel("Y-Label")
    plt.title("Title")
    plt.savefig("Sample 3")
    print("THREE WEE-HEE")
    
else:
    print("Not within the bounds smh")