# -* - coding:UTF-8 -*- 
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
from abaqus import *
import time
import sys
import os

import xml.dom.minidom
import __main__

import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior 


    


def Polygon3DFunction(XmlFile,MatrixSizeX,MatrixSizeY,MatrixSizeZ,ParticleSize,VolF,TransitonRatio,TransitonSize,MatrixMeshSize,ParticleMeshSize,TransitionMeshSize,CompositeMaterial,MatrixMaterial,ParticleMaterial,MaterialTable,StepType,Response,TimePeriod,IncType,MaxIncNum,InitialInc,MinInc,MaxInc,tempMaxCheckbox,tempMaxValue,odbFileName,DegreeFreedom,GlobalStep,SubRelative,subScale,ModelName,jobName,ProcessorNumber):
    print('start ...')
    CreateModel(ModelName)
    MesoModelCreate(XmlFile,ModelName)
    MeshParts(XmlFile,ModelName,MatrixMeshSize,ParticleMeshSize,TransitionMeshSize)
    SetMaterial(XmlFile,ModelName,CompositeMaterial,MatrixMaterial,ParticleMaterial)
    #DefineStaticStep(ModelName,TimePeriod,IncType,MaxIncNum,InitialInc,MinInc,MaxInc)
    DefineContact(XmlFile,ModelName)
    #DefineCohesiveContact(XmlFile,ModelName)
    #DefineLoadAndBC(XmlFile,ModelName,odbFileName,DegreeFreedom,GlobalStep,SubRelative,subScale)#未编写内容
    #DefineJob(ModelName,jobName,ProcessorNumber)
    
    
    
def CreateModel(ModelName):
    #创建新的模型Model
    mdb.Model(name=ModelName, modelType=STANDARD_EXPLICIT)
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    
#创建细观模型
def MesoModelCreate(XmlFile,ModelName):
    # doc = PolyReadXml(XmlFile)#开始读取xml
    
    ##获取颗粒的数目
    # PolyNumber = doc.GetPolyhedralNumber()
    # tempPrint = 'The total number of particles is '+str(PolyNumber)
    # print(tempPrint)
    
    doc = PolyReadXml(XmlFile)#开始读取xml
    #获取颗粒的数目
    PolyNumber = doc.GetPolyhedralNumber()
    tempPrint = 'The total number of particles is '+str(PolyNumber)
    print(tempPrint)
    
    
    PolyLineList = doc.GetPolyLineTuple()
    
    EdgeList = doc.GetPolyFaceLineCenterTuple()

    #循环创建颗粒
    for number in range(1,PolyNumber+1):
        tempName = 'Particle' + str(number)#颗粒的名称
        p = mdb.models[ModelName].Part(name=tempName, dimensionality=THREE_D,type=DEFORMABLE_BODY)
        p = mdb.models[ModelName].parts[tempName]
        session.viewports['Viewport: 1'].setValues(displayedObject=p)#置为当前
    
        tempPrint = 'Particle number = ' + str(number)
        print(tempPrint)
        
        #创建多面体的边
        #pointsList1 = doc.GetLineTuple(number)        
        pointsList1 = PolyLineList[number-1]
        try:
            p.WirePolyLine(points=pointsList1, mergeType=SEPARATE, meshable=ON)
        except:
            tempPrint = 'WirePolyLine: Particle: '+ str(number)
            print(tempPrint)
            continue
                     
                
        tempName = 'Particle' + str(number)
        p = mdb.models[ModelName].parts[tempName]
        e = p.edges
        
        #tempEdge = doc.GetFaceLineCenterTuple(number)
        tempEdge = EdgeList[number-1]
                    
        #依次生成面
        for i in range(0,len(tempEdge)):
            edgeCenterList = []
            for j in range(0,len(tempEdge[i])):
                try:
                    edgeCenterList.append(e.findAt(coordinates=tempEdge[i][j]))#利用中点选择边
                except:
                    tempPrint = 'Edge failed: Particle: '+ str(number)+' Face: ' + str(i+1)+' Edge: '+ str(j+1)
                    print(tempPrint)
                    
            edgeCenterListTuple = tuple(edgeCenterList)#
            
            try:
                p.CoverEdges(edgeList = edgeCenterListTuple, tryAnalytical=True)#边生成面
            except:
                tempPrint = 'Face failed: Particle: '+ str(number)+' Face: ' + str(i+1)
                print(tempPrint)
        try:
            f = p.faces
            p.AddCells(faceList = f[0:len(f)])
            p = mdb.models[ModelName].parts[tempName]#面生成体
            print('success')
        except:
            tempPrint = 'Particle failed: Partice: ' +str(number)
            print(tempPrint)
    # return 
    
    #生成基体
    # MatrixInfo = doc.GetMatrixInfo()
    # s = mdb.models[ModelName].ConstrainedSketch(name='__profile__', 
        # sheetSize=MatrixInfo[1])
    # g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    # s.setPrimaryObject(option=STANDALONE)
    # s.rectangle(point1=(0.0, 0.0), point2=MatrixInfo[0])
    # p = mdb.models[ModelName].Part(name='MatrixAl', dimensionality=THREE_D, 
        # type=DEFORMABLE_BODY)
    # p = mdb.models[ModelName].parts['MatrixAl']
    # p.BaseSolidExtrude(sketch=s, depth=MatrixInfo[1])
    # s.unsetPrimaryObject()
    # p = mdb.models[ModelName].parts['MatrixAl']
    # session.viewports['Viewport: 1'].setValues(displayedObject=p)
    # del mdb.models[ModelName].sketches['__profile__']
    # print("Matrix create successfully")
    # return
    
    #生成基体2
    tempName = 'MatrixAl'#基体的名称
    p = mdb.models[ModelName].Part(name=tempName, dimensionality=THREE_D,type=DEFORMABLE_BODY)
    p = mdb.models[ModelName].parts[tempName]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)#置为当前

    tempPrint = 'Create Matrix ...' 
    print(tempPrint)
    
    #创建多面体的边
    pointsList1 = doc.GetMatrixLineTuple()
    try:
        p.WirePolyLine(points=pointsList1, mergeType=SEPARATE, meshable=ON)
    except:
        tempPrint = 'WirePolyLine: Particle: '+ str(number)
        print(tempPrint)
                 
    p = mdb.models[ModelName].parts[tempName]
    e = p.edges
    
    #tempEdge = doc.GetFaceLineCenterTuple(number)
    tempEdge = doc.GetMatrixFaceLineCenterTuple()
                
    #依次生成面
    for i in range(0,len(tempEdge)):
        edgeCenterList = []
        for j in range(0,len(tempEdge[i])):
            try:
                edgeCenterList.append(e.findAt(coordinates=tempEdge[i][j]))#利用中点选择边
            except:
                tempPrint = 'Edge failed: Particle: '+ str(number)+' Face: ' + str(i+1)+' Edge: '+ str(j+1)
                print(tempPrint)
                
        edgeCenterListTuple = tuple(edgeCenterList)#
        
        try:
            p.CoverEdges(edgeList = edgeCenterListTuple, tryAnalytical=True)#边生成面
        except:
            tempPrint = 'Face failed: Particle: '+ str(number)+' Face: ' + str(i+1)
            print(tempPrint)
    try:
        f = p.faces
        p.AddCells(faceList = f[0:len(f)])
        p = mdb.models[ModelName].parts[tempName]#面生成体
        print('success')
    except:
        tempPrint = 'Particle failed: Partice: ' +str(number)
        print(tempPrint)
      
    
    #将颗粒加入到装配中
    a = mdb.models[ModelName].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a1 = mdb.models[ModelName].rootAssembly
    for number in range(1,PolyNumber+1):
        tempName = 'Particle' + str(number)
        p = mdb.models[ModelName].parts[tempName]        
        tempName = 'Particle' + str(number)+'-1'
        a1.Instance(name=tempName, part=p, dependent = ON)
    print("Particle first insert to Assembly successfully")
    
    #基体导入到装配中
    a = mdb.models[ModelName].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    a = mdb.models[ModelName].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[ModelName].parts['MatrixAl']
    a.Instance(name='MatrixAl-1', part=p, dependent = ON)
    print("Matrix first insert to Assembly successfully")


    # 将颗粒从基体中减去，做布尔运算
    # PolyNumber = doc.GetPolyhedralNumber()
    for number in range(1,PolyNumber+1):
    # 需要判断颗粒是否有实体，如果有，则操作，如果没有，则将基体重新命名。
        try:
            PolyhedralName = 'Particle' + str(number)+'-1'
            MatrixBoolName = 'MatrixBool' + str(number)           
            session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=OFF, 
                constraints=OFF, connectors=OFF, engineeringFeatures=OFF)
            a1 = mdb.models[ModelName].rootAssembly
            MatrixBoolNameOld = 'temp'
            if number == 1:
                MatrixBoolNameOld = 'MatrixAl-1'
            else:
                MatrixBoolNameOld =  'MatrixBool' + str(number-1) +'-1'
                
            a1.InstanceFromBooleanCut(name=MatrixBoolName, 
                instanceToBeCut=mdb.models[ModelName].rootAssembly.instances[MatrixBoolNameOld], 
                cuttingInstances=(a1.instances[PolyhedralName], ), 
                originalInstances=DELETE)
            a = mdb.models[ModelName].rootAssembly
        except:
            tempPrint = 'bool substract failed: Particle: '+ str(number)
            print(tempPrint)
    print("Boolean subtraction was successful")   
    
    # 删除装配中的基体
    MatrixName =  'MatrixBool' + str(PolyNumber) +'-1'
    a = mdb.models[ModelName].rootAssembly
    del a.features[MatrixName]
    print("Remove the last matrix part")   
    
    
    #删除多余的几何体
    del mdb.models[ModelName].parts['MatrixAl']
    for number in range(1,PolyNumber):
        try:
            MatrixName = 'MatrixBool' + str(number)
            del mdb.models[ModelName].parts[MatrixName]
            #tempPrint = 'delete redundant part-' + MatrixName
            #print(tempPrint)   
        except:
            tempPrint = 'delete redundant part failed: Particle: '+ str(number)
            print(tempPrint)
    print("Remove the superfluous body")       
    
    #重命名基体--
    MatrixName = 'MatrixBool' + str(PolyNumber)  
    mdb.models[ModelName].parts.changeKey(fromName = MatrixName, toName='MatrixAl')
    print('rename Matrix to MatrixAl')
    
    # 重新导入基体
    a = mdb.models[ModelName].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a = mdb.models[ModelName].rootAssembly
    p = mdb.models[ModelName].parts['MatrixAl']
    a.Instance(name='MatrixAl-1', part=p, dependent = ON)
    a = mdb.models[ModelName].rootAssembly
    print("Matrix insert to Assembly successfully")    
    
    # 重新导入颗粒
    # 将颗粒加入到装配中
    a = mdb.models[ModelName].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a1 = mdb.models[ModelName].rootAssembly
    for number in range(1,PolyNumber+1):
        try:
            tempName = 'Particle' + str(number)
            p = mdb.models[ModelName].parts[tempName]        
            tempName = 'Particle' + str(number)+'-1'
            a1.Instance(name=tempName, part=p, dependent = ON)
        except:
            tempPrint = 're-insert part failed: Particle: '+ str(number)
            print(tempPrint)
    
    print("Particle insert to Assembly successfully")  
    

#设置材料信息 并指定到part 
def SetMaterial(XmlFile,modelName,CompositeMaterial,MatrixMaterial,ParticleMaterial):   
 
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=OFF)
    
    #创建材料
    # mdb.models[modelName].Material(name='Al2009SiC')#材料名称Al
    # mdb.models[modelName].materials['Al2009SiC'].Density(table=((2.8E-9, ), ))#密度
    # mdb.models[modelName].materials['Al2009SiC'].Elastic(table=((103000.0, 0.3), ))#弹性模量和泊松比
    # mdb.models[modelName].materials['Al2009SiC'].Plastic(table=((300000000.0, 0.0), ))#屈服强度
    # print('create material Al2009SiC')
    
    #创建材料
    mdb.models[modelName].Material(name='Al2009')#材料名称Al
    mdb.models[modelName].materials['Al2009'].Density(table=((2.82E-9, ), ))#密度
    mdb.models[modelName].materials['Al2009'].Elastic(table=((72.4, 0.33), ))#弹性模量和泊松比
    mdb.models[modelName].materials['Al2009'].Plastic(table=((0.395, 0.0), ))#屈服强度   
    print('create material Al2009')
    
    mdb.models[modelName].Material(name='SiC')#材料名称SiC
    mdb.models[modelName].materials['SiC'].Density(table=((3.15E-9, ), ))#密度
    mdb.models[modelName].materials['SiC'].Elastic(table=((427, 0.17), ))#弹性模量和泊松比
    mdb.models[modelName].materials['SiC'].Plastic(table=((0.355, 0.0), ))#屈服强度
    print('create material SiC')
    

    
    
    
    # 创建section
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=OFF)
    mdb.models[modelName].HomogeneousSolidSection(name='MatrixSection', material=MatrixMaterial, thickness=None)
    mdb.models[modelName].HomogeneousSolidSection(name='ParticleSection', material=ParticleMaterial, thickness=None)
    # mdb.models[modelName].HomogeneousSolidSection(name='PRMMCsSection', material=CompositeMaterial, thickness=None)   
    print('create material section') 

    #指定part的材料       
    doc = PolyReadXml(XmlFile)
    PolyNumber = doc.GetPolyhedralNumber()#颗粒的数量获取
    for number in range(1,PolyNumber+1):
        tempName = 'Particle' + str(number)
        p = mdb.models[modelName].parts[tempName]
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        p = mdb.models[modelName].parts[tempName]
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        p = mdb.models[modelName].parts[tempName]
        c = p.cells
        cells = c[0:1]
        tempSetName = 'ParticleSet' + str(number)
        region = p.Set(cells=cells, name=tempSetName)
        p = mdb.models[modelName].parts[tempName]
        p.SectionAssignment(region=region, sectionName='ParticleSection', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)    
    print('set Particle material')
    
    #指定基体材料
    p = mdb.models[modelName].parts['MatrixAl']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models[modelName].parts['MatrixAl']
    c = p.cells
    cells = c[0:1]
    region = p.Set(cells=cells, name='MatrixAlSet')
    p = mdb.models[modelName].parts['MatrixAl']
    p.SectionAssignment(region=region, sectionName='MatrixSection', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
        
    print('set MatrixAl material')
    

#定义静态力学分析步
def DefineStaticStep(ModelName,TimePeriod,IncType,maxIncNum,InitialInc,MinInc,MaxInc):#缺少最大的步数
    if IncType == 'Automatic':
        a = mdb.models[ModelName].rootAssembly
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(adaptiveMeshConstraints=ON, optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
        mdb.models[ModelName].StaticStep(name='Step-1', previous='Initial', timePeriod=float(TimePeriod), maxNumInc=int(maxIncNum), initialInc=float(InitialInc), minInc=float(MinInc), maxInc=float(MaxInc))
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
        
    if IncType == 'Fixed':
        a = mdb.models[ModelName].rootAssembly
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(adaptiveMeshConstraints=ON, optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
        mdb.models[ModelName].StaticStep(name='Step-1', previous='Initial', timePeriod=float(TimePeriod), timeIncrementationMethod=FIXED, initialInc=float(InitialInc),noStop=OFF)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')

#定义结构力耦合分析步
def DefineStaticStep(ModelName,TimePeriod,IncType,maxIncNum,InitialInc,MinInc,MaxInc,tempMaxValue):#缺少最大的步数
    if IncType == 'Automatic':
        mdb.models[ModelName].CoupledTempDisplacementStep(name='Step-1', previous='Initial', timePeriod=float(TimePeriod), maxNumInc=int(maxIncNum), initialInc=float(InitialInc), minInc=float(MinInc), maxInc=float(MaxInc), deltmx=tempMaxValue)
    if IncType == 'Fixed':
        mdb.models['D2'].CoupledTempDisplacementStep(name='Step-1', previous='Initial', timeIncrementationMethod=FIXED, deltmx=None, cetol=None, creepIntegration=None)
        


    
#定义接触
def DefineContactOld(XmlFile,ModelName):
        #创建颗粒和基体的接触关系
    doc = PolyReadXml(XmlFile)    
    PolyNumber = doc.GetPolyhedralNumber()#颗粒的数量获取
    for number in range(1,PolyNumber+1):#颗粒循环
        tempName = 'Particle' + str(number) + '-1'#颗粒名称
        
        #获取面的中点
        CenterPoints = doc.GetFaceCenterTupleBy2Line(number)
        numberFace = len(CenterPoints)
        for numberFaceN in range(0,numberFace):
            a = mdb.models[ModelName].rootAssembly
            s1 = a.instances[tempName].faces
            
            side1Faces1 = s1.findAt((CenterPoints[numberFaceN], ))
            region1=regionToolset.Region(side1Faces=side1Faces1)
            
            a = mdb.models[ModelName].rootAssembly
            s1 = a.instances['MatrixAl-1'].faces
            side1Faces1 = s1.findAt((CenterPoints[numberFaceN], ))
            region2=regionToolset.Region(side1Faces=side1Faces1)
            
            tempName2 = 'Poly'+str(number)+'Face'+str(numberFaceN+1)
            mdb.models[ModelName].Tie(name=tempName2, master=region1, slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)
        temprint = 'Defined Contact Particle' + str(number) + '-1  with Matrix'#颗粒名称
        print(temprint)
        
#定义接触
def DefineContact(XmlFile,ModelName):
        #创建颗粒和基体的接触关系
    doc = PolyReadXml(XmlFile)    
    PolyNumber = doc.GetPolyhedralNumber()#颗粒的数量获取
    
    a = mdb.models[ModelName].rootAssembly
    MatrixFaceList = a.instances['MatrixAl-1'].faces
    
    for number in range(1,PolyNumber+1):#颗粒循环
        tempName = 'Particle' + str(number) + '-1'#颗粒名称
        PolyFaceList = a.instances[tempName].faces
        numberFaceN = 0
        
        for PolyFace in PolyFaceList:
            PointOnFace = PolyFace.pointOn
            
            side1Faces1 = PolyFaceList.findAt(PointOnFace)
            region1=regionToolset.Region(side1Faces=side1Faces1)
            
            side1Faces2 = MatrixFaceList.findAt(PointOnFace)
            region2=regionToolset.Region(side1Faces=side1Faces2)
            
            tempName2 = 'Poly'+str(number)+'Face'+str(numberFaceN+1)
            if len(side1Faces2)>0:
                mdb.models[ModelName].Tie(name=tempName2, master=region1, slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)
            numberFaceN = numberFaceN +1
	
        temprint = 'Defined Contact Particle' + str(number) + '-1  with Matrix'#颗粒名称
        print(temprint)


def DefineCohesiveContact(XmlFile,ModelName):
    a = mdb.models[ModelName].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, constraints=ON, connectors=ON, engineeringFeatures=ON)
    mdb.models[ModelName].ContactProperty('CohesiveProperty')#接触属性
    mdb.models[ModelName].interactionProperties['CohesiveProperty'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, 
        table=((0.1, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)#相切属性
    mdb.models[ModelName].interactionProperties['CohesiveProperty'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, 
        constraintEnforcementMethod=DEFAULT)#法向默认属性
    mdb.models[ModelName].interactionProperties['CohesiveProperty'].CohesiveBehavior(
        defaultPenalties=OFF, table=((300000.0, 100000.0, 100000.0), ))#内聚力刚度
    mdb.models[ModelName].interactionProperties['CohesiveProperty'].Damage(
        initTable=((400, 400, 400), ), useEvolution=ON, evolTable=((3E-6, ), ))#内聚力初始损伤和演化,界面厚度1um
        
    doc = PolyReadXml(XmlFile)    
    PolyNumber = doc.GetPolyhedralNumber()#颗粒的数量获取
    
    a = mdb.models[ModelName].rootAssembly
    MatrixFaceList = a.instances['MatrixAl-1'].faces
    
    for number in range(1,PolyNumber+1):#颗粒循环
        tempName = 'Particle' + str(number) + '-1'#颗粒名称
        PolyFaceList = a.instances[tempName].faces
        numberFaceN = 0
        
        for PolyFace in PolyFaceList:
            PointOnFace = PolyFace.pointOn
            
            side1Faces1 = PolyFaceList.findAt(PointOnFace)
            region1=regionToolset.Region(side1Faces=side1Faces1)
            
            side1Faces2 = MatrixFaceList.findAt(PointOnFace)
            region2=regionToolset.Region(side1Faces=side1Faces2)
            
            tempName2 = 'Poly'+str(number)+'Face'+str(numberFaceN+1)
            if len(side1Faces2)>0:
                #mdb.models[ModelName].Tie(name=tempName2, master=region1, slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)enforcement=NODE_TO_SURFACE,
                mdb.models[ModelName].SurfaceToSurfaceContactStd(name=tempName2, createStepName='Initial', master=region1, slave=region2, sliding=SMALL, enforcement=NODE_TO_SURFACE, thickness=OFF, interactionProperty='CohesiveProperty', 
                    surfaceSmoothing=NONE, adjustMethod=OVERCLOSED, smooth=0.2, initialClearance=OMIT, datumAxis=None, clearanceRegion=None, tied=OFF)
            numberFaceN = numberFaceN +1
	
        temprint = 'Defined Contact Particle' + str(number) + '-1  with Matrix'#颗粒名称
        print(temprint)    
    
#定义边界和载荷         
def DefineLoadAndBC(XmlFile,ModelName,odbFileName,DegreeFreedom,GlobalStep,SubRelative,subScale):
    #获取要加载的边界
    doc = PolyReadXml(XmlFile) 
    


#对颗粒和基体进行网格划分
def MeshParts(XmlFile,ModelName,MatrixMeshSize,ParticleMeshSize,TransitionMeshSize):
    doc = PolyReadXml(XmlFile) 
    
    #进入网格划分模块
    session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(meshTechnique=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=OFF)

    # 设置基体的种子
    p = mdb.models[ModelName].parts['MatrixAl']
    p.seedPart(size=float(MatrixMeshSize), deviationFactor=0.1, minSizeFactor=0.1)#设置整体的网格尺寸----

    c = p.cells 
    pickedRegions =c[0:len(c)]
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    #设置网格类型
    elemType1 = mesh.ElemType(elemCode=C3D20R, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D15, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD)
    
    p = mdb.models[ModelName].parts['MatrixAl']
    c = p.cells
    cells = c[0:len(c)]
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    
    p.generateMesh()#生成网格
            
            
    # 对颗粒进行网格划分
    NumPoly = doc.GetPolyhedralNumber()
    for i in range(1,NumPoly+1):
        tempName = 'Particle' + str(i)
        p = mdb.models[ModelName].parts[tempName]
        p.seedPart(size= float(ParticleMeshSize), deviationFactor=0.1, minSizeFactor=0.1)#设置整体的网格尺寸----
        
        c = p.cells
        pickedRegions =(c[0:len(c)])
        p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
        #设置网格类型
        elemType1 = mesh.ElemType(elemCode=C3D20R, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=C3D15, elemLibrary=STANDARD)
        elemType3 = mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD)
        
        p = mdb.models[ModelName].parts[tempName]
        c = p.cells
        cells = c[0:len(c)]
        pickedRegions =(cells, )
        p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
        p.generateMesh()
        
        
    def SummitJob(ModelName,):
        a = mdb.models[ModelName].rootAssembly
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
        session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=OFF)
        mdb.Job(name='Job1', model=ModelName, description='', type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
            numGPUs=0)
        mdb.jobs['Job1'].submit(consistencyChecking=OFF)
   

#提交仿真    
def DefineJob(ModelName,jobName,ProcessorNumber):
    a = mdb.models[ModelName].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=OFF)
    mdb.Job(name=jobName, model=ModelName, description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=int(ProcessorNumber), 
        numDomains=int(ProcessorNumber), numGPUs=0)
    #mdb.jobs[jobName].submit(consistencyChecking=OFF)
   
# Python读取xml的库  
class PolyReadXml():
    xmlPointPrecision = 10

    def __init__(self, xmlPath):
        self.xmlPath = xmlPath


    # 获取xml中有多少个颗粒
    def GetPolyhedralNumber(self):
        dom = xml.dom.minidom.parse(self.xmlPath)  # 打开xml文档
        # 得到文档元素对象
        root = dom.documentElement  # 获取根节点
        sequence_list = root.getElementsByTagName("Polyhedral")  # 获取多面体序列
        return len(sequence_list)

# 获取第i个多面体的线的tuple信息
    def GetMatrixLineTuple(self):
        dom = xml.dom.minidom.parse(self.xmlPath)
        root = dom.documentElement
        PolyList = root.getElementsByTagName("MatrixCell")  # 获取第i个的节点

        FaceNode = PolyList[0].getElementsByTagName("PolyFaces")  # 获取节点
        FaceList = FaceNode[0].getElementsByTagName("Face")  # 获取面的节点列表节点

        # 获取所有的面的信息
        PolyFace = []
        for face in FaceList:
            facePointList = face.getElementsByTagName("FacePoint")  # 获取面的节点列表节点
            FacePoint = []  # [[] for i in range(3)]  # 存放点的信息
            for point in facePointList:
                tempX = float(point.getAttribute("X"))
                tempY = float(point.getAttribute("Y"))
                tempZ = float(point.getAttribute("Z"))
                tempTuple = tuple([round(tempX, self.xmlPointPrecision), round(tempY, self.xmlPointPrecision),
                                   round(tempZ, self.xmlPointPrecision)])
                FacePoint.append(tempTuple)
            PolyFace.append(FacePoint)
        # print(PolyFace)

        # 依次生成直线
        PolyFaceLine = []
        for face in PolyFace:
            for i in range(0, len(face) - 1):
                tempLine = tuple([face[i], face[i + 1]])
                PolyFaceLine.append(tempLine)
            tempLine = tuple([face[len(face) - 1], face[0]])
            PolyFaceLine.append(tempLine)
        # 首尾相连的直线
        tempPolyLine = tuple(PolyFaceLine)
        return tempPolyLine
        # print(tempPolyLine)




    # 获取第i个多面体的线的tuple信息
    def GetLineTuple(self, numberPoly):
        dom = xml.dom.minidom.parse(self.xmlPath)
        root = dom.documentElement
        PolyList = root.getElementsByTagName("Polyhedral")  # 获取第i个的节点

        FaceNode = PolyList[numberPoly - 1].getElementsByTagName("PolyFaces")  # 获取节点
        FaceList = FaceNode[0].getElementsByTagName("Face")  # 获取面的节点列表节点

        # 获取所有的面的信息
        PolyFace = []
        for face in FaceList:
            facePointList = face.getElementsByTagName("FacePoint")  # 获取面的节点列表节点
            FacePoint = []  # [[] for i in range(3)]  # 存放点的信息
            for point in facePointList:
                tempX = float(point.getAttribute("X"))
                tempY = float(point.getAttribute("Y"))
                tempZ = float(point.getAttribute("Z"))
                tempTuple = tuple([round(tempX, self.xmlPointPrecision), round(tempY, self.xmlPointPrecision),
                                   round(tempZ, self.xmlPointPrecision)])
                FacePoint.append(tempTuple)
            PolyFace.append(FacePoint)
        # print(PolyFace)

        # 依次生成直线
        PolyFaceLine = []
        for face in PolyFace:
            for i in range(0, len(face) - 1):
                tempLine = tuple([face[i], face[i + 1]])
                PolyFaceLine.append(tempLine)
            tempLine = tuple([face[len(face) - 1], face[0]])
            PolyFaceLine.append(tempLine)
        # 首尾相连的直线
        tempPolyLine = tuple(PolyFaceLine)
        return tempPolyLine
        # print(tempPolyLine)

        # 获取第i个多面体的线的tuple信息
    def GetPolyLineTuple(self):
        dom = xml.dom.minidom.parse(self.xmlPath)
        root = dom.documentElement
        PolyListRoot = root.getElementsByTagName("Polyhedral")  # 获取第i个的节点
        PolyLineList = []
        for PolyList in PolyListRoot:
        
            FaceNode = PolyList.getElementsByTagName("PolyFaces")  # 获取节点
            FaceList = FaceNode[0].getElementsByTagName("Face")  # 获取面的节点列表节点

            # 获取所有的面的信息
            PolyFace = []
            for face in FaceList:
                facePointList = face.getElementsByTagName("FacePoint")  # 获取面的节点列表节点
                FacePoint = []  # [[] for i in range(3)]  # 存放点的信息
                for point in facePointList:
                    tempX = float(point.getAttribute("X"))
                    tempY = float(point.getAttribute("Y"))
                    tempZ = float(point.getAttribute("Z"))
                    tempTuple = tuple([round(tempX, self.xmlPointPrecision), round(tempY, self.xmlPointPrecision),
                                       round(tempZ, self.xmlPointPrecision)])
                    FacePoint.append(tempTuple)
                PolyFace.append(FacePoint)
            # print(PolyFace)

            # 依次生成直线
            PolyFaceLine = []
            for face in PolyFace:
                for i in range(0, len(face) - 1):
                    tempLine = tuple([face[i], face[i + 1]])
                    PolyFaceLine.append(tempLine)
                tempLine = tuple([face[len(face) - 1], face[0]])
                PolyFaceLine.append(tempLine)
            # 首尾相连的直线
            tempPolyLine = tuple(PolyFaceLine)
            PolyLineList.append(tempPolyLine)
        return PolyLineList
        # print(tempPolyLine)

    # 获取每个面的线的中点
    def GetMatrixFaceLineCenterTuple(self):
        dom = xml.dom.minidom.parse(self.xmlPath)
        root = dom.documentElement
        PolyList = root.getElementsByTagName("MatrixCell")  # 获取第i个的节点

        FaceNode = PolyList[0].getElementsByTagName("PolyFaces")  # 获取节点
        FaceList = FaceNode[0].getElementsByTagName("Face")  # 获取面的节点列表节点

        # 获取所有的面的信息
        PolyFace = []
        for face in FaceList:

            facePointList = face.getElementsByTagName("FacePoint")  # 获取面的节点列表节点
            FacePoint = [[] for i in range(3)]  # 存放点的信息
            for point in facePointList:
                FacePoint[0].append(float(point.getAttribute("X")))
                FacePoint[1].append(float(point.getAttribute("Y")))
                FacePoint[2].append(float(point.getAttribute("Z")))
            PolyFace.append(FacePoint)


        # 依次生成直线中点
        PolyFaceLineCenter = []
        for face in PolyFace:
            FaceLineCenter = []
            for i in range(0, len(face[0]) - 1):
                tempX = (face[0][i] + face[0][i + 1]) / 2.0
                tempY = (face[1][i] + face[1][i + 1]) / 2.0
                tempZ = (face[2][i] + face[2][i + 1]) / 2.0
                tempLineCenter = tuple([round(tempX, self.xmlPointPrecision + 1), round(tempY, self.xmlPointPrecision + 1), round(tempZ, self.xmlPointPrecision + 1)])
                FaceLineCenter.append(tempLineCenter)

            tempX = (face[0][len(face[0]) - 1] + face[0][0]) / 2.0
            tempY = (face[1][len(face[0]) - 1] + face[1][0]) / 2.0
            tempZ = (face[2][len(face[0]) - 1] + face[2][0]) / 2.0
            tempLineCenter = tuple([round(tempX, self.xmlPointPrecision + 1), round(tempY, self.xmlPointPrecision + 1),
                                    round(tempZ, self.xmlPointPrecision + 1)])
            FaceLineCenter.append(tempLineCenter)

            PolyFaceLineCenter.append(FaceLineCenter)

        # print(PolyFaceLineCenter)
        return PolyFaceLineCenter



    # 获取每个面的线的中点
    def GetFaceLineCenterTuple(self, numberPoly):
        dom = xml.dom.minidom.parse(self.xmlPath)
        root = dom.documentElement
        PolyList = root.getElementsByTagName("Polyhedral")  # 获取第i个的节点

        FaceNode = PolyList[numberPoly - 1].getElementsByTagName("PolyFaces")  # 获取节点
        FaceList = FaceNode[0].getElementsByTagName("Face")  # 获取面的节点列表节点

        # 获取所有的面的信息
        PolyFace = []
        for face in FaceList:

            facePointList = face.getElementsByTagName("FacePoint")  # 获取面的节点列表节点
            FacePoint = [[] for i in range(3)]  # 存放点的信息
            for point in facePointList:
                FacePoint[0].append(float(point.getAttribute("X")))
                FacePoint[1].append(float(point.getAttribute("Y")))
                FacePoint[2].append(float(point.getAttribute("Z")))
            PolyFace.append(FacePoint)


        # 依次生成直线中点
        PolyFaceLineCenter = []
        for face in PolyFace:
            FaceLineCenter = []
            for i in range(0, len(face[0]) - 1):
                tempX = (face[0][i] + face[0][i + 1]) / 2.0
                tempY = (face[1][i] + face[1][i + 1]) / 2.0
                tempZ = (face[2][i] + face[2][i + 1]) / 2.0
                tempLineCenter = tuple([round(tempX, self.xmlPointPrecision + 1), round(tempY, self.xmlPointPrecision + 1), round(tempZ, self.xmlPointPrecision + 1)])
                FaceLineCenter.append(tempLineCenter)

            tempX = (face[0][len(face[0]) - 1] + face[0][0]) / 2.0
            tempY = (face[1][len(face[0]) - 1] + face[1][0]) / 2.0
            tempZ = (face[2][len(face[0]) - 1] + face[2][0]) / 2.0
            tempLineCenter = tuple([round(tempX, self.xmlPointPrecision + 1), round(tempY, self.xmlPointPrecision + 1),
                                    round(tempZ, self.xmlPointPrecision + 1)])
            FaceLineCenter.append(tempLineCenter)

            PolyFaceLineCenter.append(FaceLineCenter)

        # print(PolyFaceLineCenter)
        return PolyFaceLineCenter

    # 获取每个面的线的中点
    def GetPolyFaceLineCenterTuple(self):
        dom = xml.dom.minidom.parse(self.xmlPath)
        root = dom.documentElement
        PolyListRoot = root.getElementsByTagName("Polyhedral")  # 获取第i个的节点
        PolyFaceLineCenterList = []
        for PolyList in PolyListRoot:
            FaceNode = PolyList.getElementsByTagName("PolyFaces")  # 获取节点
            FaceList = FaceNode[0].getElementsByTagName("Face")  # 获取面的节点列表节点

            # 获取所有的面的信息
            PolyFace = []
            for face in FaceList:

                facePointList = face.getElementsByTagName("FacePoint")  # 获取面的节点列表节点
                FacePoint = [[] for i in range(3)]  # 存放点的信息
                for point in facePointList:
                    FacePoint[0].append(float(point.getAttribute("X")))
                    FacePoint[1].append(float(point.getAttribute("Y")))
                    FacePoint[2].append(float(point.getAttribute("Z")))
                PolyFace.append(FacePoint)


            # 依次生成直线中点
            PolyFaceLineCenter = []
            for face in PolyFace:
                FaceLineCenter = []
                for i in range(0, len(face[0]) - 1):
                    tempX = (face[0][i] + face[0][i + 1]) / 2.0
                    tempY = (face[1][i] + face[1][i + 1]) / 2.0
                    tempZ = (face[2][i] + face[2][i + 1]) / 2.0
                    tempLineCenter = tuple([round(tempX, self.xmlPointPrecision + 1), round(tempY, self.xmlPointPrecision + 1), round(tempZ, self.xmlPointPrecision + 1)])
                    FaceLineCenter.append(tempLineCenter)

                tempX = (face[0][len(face[0]) - 1] + face[0][0]) / 2.0
                tempY = (face[1][len(face[0]) - 1] + face[1][0]) / 2.0
                tempZ = (face[2][len(face[0]) - 1] + face[2][0]) / 2.0
                tempLineCenter = tuple([round(tempX, self.xmlPointPrecision + 1), round(tempY, self.xmlPointPrecision + 1),
                                        round(tempZ, self.xmlPointPrecision + 1)])
                FaceLineCenter.append(tempLineCenter)

                PolyFaceLineCenter.append(FaceLineCenter)
            PolyFaceLineCenterList.append(PolyFaceLineCenter)
        # print(PolyFaceLineCenter)
        return PolyFaceLineCenterList


    # 获取基体信息
    def GetMatrixInfo(self):
        dom = xml.dom.minidom.parse(self.xmlPath)  # 打开xml文档
        # print("start reading xml")
        # 得到文档元素对象
        root = dom.documentElement  # 获取根节点
        LimitsList = root.getElementsByTagName("MatrixSize")  # 获取基体限制
        LimitX = float(LimitsList[0].getAttribute("X"))
        LimitY = float(LimitsList[0].getAttribute("Y"))
        LimitZ = float(LimitsList[0].getAttribute("Z"))

        tempXY = tuple([LimitX, LimitY])
        tempZ = LimitZ
        tempXYZ = tuple([-LimitX / 2.0, -LimitY / 2.0, -LimitZ / 2.0])

        return [tempXY, tempZ, tempXYZ]

    # 获取每个面的中点
    def GetFaceCenterTupleBy2Line(self, numberPoly):
        # 获取基体信息
        [a,b,tempXYZ] =  self.GetMatrixInfo()
        MatrixXYZ = [tempXYZ[0],-tempXYZ[0],tempXYZ[1],-tempXYZ[1],tempXYZ[2],-tempXYZ[2]]
        
        FaceLineList = self.GetFaceLineCenterTuple(numberPoly)
        FaceSect = []
        for face in FaceLineList:
            tempX = (face[0][0] + face[1][0]) / 2.0
            tempY = (face[0][1] + face[1][1]) / 2.0
            tempZ = (face[0][2] + face[1][2]) / 2.0
            if tempX in MatrixXYZ or tempY in MatrixXYZ or tempZ in MatrixXYZ:
                break
           
            tempFaceSect = tuple([round(tempX, self.xmlPointPrecision + 1), round(tempY, self.xmlPointPrecision + 1),
                                  round(tempZ, self.xmlPointPrecision + 1)])
            FaceSect.append(tempFaceSect)

        return FaceSect
        
    def GetFaceCenterTuple(self, numberPoly):
        # 获取基体信息
        [a,b,tempXYZ] =  self.GetMatrixInfo()
        MatrixXYZ = [tempXYZ[0],-tempXYZ[0],tempXYZ[1],-tempXYZ[1],tempXYZ[2],-tempXYZ[2]]

        dom = xml.dom.minidom.parse(self.xmlPath)
        root = dom.documentElement
        PolyList = root.getElementsByTagName("Polyhedral")  # 获取第i个的节点

        FaceNode = PolyList[numberPoly - 1].getElementsByTagName("PolyFaces")  # 获取节点
        FaceList = FaceNode[0].getElementsByTagName("Face")  # 获取面的节点列表节点

        # 获取所有的面的信息
        PolyFace = []
        for face in FaceList:
            tempX = float(face.getAttribute("X"))
            tempY = float(face.getAttribute("Y"))
            tempZ = float(face.getAttribute("Z"))

            if tempX in MatrixXYZ or tempY in MatrixXYZ or tempZ in MatrixXYZ:
                break
            else:
                PolyFace.append(tuple([tempX,tempY,tempZ]))
        return PolyFace


    #获取基体内部小边界的中点值
    def GetMatrixInFaceCenter(self):
        #获取多面体的数量
        MatrixLinceCenter = []
        NumPoly = self.GetPolyhedralNumber()
        for i in range(1,NumPoly+1):
            #获取单个多面体上的中点值，并转换成tuple
            FacesLineCenter = self.GetFaceLineCenterTuple(i)
            for LineCenter in FacesLineCenter:
                MatrixLinceCenter = MatrixLinceCenter + LineCenter

        return tuple(MatrixLinceCenter)
        
    # 获取颗粒面的中点值
    def GetPolyFaceLineCenter(self,i):
        FacesLineCenter = self.GetFaceLineCenterTuple(i)
        PolyLinceCenter = []
        for LineCenter in FacesLineCenter:
            PolyLinceCenter = PolyLinceCenter + LineCenter
        return tuple(PolyLinceCenter)    
        
              
    # 获取颗粒要加载的面Z，第一个为固定，第二个为加载，[[3], [(0.1047, -0.0217525, -0.5)]]
    def GetPolyBCLoadTuple(self):
        # 获取基体信息
        [a, b, tempXYZ] = self.GetMatrixInfo()

        FaceNumber = self.GetPolyhedralNumber()
        Fix_BC = [[] for t in range(2)]
        Load_Face = [[] for t in range(2)]
        for i in range(1,FaceNumber):#逐个读取多面体
            FaceLineList = self.GetFaceLineCenterTuple(i)
            for face in FaceLineList:
                tempX = (face[0][0] + face[1][0]) / 2.0
                tempY = (face[0][1] + face[1][1]) / 2.0
                tempZ = (face[0][2] + face[1][2]) / 2.0
                if tempZ <= tempXYZ[2]: # -Z方向，固定载荷
                    tempFaceSect = tuple(
                        [round(tempX, self.xmlPointPrecision + 1), round(tempY, self.xmlPointPrecision + 1),
                         round(tempZ, self.xmlPointPrecision + 1)])
                    Fix_BC[1].append(tempFaceSect)
                    Fix_BC[0].append(i)

                if tempZ >= -tempXYZ[2]:# Z方向，力载荷
                    tempFaceSect = tuple(
                        [round(tempX, self.xmlPointPrecision + 1), round(tempY, self.xmlPointPrecision + 1),
                         round(tempZ, self.xmlPointPrecision + 1)])
                    Load_Face[1].append(tempFaceSect)
                    Load_Face[0].append(i)

        return [Fix_BC,Load_Face]

    # 获取基体要加载的面Z，第一个返回值为固定，第二个返回值为加载
    def GetMatrixBCLoadTuple(self):
        # 获取到在Z正负方向的点集
        [a, b, tempXYZ] = self.GetMatrixInfo()

        FaceNumber = self.GetPolyhedralNumber()

        Fix_BC = []
        Load_Face = []

        for i in range(1, FaceNumber):  # 逐个读取多面体
            dom = xml.dom.minidom.parse(self.xmlPath)
            root = dom.documentElement
            PolyList = root.getElementsByTagName("Polyhedral")  # 获取第i个的节点
            FaceNode = PolyList[i - 1].getElementsByTagName("PolyFaces")  # 获取节点
            FaceList = FaceNode[0].getElementsByTagName("Face")  # 获取面的节点列表节点

            # 获取所有的面的信息

            for face in FaceList:
                tempZ = float(face.getAttribute("Z"))
                if tempZ <= tempXYZ[2]: # 判断固定面的坐标
                    #如果存在，则读取相应的面上点击的坐标
                    PointList = face.getElementsByTagName("FacePoint")
                    PolyFace = []
                    for point in PointList:
                        tempX = float(point.getAttribute("X"))
                        tempY = float(point.getAttribute("Y"))
                        tempZ = float(point.getAttribute("Z"))
                        PolyFace.append([tempX,tempY,tempZ])
                    Fix_BC.append(PolyFace)

                if tempZ >= -tempXYZ[2]: # 判断固定面的坐标
                    #如果存在，则读取相应的面上点击的坐标
                    PointList = face.getElementsByTagName("FacePoint")
                    PolyFace = []
                    for point in PointList:
                        tempX = float(point.getAttribute("X"))
                        tempY = float(point.getAttribute("Y"))
                        tempZ = float(point.getAttribute("Z"))
                        PolyFace.append([tempX,tempY,tempZ])
                    Load_Face.append(PolyFace)

        # return [Fix_BC,Load_Face]
        Fix_BC_Box = self.GetLimtsList(Fix_BC)
        Load_Face_Box = self.GetLimtsList(Load_Face)

        RandomFix_BCPoint = self.GetRandomPointOutBox(tempXYZ,Fix_BC_Box,1)
        RandomLoad_FacePoint = self.GetRandomPointOutBox(tempXYZ,Load_Face_Box,-1)

        return [tuple(RandomFix_BCPoint),tuple(RandomLoad_FacePoint)]


    #根据列表获取包围盒
    def GetLimtsList(self,BC):
        BoxBounding = []
        for PolyFace in BC:
            ListX = []
            ListY = []
            for FacePoints in PolyFace:
                ListX.append(FacePoints[0])
                ListY.append(FacePoints[1])
            BoxBounding.append([min(ListX),max(ListX),min(ListY),max(ListY)])
        return BoxBounding

    # 随机生成一点，在切割的平面外
    def GetRandomPointOutBox(self,Limits,BoxBounding,Status):
        import random
        #随机生成一个点，在基体面内
        while True:
            RandomX = random.random()*(-Limits[0]) - (-Limits[0])
            RandomY = random.random() * (-Limits[1]) - (-Limits[1])
            for box in BoxBounding:
                #判断点是否在box内部
                if RandomX > box[0] or RandomX < box[1] or RandomY > box[2] or RandomY < box[3]:
                    continue
            return [round(RandomX, self.xmlPointPrecision + 1),round(RandomY, self.xmlPointPrecision + 1),Limits[2]*Status]


def TestEnd():
    print('end')
