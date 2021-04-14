# -* - coding:UTF-8 -*- 
# Do not delete the following import lines
from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class PRMMCs_3DGeom_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='Polygon3DFunction',objectName='pRMMCs_3DGeomModul', registerQuery=False)
        pickedDefault = ''
        self.XmlFileKw = AFXStringKeyword(self.cmd, 'XmlFile', True, r'G:\ABAQUS2020\SubModelTest\Geom.xml')
        self.MatrixSizeXKw = AFXStringKeyword(self.cmd, 'MatrixSizeX', True, '20')
        self.MatrixSizeYKw = AFXStringKeyword(self.cmd, 'MatrixSizeY', True, '20')
        self.MatrixSizeZKw = AFXStringKeyword(self.cmd, 'MatrixSizeZ', True, '20')
        self.VolFKw = AFXStringKeyword(self.cmd, 'VolF', True, '0.2')
        self.ParticleSizeKw = AFXStringKeyword(self.cmd, 'ParticleSize', True, '5')
        self.TransitonRatioKw = AFXStringKeyword(self.cmd, 'TransitonRatio', True, '5')
        self.TransitonSizeKw = AFXStringKeyword(self.cmd, 'TransitonSize', True, '0.1')

        #Mesh Setting
        self.MatrixMeshSizeKw = AFXStringKeyword(self.cmd, 'MatrixMeshSize', True, '1')
        self.ParticleMeshSizeKw = AFXStringKeyword(self.cmd, 'ParticleMeshSize', True, '1')
        self.TransitionMeshSizeKw = AFXStringKeyword(self.cmd, 'TransitionMeshSize', True, '1')

        #Material Setting
        self.CompositeMaterialKw = AFXStringKeyword(self.cmd, 'CompositeMaterial', True, 'Al2009SiC')
        self.MatrixMaterialKw = AFXStringKeyword(self.cmd, 'MatrixMaterial', True, 'Al2009')
        self.ParticleMaterialKw = AFXStringKeyword(self.cmd, 'ParticleMaterial', True, 'SiC')
        self.MaterialTableKw = AFXTableKeyword(self.cmd, 'MaterialTable', True)
        self.MaterialTableKw.setColumnType(0, AFXTABLE_TYPE_STRING)
        self.MaterialTableKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        self.MaterialTableKw.setColumnType(2, AFXTABLE_TYPE_STRING)

        # Step Setting
        self.StepTypeKw = AFXStringKeyword(self.cmd, 'StepType', True, 'Static,General')

        if not self.radioButtonGroups.has_key('Response'):#Steady-state
            self.ResponseKw1 = AFXIntKeyword(None, 'ResponseDummy', True)
            self.ResponseKw2 = AFXStringKeyword(self.cmd, 'Response', True)
            self.radioButtonGroups['Response'] = (self.ResponseKw1, self.ResponseKw2, {})
        self.radioButtonGroups['Response'][2][253] = 'Steady-state'
        self.ResponseKw1.setValue(253)

        if not self.radioButtonGroups.has_key('Response'):#HFrame4
            self.ResponseKw1 = AFXIntKeyword(None, 'ResponseDummy', True)
            self.ResponseKw2 = AFXStringKeyword(self.cmd, 'Response', True)
            self.radioButtonGroups['Response'] = (self.ResponseKw1, self.ResponseKw2, {})
        self.radioButtonGroups['Response'][2][254] = 'Transient'

        self.TimePeriodKw = AFXStringKeyword(self.cmd, 'TimePeriod', True, '1')


        #Step --- Incrementation 
        if not self.radioButtonGroups.has_key('IncType'):
            self.IncTypeKw1 = AFXIntKeyword(None, 'IncTypeDummy', True)
            self.IncTypeKw2 = AFXStringKeyword(self.cmd, 'IncType', True)
            self.radioButtonGroups['IncType'] = (self.IncTypeKw1, self.IncTypeKw2, {})
        self.radioButtonGroups['IncType'][2][255] = 'Automatic'
        self.IncTypeKw1.setValue(255)

        if not self.radioButtonGroups.has_key('IncType'):
            self.IncTypeKw1 = AFXIntKeyword(None, 'IncTypeDummy', True)
            self.IncTypeKw2 = AFXStringKeyword(self.cmd, 'IncType' ,True)
            self.radioButtonGroups['IncType'] = (self.IncTypeKw1, self.IncTypeKw2, {})
        self.radioButtonGroups['IncType'][2][256] = 'Fixed'
        
        self.MaxNumKw = AFXStringKeyword(self.cmd, 'MaxIncNum', True, '200')
        self.InitialIncKw = AFXStringKeyword(self.cmd, 'InitialInc', True, '1')
        self.MinIncKw = AFXStringKeyword(self.cmd, 'MinInc', True, '0.05')
        self.MaxIncKw = AFXStringKeyword(self.cmd, 'MaxInc', True, '1')
        self.tempMaxCheckboxKw = AFXBoolKeyword(self.cmd, 'tempMaxCheckbox', AFXBoolKeyword.TRUE_FALSE, True, True)
        self.tempMaxValueKw = AFXStringKeyword(self.cmd, 'tempMaxValue', True, '5')

        # Load Setting
        self.odbFileNameKw = AFXStringKeyword(self.cmd, 'odbFileName', True, '')
        self.DegreeFreedomKw = AFXStringKeyword(self.cmd, 'DegreeFreedom', True, '1,2,3')
        self.GlobalStepKw = AFXStringKeyword(self.cmd, 'GlobalStep', True, '1')
        self.SubRelativeKw = AFXStringKeyword(self.cmd, 'SubRelative', True, '0.05')
        self.subScaleKw = AFXStringKeyword(self.cmd, 'subScale', True, '1')

        # Job Setting
        self.ModelNameKw = AFXStringKeyword(self.cmd, 'ModelName', True, 'D2')
        self.jobNameKw = AFXStringKeyword(self.cmd, 'jobName', True, 'D2-Job')
        self.ProcessorNumberKw = AFXStringKeyword(self.cmd, 'ProcessorNumber', True, '15')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import pRMMCs_3DGeomDB
        return pRMMCs_3DGeomDB.PRMMCs_3DGeomDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='PRMMCs_3DGeom_Tool', 
    object=PRMMCs_3DGeom_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    kernelInitString='import pRMMCs_3DGeomModul',
    applicableModules=ALL,
    version='N/A',
    author='N/A',
    description='N/A',
    helpUrl='N/A'
)
