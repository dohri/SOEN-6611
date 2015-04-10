import datetime
import fileinput
import understand
import os

srcFile = ""
functionsLinksDictioanry = {}

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
                    srcFile.write('Depends = %d, Dependsby = %d, CBO = %d\n' % (
                        len(classDependencies), len(classDependensby), (len(classDependencies) + len(classDependensby))))
                    srcFile.write("\n")

                    classesCBO[sourceFile.longname()] = len(classDependencies) + len(classDependensby)
    return classesCBO


def CalculateLCOM():
    # This method is still incomplete. Run the code and check the 'LCOM.txt' for clarifications

    classCBO = {}

    functionKinds = "Function", "Method", "Public Function", "Private Function", "Protected Function", "Public Virtual Function", "Private Virtual Function", "Protected Virtual Function", "Public Const Function", "Explicit Public Function", "Public Virtual Const Function", "Instance Method"
    attributesKinds = "Parameter", "Private Object", "Public Object", "Protected Object", "Global Object", "Enumerator", "Public Enumerator"
    for sourceFile in db.ents("file"):
        fileName, fileExtension = os.path.splitext(sourceFile.longname())
        if (fileExtension in ('.c', '.C', '.cc', '.cpp')):
            # Get a list of all class references defined in the source file
            fileReferences = sourceFile.refs("Define")
            for classReference in fileReferences:
                if (classReference.ent().kindname() in ("Class, Public Class, Private Class, Unknown Class")):
                    classDefinedReferences = classReference.ent().refs("Define")
                    srcFile.write("# of references in class \'%s\' = %d\n" % (
                        classReference.ent().longname(), len(classDefinedReferences)))

                    graph = set()

                    totalNumberOfMethods = len(classDefinedReferences)
                    for reference in classDefinedReferences:
                        try:
                            usedEntities = reference.ent().refs("Use")
                            srcFile.write(
                                "# of entities used by \'%s\' = %d\n" % (reference.ent().name(), len(usedEntities)))

                            entityKind = reference.ent().kindname()
                            entityName = reference.ent().name()

                            for usedEntity in usedEntities:
                                usedEntityKind = reference.ent().kindname()
                                usedEntityName = reference.ent().name()
                                srcFile.write("%s %s uses %s %s\n" % (
                                    reference.ent().kindname(), reference.ent().name(), usedEntity.ent().kindname(),
                                    usedEntity.ent().name()))
                                functionsLinksDictioanry[reference.ent().name()].append[usedEntity.ent.name()]

                                srcFile.write("\n")
                        except:
                            continue
                srcFile.write("\n")
        counter = 0
        dictLength = len(functionsLinksDictioanry)
        ls = []
        temp = []
        for i in functionsLinksDictioanry:
            ls.append(i)
            listLen = len(ls)

            for i in range(0, listLen):
                val = str(ls[i])
                if i < dictLength - 1:
                    if [y for y in functionsLinksDictioanry[ls[0]] if y in functionsLinksDictioanry[ls[i + 1]]]:
                        print (ls[0])
                        print (ls[i + 1])
                        counter = counter + 1
                        print (temp)
            print ("LCOM:-", len(functionsLinksDictioanry) - counter)

if __name__ == '__main__':
    # Database path is defined in config file
    ConfigAttributes = fileinput.input()
    DB_ROOT_DIRECTORY = ConfigAttributes[0].split(' = ')[1]

    # Open Database
    print("Opening database..\n")
    db = understand.open(DB_ROOT_DIRECTORY)

    # print("Calculating the CBO metric..")
    startCalcTime = datetime.datetime.now()
    srcFile = open("CBO.txt", 'w')
    classesCBO = CalculateCBO()
    srcFile.close()
    endCalcTime = datetime.datetime.now()
    print("Total time elapsed for CBO calculation = ", endCalcTime - startCalcTime)

    print("Calculating the LCOM metric..")
    startCalcTime = datetime.datetime.now()
    srcFile = open("LCOM.txt", 'w')
    CalculateLCOM()

    srcFile.close()
    endCalcTime = datetime.datetime.now()
    print("Total time elapsed for LCOM calculation = ", endCalcTime - startCalcTime)

    print("\nCalculations are done. Refer to generated files for metrics details.")
    print (diction)