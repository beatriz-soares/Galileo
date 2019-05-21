import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    import csv
    import matplotlib.pyplot as plt

    with open("pontos.csv", "r") as pontos:
        pontos = pontos.read()
        pontos = pontos.replace('"', '').split("\n")[:-1]
        lista = [int(p) for p in pontos][-20:]

    # Limit x and y lists to 20 items
    ys = lista

    # Draw x and y lists
    ax.clear()
    ax.plot(ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Som')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=500)
plt.show()
