import sys
import logging
import nodethread
from threading import Event

minNode = 0
maxNode = 0

nodes = []
shortcuts = []

def main(argv):
    global minNode, maxNode, nodes, shortcuts

    f = open(argv[0], "r")
    for line in f:
        if "key-space" in line:
            nextLine = f.readline()
            numberArray = nextLine.split(",") # Split by comma
            minNode = int(numberArray[0]) # Parse min and max node values
            maxNode = int(numberArray[1])
        if "nodes" in line:
            nextLine = f.readline()
            nodesArray = nextLine.split(",")
            for node in nodesArray:
                node = int(node)
                if node < minNode or node > maxNode: # Check if the node is in acceptable range
                    logging.warning("Node ID is not in acceptable range! Node ID: " + str(node))
                else:
                    nodes.append(node) # If is, add to the array
        if "shortcuts" in line:
            nextLine = f.readline()
            if nextLine == "\n": # For case if we do not have any shortcuts
                continue
            shortcutsArray = nextLine.split(",")
            for shortcut in shortcutsArray:
                splitShortcut = shortcut.split(":")
                shortcuts.append((int(splitShortcut[0]), int(splitShortcut[1])))

    f.close()

    print(minNode)
    print(maxNode)
    print(nodes)
    print(shortcuts)

    # Will create a separate thread for each node. Hold them in threadpool. The ring is completed in this section.
    threadPool = {}
    nodes.sort()

    # Adding successors and next successors
    for i, node in enumerate(nodes):
        threadPool[node] = nodethread.nodeThread(node)

        if i < len(nodes) - 1:
            threadPool[node].successor = nodes[i+1]
        else:
            threadPool[node].successor = nodes[0]

        if i < len(nodes) - 2:
            threadPool[node].nextSuccessor = nodes[i+2]
        else:
            if i == len(nodes) - 2:
                threadPool[node].nextSuccessor = nodes[0]
            else:
                threadPool[node].nextSuccessor = nodes[1]

    # Adding shortcuts
    for shortcut in shortcuts:
        threadPool[shortcut[0]].shortcuts.append(shortcut[1])

    try:
        while True:
            text = input("Choose next command (list, lookup, join, leave, shortcut)\n")

            # waiting for user input and act accordingly
            if ("list" in text):
                print("Sorry, not implemented\n")
            elif ("lookup" in text):
                print("Sorry, not implemented\n")
            elif ("join" in text):
                print("Sorry, not implemented\n")
            elif ("leave" in text):
                print("Sorry, not implemented\n")
            elif ("shortcut" in text):
                # Right now just adding the shortcuts to the list and appending to the right thread as well
                splitText = text.split()
                shortcut = splitText[1].split(":")
                if int(shortcut[0]) in nodes and int(shortcut[1]) in nodes:
                    shortcuts.append((int(shortcut[0]), int(shortcut[1])))
                    threadPool[(int(shortcut[0]))].shortcuts.append(int(shortcut[1]))
                    print(shortcuts)
                    print("OK\n")
                else:
                    logging.warning("There is no node with given ID\n")

            else:
                logging.warning("Please enter valid command!\n")

    except KeyboardInterrupt:
        # Exit all threads and wait
        for node in threadPool:
            threadPool[node].setRunning(False)
            threadPool[node].join()
        print("All threads closed!")

if __name__ == "__main__":
    main(sys.argv[1:])