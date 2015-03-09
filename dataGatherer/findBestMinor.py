import pickle
import csv
import sys

class minor(object):
	def __init__(self, url, name, total_credits, credits_left, all_classes, classes_remaining):
		super(minor, self).__init__()
		self.url = url
		self.name = name
		self.total_credits = total_credits
		self.credits_left = credits_left
		self.all_classes = all_classes
		self.classes_remaining = classes_remaining
		
		

def removeClassesTaken(all_classes):
	classes_taken = ["140507","140506","140516","140517","140514","140526","140529","140530",
					 "142373","142374","142375","142382","140667","143000","143096","141200",
					 "141706","141703","144085","139899","139903","142885","142923","141033",
					 "143939","139749"]
	classes_remaining = [course for course in all_classes if course not in classes_taken]
	return classes_remaining
	

def readInMinors(csvFile):
	minorList = []
	minorList.append(minor("tmp","tmp",0,0,["tmp"],["tmp"]))

	csv_data = csv.reader(file(csvFile))
	csv_data.next()   # skip the first line
	for csvRow in csv_data:
		url = csvRow[0]
		total_credits = int(csvRow[1])
		name = csvRow[2]
		all_classes = pickle.loads(csvRow[3])
		classes_remaining = removeClassesTaken(all_classes)
		credits_left = total_credits - ((len(all_classes) - len(classes_remaining))*3)
		if credits_left != total_credits:
			if minorList[-1].name != name:
				minorList.append(minor(url, name, total_credits, credits_left, all_classes, classes_remaining))
	return minorList			


def main():
    minorList = readInMinors(sys.argv[1])
    minorList.sort(key=lambda x: x.credits_left)

    print "Minors we care about: " + str(len(minorList))
    for minor in minorList:
    	print minor.name + " : " + str(minor.credits_left)

	

if __name__ == "__main__":
    main()
