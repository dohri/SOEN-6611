import datetime
import fileinput
import understand
import os

srcFile = ""

def CalculateCBO():
    
    # I have made modifications to this method. Our previous calculations were not correct
    
    classesCBO = {}

    for sourceFile in db.ents("file"):
        fileName, fileExtension = os.path.splitext(sourceFile.longname())
        if (fileExtension in ('.c', '.C', '.cc', '.cpp')):
            # Get a list of all class references defined in the source file
            fileReferences = sourceFile.refs("Define")
            for classReference in fileReferences:
                if (classReference.ent().kindname() in ("Class, Public Class, Private Class, Unknown Class")):
                    classDependencies = classReference.ent().depends()
                    classDependensby = classReference.ent().dependsby()

                    # Log statistics
                    srcFile.write(sourceFile.longname() + "\n")
                    srcFile.write('Depends = %d, Dependsby = %d, CBO = %d\n' % (len(classDependencies), len(classDependensby), (len(classDependencies) + len(classDependensby))))
                    srcFile.write("\n")

                    classesCBO[sourceFile.longname()] = len(classDependencies) + len(classDependensby)
    return classesCBO

def CalculateLCOM():
    
    # This method is still incomplete. Run the code and check the 'LCOM.txt' for clarifications
    
    classesLCOM = {}
    LCOM = 0
    functionKinds = "Function","Method","Public Function","Private Function","Protected Function","Public Virtual Function","Private Virtual Function","Protected Virtual Function","Public Const Function","Explicit Public Function","Public Virtual Const Function","Instance Method"
    attributesKinds = "Parameter","Private Object","Public Object","Protected Object","Global Object","Enumerator","Public Enumerator"
    for sourceFile in db.ents("file"):
        fileName, fileExtension = os.path.splitext(sourceFile.longname())
        if (fileExtension in ('.c', '.C', '.cc', '.cpp')):
            # Get a list of all class references defined in the source file
            fileReferences = sourceFile.refs("Define")
            for classReference in fileReferences:
                if (classReference.ent().kindname() in ("Class, Public Class, Private Class, Unknown Class")):
                    classDefinedReferences = classReference.ent().refs("Define")
                    srcFile.write("# of references in class \'%s\' = %d\n" % (classReference.ent().longname(), len(classDefinedReferences)))

                    graph = set()
                    totalNumberOfMethods = len(classDefinedReferences)
                    if (totalNumberOfMethods == 0):
                        return LCOM
                    else:
                        for reference in classDefinedReferences:
                            try:
                                usedEntities = reference.ent().refs("Use")
                                srcFile.write("# of entities used by \'%s\' = %d\n" % (reference.ent().name(), len(usedEntities)))

                                entityKind = reference.ent().kindname()
                                entityName = reference.ent().name()

                                for usedEntity in usedEntities:
                                    usedEntityKind = reference.ent().kindname()
                                    usedEntityName = reference.ent().name()
                                    srcFile.write("%s %s uses %s %s\n" % (
                                        reference.ent().kindname(), reference.ent().name(), usedEntity.ent().kindname(),
                                        usedEntity.ent().name()))

                                    if (entityKind in (functionKinds)):
                                        # Function/Method uses another Function/Method
                                        if (usedEntityKind in ("%s" % (functionKinds))):
                                            graph.add(frozenset(["%s %s" % (entityKind,entityName), "%s %s" % (usedEntityKind,usedEntityName)]))

                                        # 2 Functions/Methods use the same attribute
                                        if (usedEntityKind in ("%s" % (attributesKinds))):
                                            print ("Verify use of attributes")
                                srcFile.write("\n")
                            except:
                                continue
                        srcFile.write("\n")

                    totalNumberOfActualLinks = len(graph)
                    minimumNumberOfLinks = totalNumberOfMethods-1
                    LCOM = getLCOM(minimumNumberOfLinks,totalNumberOfActualLinks,minimumNumberOfLinks)
                classesLCOM[sourceFile.longname()] = LCOM
    return classesLCOM

def getLCOM(minimumNumOfLinks, totalNumOfActualLinks, minimumNumOfActualLinks):
    LCOM = 0
    if (totalNumOfActualLinks >= minimumNumOfLinks):
        LCOM = 1
        return LCOM
    elif(totalNumOfActualLinks == minimumNumOfLinks - totalNumOfActualLinks + 1):
        LCOM = minimumNumOfActualLinks - totalNumOfActualLinks + 1
        return LCOM
    else:
        minimumNumberOfLinks = minimumNumOfLinks - 1
        getLCOM(minimumNumberOfLinks,totalNumOfActualLinks)

def writeMetricsInfoToCsv(releaseNumber,cboDictionary,lcomDictionary):
    temp = ''
    for key in cboDictionary:
        temp = temp + releaseNumber + key + ',' + cboDictionary[key] + ',' + lcomDictionary[key] + '\n'
        temp1 = open('metrics.txt','wb')
        temp1.write(temp)

if __name__ == '__main__':
    # Database path is defined in config file
    ConfigAttributes = fileinput.input()
    DB_ROOT_DIRECTORY = ConfigAttributes[0].split(' = ')[1]
    releaseNumber = ConfigAttributes[1].split(' = ')[1].split('.')[0]

    # Open Database
    print("Opening database..\n")
    print (DB_ROOT_DIRECTORY)
    db = understand.open(DB_ROOT_DIRECTORY)

    print("Calculating the CBO metric..")
    startCalcTime = datetime.datetime.now()
    srcFile = open("CBO.txt", 'w')
    classesCBO = CalculateCBO()
    srcFile.close()
    endCalcTime = datetime.datetime.now()
    print("Total time elapsed for CBO calculation = ", endCalcTime - startCalcTime)

    print("Calculating the LCOM metric..")
    startCalcTime = datetime.datetime.now()
    srcFile = open("LCOM.txt", 'w')
    classesLCOM = CalculateLCOM()
    srcFile.close()
    endCalcTime = datetime.datetime.now()
    print("Total time elapsed for LCOM calculation = ", endCalcTime - startCalcTime)

    print("Writing metrics to file..")
    writeMetricsInfoToCsv(releaseNumber, classesCBO, classesLCOM)

    print("\nCalculations are done. Refer to generated files for metrics details.")
