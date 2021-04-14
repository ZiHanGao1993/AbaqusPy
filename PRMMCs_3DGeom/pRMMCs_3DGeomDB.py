# -* - coding:UTF-8 -*- 
# Do not delete the following import lines
from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os
from mlab.releases import latest_release as matlab 
import xml.dom.minidom

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class PRMMCs_3DGeomDB(AFXDataDialog):
    ID_GeomTool = AFXDataDialog.ID_LAST
    ID_ReadData = ID_GeomTool +1
    ID_Show = ID_GeomTool +2
    ID_SingleRVE = ID_GeomTool+3
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'PRMMCs_3D_Geom_Tool',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        TabBook_1 = FXTabBook(p=self, tgt=None, sel=0,
            opts=TABBOOK_NORMAL,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING)
        tabItem = FXTabItem(p=TabBook_1, text='Geometry', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_1 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        fileHandler = PRMMCs_3DGeomDBFileHandler(form, 'XmlFile', '*xml')
        fileTextHf = FXHorizontalFrame(p=TabItem_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        fileTextHf.setSelector(99)
        AFXTextField(p=fileTextHf, ncols=40, labelText='Geometry File:', tgt=form.XmlFileKw, sel=0,
            opts=AFXTEXTFIELD_STRING|LAYOUT_CENTER_Y)
        icon = afxGetIcon('fileOpen', AFX_ICON_SMALL )
        FXButton(p=fileTextHf, text='	Select File\nFrom Dialog', ic=icon, tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)
        HFrame_2 = FXHorizontalFrame(p=TabItem_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        #l = FXLabel(p=HFrame_2, text='[GeomTool]', opts=JUSTIFY_LEFT)
        #l = FXLabel(p=HFrame_2, text='[Read Data]', opts=JUSTIFY_LEFT)
        #l = FXLabel(p=HFrame_2, text='[Show]', opts=JUSTIFY_LEFT)
        # 注册三个按钮
        FXMAPFUNC(self, SEL_COMMAND, self.ID_GeomTool,PRMMCs_3DGeomDB.onCmdMybutton)
        FXButton(p=HFrame_2, text='Geom Tool', ic= None, tgt= self, sel= self.ID_GeomTool, opts = BUTTON_NORMAL)
        
        FXMAPFUNC(self, SEL_COMMAND, self.ID_ReadData,PRMMCs_3DGeomDB.onCmdMybutton)
        FXButton(p=HFrame_2, text='Read Data', ic= None, tgt= self, sel= self.ID_ReadData, opts = BUTTON_NORMAL)
        
        FXMAPFUNC(self, SEL_COMMAND, self.ID_Show,PRMMCs_3DGeomDB.onCmdMybutton)
        FXButton(p=HFrame_2, text='Show Geom', ic= None, tgt= self, sel= self.ID_Show, opts = BUTTON_NORMAL)
        
        FXMAPFUNC(self, SEL_COMMAND, self.ID_SingleRVE,PRMMCs_3DGeomDB.onCmdMybutton)
        FXButton(p=HFrame_2, text='SingleRVE', ic= None, tgt= self, sel= self.ID_SingleRVE, opts = BUTTON_NORMAL)
        
        
        HFrame_3 = FXHorizontalFrame(p=TabItem_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_1 = FXGroupBox(p=HFrame_3, text='Matrix Size', opts=FRAME_GROOVE)
        VAligner_5 = AFXVerticalAligner(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=VAligner_5, ncols=12, labelText='X:', tgt=form.MatrixSizeXKw, sel=0)
        AFXTextField(p=VAligner_5, ncols=12, labelText='Y:', tgt=form.MatrixSizeYKw, sel=0)
        AFXTextField(p=VAligner_5, ncols=12, labelText='Z:', tgt=form.MatrixSizeZKw, sel=0)
        VAligner_1 = AFXVerticalAligner(p=HFrame_3, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        
        AFXTextField(p=VAligner_1, ncols=12, labelText='Volume Fraction:', tgt=form.VolFKw, sel=0)
        AFXTextField(p=VAligner_1, ncols=12, labelText='Particle Size:', tgt=form.ParticleSizeKw, sel=0)
        AFXTextField(p=VAligner_1, ncols=12, labelText='Transition Ratio:', tgt=form.TransitonRatioKw, sel=0)
        AFXTextField(p=VAligner_1, ncols=12, labelText='Transition Size:', tgt=form.TransitonSizeKw, sel=0)
        tabItem = FXTabItem(p=TabBook_1, text='Mesh', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_3 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        VAligner_4 = AFXVerticalAligner(p=TabItem_3, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=VAligner_4, ncols=12, labelText='Matrix Size:', tgt=form.MatrixMeshSizeKw, sel=0)
        AFXTextField(p=VAligner_4, ncols=12, labelText='Particle Size:', tgt=form.ParticleMeshSizeKw, sel=0)
        AFXTextField(p=VAligner_4, ncols=12, labelText='Transition Size:', tgt=form.TransitionMeshSizeKw, sel=0)
        tabItem = FXTabItem(p=TabBook_1, text='Material', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_4 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        VAligner_6 = AFXVerticalAligner(p=TabItem_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        ComboBox_5 = AFXComboBox(p=VAligner_6, ncols=0, nvis=1, text='Composite:', tgt=form.CompositeMaterialKw, sel=0)
        ComboBox_5.setMaxVisible(10)
        ComboBox_5.appendItem(text='Al2009SiC')
        ComboBox_5.appendItem(text='Al2009')
        ComboBox_5.appendItem(text='SiC')
        ComboBox_3 = AFXComboBox(p=VAligner_6, ncols=0, nvis=1, text='Matrix:', tgt=form.MatrixMaterialKw, sel=0)
        ComboBox_3.setMaxVisible(10)
        ComboBox_3.appendItem(text='Al2009SiC')
        ComboBox_3.appendItem(text='Al2009')
        ComboBox_3.appendItem(text='SiC')
        ComboBox_4 = AFXComboBox(p=VAligner_6, ncols=0, nvis=1, text='Particle:', tgt=form.ParticleMaterialKw, sel=0)
        ComboBox_4.setMaxVisible(10)
        ComboBox_4.appendItem(text='Al2009SiC')
        ComboBox_4.appendItem(text='Al2009')
        ComboBox_4.appendItem(text='SiC')
        # if isinstance(TabItem_4, FXHorizontalFrame):
            # FXVerticalSeparator(p=TabItem_4, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        # else:
            # FXHorizontalSeparator(p=TabItem_4, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
            
            
        # vf = FXVerticalFrame(TabItem_4, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            # 0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
              # colored differently from its parent when the 'Color layout managers'
              # button is checked in the RSG Dialog Builder dialog.
        # vf.setSelector(99)
        # table = AFXTable(vf, 6, 4, 6, 4, form.MaterialTableKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        # table.setPopupOptions(AFXTable.POPUP_CUT|AFXTable.POPUP_COPY|AFXTable.POPUP_PASTE|AFXTable.POPUP_INSERT_ROW|AFXTable.POPUP_DELETE_ROW|AFXTable.POPUP_CLEAR_CONTENTS|AFXTable.POPUP_READ_FROM_FILE|AFXTable.POPUP_WRITE_TO_FILE)
        # table.setLeadingRows(1)
        # table.setLeadingColumns(1)
        # table.setColumnWidth(1, 100)
        # table.setColumnType(1, AFXTable.TEXT)
        # table.setColumnWidth(2, 100)
        # table.setColumnType(2, AFXTable.FLOAT)
        # table.setColumnWidth(3, 100)
        # table.setColumnType(3, AFXTable.TEXT)
        # table.setLeadingRowLabels('Type\tParameter\tDescribe')
        # table.setStretchableColumn( table.getNumColumns()-1 )
        # table.showHorizontalGrid(True)
        # table.showVerticalGrid(True)        
        
        
        tabItem = FXTabItem(p=TabBook_1, text='Step', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_7 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        ComboBox_8 = AFXComboBox(p=TabItem_7, ncols=0, nvis=1, text='Type:', tgt=form.StepTypeKw, sel=0)
        ComboBox_8.setMaxVisible(10)
        ComboBox_8.appendItem(text='Static,General')
        ComboBox_8.appendItem(text='Heat transfer')
        ComboBox_8.appendItem(text='Coupled temp-displacement')
        HFrame_4 = FXHorizontalFrame(p=TabItem_7, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_4, text='Response:', opts=JUSTIFY_LEFT)
        
        FXRadioButton(p=HFrame_4, text='Steady-state', tgt=form.ResponseKw1, sel=253)#静力分析
        FXRadioButton(p=HFrame_4, text='Transient', tgt=form.ResponseKw1, sel=254)#瞬态分析
        
        
        AFXTextField(p=TabItem_7, ncols=12, labelText='Time period:', tgt=form.TimePeriodKw, sel=0)
        GroupBox_2 = FXGroupBox(p=TabItem_7, text='Incrementation', opts=FRAME_GROOVE)
        HFrame_6 = FXHorizontalFrame(p=GroupBox_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_6, text='Type:', opts=JUSTIFY_LEFT)
        
        FXRadioButton(p=HFrame_6, text='Automatic', tgt=form.IncTypeKw1, sel=255)#自动步
        FXRadioButton(p=HFrame_6, text='Fixed', tgt=form.IncTypeKw1, sel=256)#固定步
        
        VAligner_7 = AFXVerticalAligner(p=GroupBox_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        
        AFXTextField(p=VAligner_7, ncols=12, labelText='Max Number:', tgt=form.MaxNumKw, sel=0)
        AFXTextField(p=VAligner_7, ncols=12, labelText='Initial:', tgt=form.InitialIncKw, sel=0)
        AFXTextField(p=VAligner_7, ncols=12, labelText='Minimum:', tgt=form.MinIncKw, sel=0)
        AFXTextField(p=VAligner_7, ncols=12, labelText='Maximun:', tgt=form.MaxIncKw, sel=0)
        HFrame_7 = FXHorizontalFrame(p=GroupBox_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        FXCheckButton(p=HFrame_7, text='Max.', tgt=form.tempMaxCheckboxKw, sel=0)
        AFXTextField(p=HFrame_7, ncols=12, labelText='allowable temperature change:', tgt=form.tempMaxValueKw, sel=0)
        tabItem = FXTabItem(p=TabBook_1, text='Load', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_5 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        fileHandler = PRMMCs_3DGeomDBFileHandler(form, 'odbFileName', '*odb')
        fileTextHf = FXHorizontalFrame(p=TabItem_5, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        fileTextHf.setSelector(99)
        AFXTextField(p=fileTextHf, ncols=40, labelText='ODB  Result:', tgt=form.odbFileNameKw, sel=0,
            opts=AFXTEXTFIELD_STRING|LAYOUT_CENTER_Y)
        icon = afxGetIcon('fileOpen', AFX_ICON_SMALL )
        FXButton(p=fileTextHf, text='	Select File\nFrom Dialog', ic=icon, tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)
        VAligner_8 = AFXVerticalAligner(p=TabItem_5, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=VAligner_8, ncols=12, labelText='Degrees of freedom:', tgt=form.DegreeFreedomKw, sel=0)
        AFXTextField(p=VAligner_8, ncols=12, labelText='Global step number:', tgt=form.GlobalStepKw, sel=0)
        AFXTextField(p=VAligner_8, ncols=12, labelText='Relative:', tgt=form.SubRelativeKw, sel=0)
        AFXTextField(p=VAligner_8, ncols=12, labelText='Scale:', tgt=form.subScaleKw, sel=0)
        tabItem = FXTabItem(p=TabBook_1, text='Job', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_6 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        VAligner_9 = AFXVerticalAligner(p=TabItem_6, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=VAligner_9, ncols=20, labelText='Model Name:', tgt=form.ModelNameKw, sel=0)
        AFXTextField(p=VAligner_9, ncols=20, labelText='Job Name:', tgt=form.jobNameKw, sel=0)
        AFXTextField(p=VAligner_9, ncols=20, labelText='Processor Number', tgt=form.ProcessorNumberKw, sel=0)
        self.form = form


    def onCmdMybutton(self, sender, sel, ptr):
        if SELID(sel) == self.ID_GeomTool: #打开建模工具软件
            mw = getAFXApp().getAFXMainWindow()
            mw.writeToMessageArea('Geom tool starting ...' ) 
            #添加工作目录
            x = matlab.path(matlab.path(),r'C:\Users\15321\abaqus_plugins\GeomPoly3D_Paper_matlab') 
            x = matlab.path(matlab.path(),r'C:\Users\15321\abaqus_plugins\GeomPoly3D_Paper_matlab\geom3d') 
            x = matlab.path(matlab.path(),r'C:\Users\15321\abaqus_plugins\GeomPoly3D_Paper_matlab\methods') 
            x = matlab.path(matlab.path(),r'C:\Users\15321\abaqus_plugins\GeomPoly3D_Paper_matlab\PolyExtrude') 
            x = matlab.path(matlab.path(),r'C:\Users\15321\abaqus_plugins\GeomPoly3D_Paper_matlab\polymat') 
            x = matlab.path(matlab.path(),r'C:\Users\15321\abaqus_plugins\GeomPoly3D_Paper_matlab\PolyRandomCut')  
            matlab.PRMMCsGeomTool()                        
            return 1      
        
        if SELID(sel) == self.ID_ReadData: #从xml中读取信息
            mw = getAFXApp().getAFXMainWindow()
            mw.writeToMessageArea('Get geom info ...' )    
            self.UpdateGeomInfo()
            return 1 
            
        if SELID(sel) == self.ID_Show: # 显示图片 生成exe函数                       
            #在DOS界面下输出提示信息
            mw = getAFXApp().getAFXMainWindow()
            mw.writeToMessageArea('Show picture ...' )        
            
            x = matlab.path(matlab.path(),r'C:\Users\15321\abaqus_plugins\GeomPoly3D_Paper_matlab') 
            x = matlab.path(matlab.path(),r'C:\Users\15321\abaqus_plugins\GeomPoly3D_Paper_matlab\geom3d') 
            x = matlab.path(matlab.path(),r'C:\Users\15321\abaqus_plugins\GeomPoly3D_Paper_matlab\methods') 
            x = matlab.path(matlab.path(),r'C:\Users\15321\abaqus_plugins\GeomPoly3D_Paper_matlab\PolyExtrude') 
            x = matlab.path(matlab.path(),r'C:\Users\15321\abaqus_plugins\GeomPoly3D_Paper_matlab\polymat') 
            x = matlab.path(matlab.path(),r'C:\Users\15321\abaqus_plugins\GeomPoly3D_Paper_matlab\PolyRandomCut')  

            xmlPath = self.form.XmlFileKw.getValue()#获取xml的路径
            number = matlab.PlotPolyhedralCellXml(xmlPath)
            tempPrint = 'the number of particles is ' + str(number)
            mw.writeToMessageArea(tempPrint)                    
            return 1   
        
        if SELID(sel) == self.ID_SingleRVE:#单颗粒模型
            mw = getAFXApp().getAFXMainWindow()
            mw.writeToMessageArea('Single RVE tool starting ...' ) 
            x = matlab.path(matlab.path(),r'G:\ABAQUS2020\CSTE_08\Single_Particle\GeomPoly3D_CSTE_Single') 
            x = matlab.path(matlab.path(),r'G:\ABAQUS2020\CSTE_08\Single_Particle\GeomPoly3D_CSTE_Single\SingleParticle')
            x = matlab.path(matlab.path(),r'G:\ABAQUS2020\CSTE_08\Single_Particle\GeomPoly3D_CSTE_Single\geom3d') 
            x = matlab.path(matlab.path(),r'G:\ABAQUS2020\CSTE_08\Single_Particle\GeomPoly3D_CSTE_Single\methods') 
            x = matlab.path(matlab.path(),r'G:\ABAQUS2020\CSTE_08\Single_Particle\GeomPoly3D_CSTE_Single\PolyExtrude') 
            x = matlab.path(matlab.path(),r'G:\ABAQUS2020\CSTE_08\Single_Particle\GeomPoly3D_CSTE_Single\polymat') 
            x = matlab.path(matlab.path(),r'G:\ABAQUS2020\CSTE_08\Single_Particle\GeomPoly3D_CSTE_Single\PolyRandomCut')
            matlab.SingleRVE()   
            return 1
        

    #更新信息
    def UpdateGeomInfo(self):
        xmlPath = self.form.XmlFileKw.getValue()#获取xml的路径
        #设置基体参数
        GeomInfoList = self.GetxmlInfo(xmlPath)
        
        InfoList = GeomInfoList
        mw = getAFXApp().getAFXMainWindow()
        mw.writeToMessageArea(str(InfoList))
        
        self.form.MatrixSizeXKw.setValue(str(InfoList[0][0]))
        self.form.MatrixSizeYKw.setValue(str(InfoList[0][1]))
        self.form.MatrixSizeZKw.setValue(str(InfoList[0][2]))
        
        self.form.ParticleSizeKw.setValue(str(InfoList[1]))
        self.form.VolFKw.setValue(str(InfoList[2]))

    def GetxmlInfo(self,xmlPath):
        dom = xml.dom.minidom.parse(xmlPath)  # 打开xml文档
        # 得到文档元素对象
        root = dom.documentElement  # 获取根节点
        # 获取基体尺寸
        LimitsList = root.getElementsByTagName("MatrixSize")  # 获取基体限制
        LimitX = float(LimitsList[0].getAttribute("X"))
        LimitY = float(LimitsList[0].getAttribute("Y"))
        LimitZ = float(LimitsList[0].getAttribute("Z"))
        MatrixSize = [LimitX,LimitY,LimitZ]

        #获取颗粒尺寸
        ParticleSizeList = []
        ParticleList = root.getElementsByTagName("Distribution")  # 获取基体限制
        for Particle in ParticleList:
            RadiusX = float(Particle.getAttribute("Max"))
            ZX=float(Particle.getAttribute("ZX"))
            YX=float(Particle.getAttribute("YX"))
            RadiusY = float(YX)*RadiusX
            RadiusZ = float(ZX)*RadiusX
            ParticleSizeList.append(max(RadiusX,RadiusY,RadiusZ))
        MaxParticleSize = max(ParticleSizeList)

        # 获取体积分数
        VolFnode = root.getElementsByTagName("VolF")  # 获取基体限制
        VolF = float(VolFnode[0].getAttribute("Value"))

        return [MatrixSize,MaxParticleSize,VolF]
    
###########################################################################
# Class definition
###########################################################################

class PRMMCs_3DGeomDBFileHandler(FXObject):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form, keyword, patterns='*'):

        self.form = form
        self.patterns = patterns
        self.patternTgt = AFXIntTarget(0)
        exec('self.fileNameKw = form.%sKw' % keyword)
        self.readOnlyKw = AFXBoolKeyword(None, 'readOnly', AFXBoolKeyword.TRUE_FALSE)
        FXObject.__init__(self)
        FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, PRMMCs_3DGeomDBFileHandler.activate)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def activate(self, sender, sel, ptr):

       fileDb = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select a File',
           self.fileNameKw, self.readOnlyKw,
           AFXSELECTFILE_ANY, self.patterns, self.patternTgt)
       fileDb.setReadOnlyPatterns('*.odb')
       fileDb.create()
       fileDb.showModal()
