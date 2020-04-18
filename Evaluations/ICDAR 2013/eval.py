# Please Note 
# 1) This file and tool.jar must be kept in the same directory as the PDF 
# 2) Format of pdf, groundtruth and result are same as the ICDAR 13, ex : eu-001.pdf,eu-001-reg.xml,eu-001-reg-result.xml
# 3) PDF,Groundtruth and result must be in same directory as the this program

# import subprocess library
import subprocess
import glob as glob

# Global 
GcompleteDetected = 0
GcompleteTotal = 0
GpurityDetected = 0
GpurityTotal = 0

# Get all the Images 
path = glob.glob("*.pdf")

# Run eval for each PDF
for file in path:
	name = file[:-4]
	print("\nProcessing : ",name)

	# Running Java tool through Command line 
	out = subprocess.Popen(['java', '-jar', 'tool.jar','-reg',name], 
	           stdout=subprocess.PIPE, 
	           stderr=subprocess.STDOUT)
	
	# Taking output
	stdout,stderr = out.communicate()
	
	# Filtering
	lastPortion = str(stdout[-45:]).split("=")[:-1]
	lastPortion = str(lastPortion).split(" ")
	number = [] 
	for element in lastPortion:
		if element.isnumeric():
			number.append(element)
    
    # getting the variables required for evaluation
	completeDetected = int(number[0])
	completeTotal = int(number[1])
	purityDetected = int(number[-1])
	purityTotal = int(number[-1])

	# print("Completeness : ",completeDetected,"/",completeTotal,"=",completeDetected/completeTotal,"Purity :" ,purityDetected,"/",purityTotal,"=",purityDetected/purityTotal)
	if purityTotal != 0:
		print("Completeness : ",completeDetected,"/",completeTotal,"=",completeDetected/completeTotal,"Purity :" ,purityDetected,"/",purityTotal,"=",purityDetected/purityTotal)
	else :
		print("None Detected From ",completeTotal)
	
	GcompleteDetected += completeDetected
	GcompleteTotal += completeTotal
	GpurityDetected += purityDetected
	GpurityTotal += purityTotal

# Compute
Completeness = GcompleteDetected/GcompleteTotal
Purity =  GpurityDetected/GpurityTotal
Precision = GcompleteDetected/GpurityDetected
Recall = Completeness * Purity
F1 = (2 * Precision * Recall)/(Precision+Recall)

# Display the final score
print("\n\n\nFinal Result")
print("Complete Total : ",GcompleteDetected)
print("Complete Detected : ",GcompleteTotal)
print("Purity Detected : ",GpurityDetected)
print("Purity Total : ",GpurityTotal)
print("Completeness : ",Completeness,"Purity :" ,Purity)
print("Precision : ",Precision,"Recall :" ,Recall)
print("F1 :",F1)
