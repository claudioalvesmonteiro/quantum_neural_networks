from encodingsource import InitializerUniformlyRotation
from sf import sfGenerator
from hsgs import hsgsGenerator
import numpy as np
import math
import random
from qiskit import execute, Aer, QuantumRegister, QuantumCircuit, ClassicalRegister
from sympy.combinatorics.graycode import GrayCode
from qiskit.circuit.library.standard_gates.multi_control_rotation_gates import _apply_mcu3_graycode, mcrx
from qiskit.aqua.utils.controlled_circuit import apply_cu3


def EncodingGenerator(inputVector, circuit, nSize):
	#inputVector is a Python list 
		#eg. inputVector=[1, -1, 1, 1]
	#circuit is a Quantum Circuit
	#nSize is the input size
	QuantumCircuit.ur_initialize = InitializerUniformlyRotation.initialize
	circuit.ur_initialize(inputVector, nSize)

	return circuit

def createNeuron (inputVector, weightVector, circuitGeneratorOfUOperator):
	#inputVector is a Python list 
		#eg. inputVector=[1, -1, 1, 1]
	#weightVector is a Python list 
		#eg. weightVector=[1, 1, 1, -1]
	#circuitGeneratorOfUOperator is a function in python that will generate the Ui and Uw operators.
		#circuitGeneratorOfUOperator can be "hsgs", "sf", "encoding"

	##this function returns the quantum circuit of the neuron

	n = int(math.log(len(input_vector), 2))

	circuit = QuantumCircuit()
	q_input = QuantumRegister(n, 'q_input')
	q_target = QuantumRegister(1, 'q_target')
	q_output = QuantumRegister(1, 'q_output')
	c_output = ClassicalRegister(1, 'c_output')
	circuit.add_register(q_input)
	circuit.add_register(q_target)
	circuit.add_register(q_output)
	circuit.add_register(c_output)


	for i in range(n):
		circuit.h(q_input[i])

	if circuitGeneratorOfUOperator == "hsgs":
		hsgsGenerator(inputVector, circuit, q_input,  n)
	elif circuitGeneratorOfUOperator == "sf":
    	sfGenerator(inputVector, circuit, q_input, q_target, n)
	elif circuitGeneratorOfUOperator == "encoding":
    	EncondingGenerator(inputVector, circuit, n)

	for i in range(n):
		circuit.h(q_input[i])
		circuit.x(q_input[i])

	mcrx(circuit, math.pi, q_input, q_output[0])

	#comentario de fernando: falta a sequencia de CNOTS
	circuit.measure(q_output, c_output)
	return circuit


def executeNeuron(neuronQuantumCircuit, simulator, threshold):
	#neuronQuantumCircuit is the return of the function createNeuron
	#simulator function of a qiskit quantum simulator
	#expectedOutput is a Python List with expected value
		#e.g expectedOutput = [1] or expectedOutput = [0]
	#threshold is a real value between 0 or 1


	##this function returns the output 0 or 1 of the neuron depending of threshold value

    neuronOutput = int # FARIA MAI SENTIDO ISSO SER TRUE OU FALSE
    circuit = neuronQuantumCircuit
    job = execute(circuit, backend=backend_simulador, shots=8192)
    result = job.result()
    count = result.get_counts()

    results1 = count.get('1') # Resultados que deram 1
    if str(type(results1)) == "<class 'NoneType'>": results1 = 0

    results0 = contagem.get('0') # Resultados que deram 0
    if str(type(results0)) == "<class 'NoneType'>": results0 = 0

        # Utilizando threshold
        if results1 >= (nshots * threshold):
            neuronOutput = 1 # FARIA MAIS SENTIDO ISSO SER TRUE
        else:
            neuronOutput = 0 # FARIA MAIS SENTIDO ISSO SER FALSE

    return neuronOutput


	def runDataset(listOfInput, listOfExpectedOutput, weightVector, circuitGeneratorOfUOperator, simulator, threshold, memoryOfExecutions):
	#listOfInput is a Python List 
		#e.g listOfInput= [[1,-1,1,1], [-1,-1,-1,1]]
	#listOfExpectedOutput is a Python List 
		#e.g listOfExpectedOutput= [[0], [1]]
	#weightVector is a Python list 
		#eg. weightVector=[1, 1, 1, -1]
	#circuitGeneratorOfUOperator is a function in python that will generate the Ui and Uw operators.
		#circuitGeneratorOfUOperator can be "hsgsGenerator", "SFGenerator", "EncodingGenerator"
	#simulator function of a qiskit quantum simulator
	#threshold is a real value between 0 or 1
	#memoryOfExecutions is a Python Dictionary with the executions and its results
		#the index is (inputVector, weightVector) and the content of the dic is the output of the neuron
		#e.g memoryOfExecutions = {([1,1,-1,1], [1,1,-1,1]: 0)}

	#for each input in listOfInput
		#generate the neuron circuit only if the configuration (input, weight) is not in Dic memoryOfExecutions
		#execute and save in the memoryOfExecutions


	##this function returns confusion matrix for this listOfInput and weightVector.

        #Variables initialization
        circuit = QuantumCircuit()
        truePositives = 0
        trueNegatives = 0
        falsePositives = 0
        falseNegatives = 0
        datasetSize = len(listOfInput)

        #Starting the run in the entire dataset
        for i in range(datasetSize):

            inputVector = listOfInput[i]
            theClass = listOfExpectedOutput[i]

            # ANTES DE EXECUTAR VERIFICAR NO DICIONARIO memoryOfExecutions

            circuit = createNeuron(inputVector, weightVector, circuitGeneratorOfUOperator)     
            executionResult = executeNeuron(circuit, simulator, threshold)

            # Comparing the actual result with the expected result 
            if executionResult == 0: # neuronio deu como saida 0
                if theClass != 0: 
                    falseNegatives = falseNegatives + 1
                else:
                    trueNegatives = trueNegatives + 1
            else: # neuronio deu como saida 1
                if theClass != 1: 
                    falsePositives = falsePositives + 1
                else:
                    truePositives = truePositives + 1

        return [[trueNegatives, falsePositives],[falseNegatives, truePositives]], memoryOfExecutions
    




