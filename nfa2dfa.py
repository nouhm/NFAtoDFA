from graphviz import Digraph
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global vars to take input
statesString = ''
startStateString = ''
alphabetString = ''
finalStatesString = ''
deltaString = ''


# Creating the NFA Class that will include the NFA Transition Table
class NFA:
    # Constructor of the class to identify the quintuple of the NFA
    def __init__(self, numOfStates, qStates, numOfAlphabet, alphabets, startState,
                 numOfFinalStates, finalStates, numOfAllTransitions, allTransitions):
        self.numOfStates = numOfStates
        self.qStates = qStates
        self.numOfAlphabet = numOfAlphabet
        self.alphabets = alphabets

        # Adding epsilon alphabet to the list
        # and incrementing the alphabet count
        self.alphabets.append('e')
        self.numOfAlphabet += 1
        # Identifying the start state
        self.startState = startState
        # Identifying the number of final states.
        self.numOfFinalStates = numOfFinalStates
        # Identifying the final transition states.
        self.finalStates = finalStates
        # Identifying the number of transitions
        self.numOfAllTransitions = numOfAllTransitions
        # Identifying the transition symbols
        self.allTransitions = allTransitions
        self.graph = Digraph()

        # The following dictionary is used to store the indexes of the states
        self.statesDict = dict()
        for i in range(self.numOfStates):
            self.statesDict[self.qStates[i]] = i
        # The following dictionary is used to store the indexes of the alphabets
        self.alphabetsDict = dict()
        for i in range(self.numOfAlphabet):
            self.alphabetsDict[self.alphabets[i]] = i

        # The following dictionary is used for creating the transition table in the follownig format:
        # [From State + Alphabet pair] -> [Set of To States]
        self.transitionsTable = dict()
        # This for loop gets the first part of the format: [From State + Alphabet pair]
        for i in range(self.numOfStates):
            for j in range(self.numOfAlphabet):
                self.transitionsTable[str(i) + str(j)] = []
        # This for loop gets the first part of the format: [Set of To States]
        for i in range(self.numOfAllTransitions):
            self.transitionsTable[str(self.statesDict[self.allTransitions[i][0]])
                                  + str(self.alphabetsDict[
                                            self.allTransitions[i][1]])].append(
                self.statesDict[self.allTransitions[i][2]])

    # Function that prints the NFA quintuple to the user in the following form:
    # Q: states
    # Σ: alphabets
    # q0: Start state
    # F: Final State
    # δ: transition table
    def __repr__(self):
        return "Q : " + str(self.qStates) + "\nΣ : "
        + str(self.alphabets) + "\nq0 : "
        + str(self.startState) + "\nF : " + str(self.finalStates) + \
        "\nδ : \n" + str(self.transitionsTable)

    # Function to perform epsilon closure of a state in the NFA that has epsilon as a transition symbol.
    def getEpsilonClosure(self, state):
        # This dictionary will be used to store all the visited states to avoid repitions.
        closure = dict()
        closure[self.statesDict[state]] = 0
        # This stack is used to get the next state to be visited
        closureStack = [self.statesDict[state]]

        # Check the capacity of the stack, if not empty execute the code inside.
        while len(closureStack) > 0:
            # Store the top of the stack in a variable to be examined.
            # The top of the stack represents the current visited state.
            cur = closureStack.pop(0)
            # Loop on the states that have epsilon as an input symbol
            for x in self.transitionsTable[str(cur) + str(self.alphabetsDict['e'])]:
                # Check if this state is not already visited before
                if x not in closure.keys():
                    # add the state to the dictionary
                    closure[x] = 0
                    # push the current state to the stack
                    closureStack.append(x)
            closure[cur] = 1
        return closure.keys()

    # A Function to return the name from set of states to display in the DFA diagram
    def getStateName(self, state_list):
        name = ''
        for x in state_list:
            name += self.qStates[x]
        return name

    # Function that identifies the final states in the DFA Diagram according to the number
    # of final states in NFA.
    def isFinalDFA(self, state_list):
        for x in state_list:
            for y in self.finalStates:
                if x == self.statesDict[y]:
                    return True
        return False


def convert():
    print("Start Conversion")
    global statesString, startStateString, deltaString, alphabetString, finalStatesString

    # mapping the strings to the content of the input from the GUI
    statesString = setOfStatesInput.get()
    startStateString = startStateInput.get()
    alphabetString = alphabetInput.get()
    finalStatesString = finalStatesInput.get()
    deltaString = deltaInput.get()

    # transform strings into arrays
    allStates = statesString.split(',')
    qNode = startStateString
    inputSymbols = alphabetString.split(',')
    qFinal = finalStatesString.split(',')
    transitionTable = [list(line.split(',')) for line in deltaString.split('|')]

    nfa = NFA(
        len(allStates),  # number of states
        allStates,  # array of states
        len(inputSymbols),  # number of alphabets
        inputSymbols,  # array of alphabets
        qNode,  # start state
        len(qFinal),  # number of final states
        qFinal,  # array of final states
        len(transitionTable),  # number of transitions
        transitionTable,
        # array of transitions with its element of type :
        # [from state, alphabet, to state]
    )
    # Making an object of Digraph to visualize NFA diagram
    nfa.graph = Digraph()

    # Creating the States in the NFA Diagram
    for x in nfa.qStates:
        # This if condition is used for displaying the circles in the diagram:
        # if the state is not a final state --> display it with a single circle.
        if x not in nfa.finalStates:
            nfa.graph.attr('node', shape='circle')
            nfa.graph.node(x)
        # if the state is a final state --> display it with double circles.
        else:
            nfa.graph.attr('node', shape='doublecircle')
            nfa.graph.node(x)

    # Creating the pointing arrow to the start state in NFA Diagram
    nfa.graph.attr('node', shape='none')
    nfa.graph.node('')
    nfa.graph.edge('', nfa.startState)

    # Create the edges between the states from the transitions array.
    for x in nfa.allTransitions:
        nfa.graph.edge(x[0], x[2], label=('ε', x[1])[x[1] != 'e'])

    # Generates a pdf that visualizes the NFA Diagram
    nfa.graph.render('nfa', view=False, format="png")

    # Making an object of Digraph to visualize DFA diagram
    dfa = Digraph()

    # Calling the function that performs the epsilon closure.
    epsilon_closure = dict()
    for x in nfa.qStates:
        epsilon_closure[x] = list(nfa.getEpsilonClosure(x))

    # The epsilon closure of the start state of the NFA will be the first state in the DFA.
    dfaSavedStack = list()
    # The previous list is created to store the states until the current is finished converting from NFA to DFA.
    dfaSavedStack.append(epsilon_closure[nfa.startState])

    # Condition that checks if the start state is also a final state.
    if nfa.isFinalDFA(dfaSavedStack[0]):
        dfa.attr('node', shape='doublecircle')
    else:
        dfa.attr('node', shape='circle')
    dfa.node(nfa.getStateName(dfaSavedStack[0]))

    # Identify the DFA start state by drawing an arrow
    dfa.attr('node', shape='none')
    dfa.node('')
    dfa.edge('', nfa.getStateName(dfaSavedStack[0]))

    # Create a list to keep track of DFA states
    dfaStates = list()
    dfaStates.append(epsilon_closure[nfa.startState])

    # The conversion will keep running until the array that stores the DFA states is empty
    while len(dfaSavedStack) > 0:
        # Popping the stack state after the other and storing it into a variable to
        # start making the conversion for that state.
        currentState = dfaSavedStack.pop(0)

        # Loop over all the alphabets for the states stored in the currentState variable
        # to get the corresponding transitions of those states in the DFA
        for al in range(nfa.numOfAlphabet - 1):
            # A set to check if the epsilon closure of the current state is empty or not
            closureOutput = set()
            for x in currentState:
                # Perform union operation between the states found in the epsilon closure of the current state.
                closureOutput.update(
                    set(nfa.transitionsTable[str(x) + str(al)]))

            # Condition to ensure that the epsilon closure of the new set is not empty.
            if len(closureOutput) > 0:
                # Create a set to store the states the current state will be transitioned to.
                toState = set()
                for x in list(closureOutput):
                    toState.update(set(epsilon_closure[nfa.qStates[x]]))

                # Check if the to state already exists in DFA and if not then add it
                if list(toState) not in dfaStates:
                    dfaSavedStack.append(list(toState))
                    dfaStates.append(list(toState))

                    # This consition checks if this state is a final state or not
                    # in order to identify if it should be surrounded by double circles or
                    # a single circle.
                    if nfa.isFinalDFA(list(toState)):
                        dfa.attr('node', shape='doublecircle')
                    else:
                        dfa.attr('node', shape='circle')
                    dfa.node(nfa.getStateName(list(toState)))

                # Draw an edge from the current state to the corresponding to state.
                dfa.edge(nfa.getStateName(currentState),
                         nfa.getStateName(list(toState)),
                         label=nfa.alphabets[al])

            # Else, the current state has an empty epsilon closure, then it
            # will be represented as a phi (ϕ) state.
            else:

                # Condition to make sure there weren't any dead states present
                # before this one.
                # 1- if there wasn't any phi state beofre then we create a new one
                if (-1) not in dfaStates:
                    dfa.attr('node', shape='circle')
                    dfa.node('ϕ')

                    # The phi state will have all transitions looping on itself.
                    for alpha in range(nfa.numOfAlphabet - 1):
                        dfa.edge('ϕ', 'ϕ', nfa.alphabets[alpha])

                    # Adding -1 to list to mark that dead state is present
                    dfaStates.append(-1)

                # 2- Else, we add this current state to the phi state.
                dfa.edge(nfa.getStateName(currentState, ),
                         'ϕ', label=nfa.alphabets[al])

    # Generates a pdf and opens the DFA diagram.
    dfa.render('dfa', view=False, format="png")
    # make new figure with 2 sub-figures
    # each sub-figure can have an image in it
    fig = plt.figure()
    image1 = plt.subplot(121)
    image2 = plt.subplot(122)

    # read the image files (png files preferred)
    img_source1 = mpimg.imread('nfa.png')
    img_source2 = mpimg.imread('dfa.png')
    # put the images into the window
    _ = image1.imshow(img_source1)
    _ = image2.imshow(img_source2)

    # hide axis and show window with images
    image1.axis("off")
    image2.axis("off")
    plt.show()


# GUI
root = Tk()
root.geometry(str(400) + "x" + str(300))
root.title("NFA to DFA - ASU Final Automata Course Project")

Label(root, text="Enter NFA to convert", font=("Montserrat", 18), fg='#000000').grid(column=1, row=1, padx=2,
                                                                                     sticky="w")

Label(root, text="States", font=("Montserrat", 12), fg='#f66666').grid(column=1, row=2, padx=2, sticky="w")
setOfStatesInput = Entry(root, width=15, justify="left", bg='#f0f0f0')
setOfStatesInput.grid(column=2, row=2, padx=2, sticky="w")

Label(root, text="Start State", font=("Montserrat", 12), fg='#f66666').grid(column=1, row=4, padx=2, sticky="w")
startStateInput = Entry(root, width=5, justify="left", bg='#f0f0f0')
startStateInput.grid(column=2, row=4, padx=2, sticky="w")

Label(root, text="Final State", font=("Montserrat", 12), fg='#f66666').grid(column=1, row=6, padx=2, sticky="w")
finalStatesInput = Entry(root, width=5, justify="left", bg='#f0f0f0')
finalStatesInput.grid(column=2, row=6, padx=2, sticky="w")

Label(root, text="Alphabet", font=("Montserrat", 12), fg='#f66666').grid(column=1, row=8, padx=2, sticky="w")
alphabetInput = Entry(root, width=5, justify="left", bg='#f0f0f0')
alphabetInput.grid(column=2, row=8, padx=2, sticky="w")

Label(root, text="Delta", font=("Montserrat", 12), fg='#f66666').grid(column=1, row=10, padx=2, sticky="w")
deltaInput = Entry(root, width=15, justify="left", bg='#f0f0f0')
deltaInput.grid(column=2, row=10, padx=2, sticky="w")

convertBtn = Button(root, text="Convert", width=30, height=2, font=("Montserrat", 10),
                    command=lambda: convert())
convertBtn.grid(column=1, row=12, columnspan=3, sticky="w", padx=10, pady=10)

root.mainloop()
