import random

def getInsertLength():
	return 1000		#This should be replaced with a distribution

#	Real read lengths vary once they have been trimmed. To simulate that variation
#	the ReadLength table contains a distribution of read lengths generated from 
#	real MiSeq reads of NTM. This function generates a pseudo random number and then
#	usues it to lookup the associated read length from the database
def getReadLength(cursor, nominalReadLength, direction):
	myRand = random.random()
	sql = 'SELECT ReadLength FROM ReadLength WHERE LowerBound <= ? AND ? < UpperBound AND NominalReadLength = ? AND Direction = ?'
	#could use some error handling here...
	cursor.execute(sql, (myRand, myRand, nominalReadLength, direction))
	return cursor.fetchone()[0]