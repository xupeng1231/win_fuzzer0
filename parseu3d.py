import sys
from rdpy.core.type import *
import random
import time
import copy

class BlockHeader(CompositeType):
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
        self.type=UInt32Le()
        self.dataSize=UInt32Le()
        self.metadataSize=UInt32Le()
class LString(CompositeType):
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
        self.len_=UInt16Le()
        self.str=String(readLen=CallableValue(lambda:self.len_.value))
    def __mutate__(self):
        CompositeType.mutate(self)
        self.len_.value=sizeof(self.str)#len(self.str.value)
class Block(CompositeType):
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
    def __read__(self,s):
        bl=BlockHeader()
        s.readNextType(bl)
        if bl.type.value==0x443355:
            self.b=Block443355(readLen=bl.dataSize+bl.metadataSize+12)
        elif bl.type.value==0xffffff14:
            self.b=Block14(readLen=bl.dataSize+bl.metadataSize+12)
        elif bl.type.value==0xffffff15:
            self.b=Block15(readLen=bl.dataSize+bl.metadataSize+12)
        elif bl.type.value==0xffffff21:
            self.b=Block21(readLen=bl.dataSize+bl.metadataSize+12)
        elif bl.type.value==0xffffff22:
            self.b=Block22(readLen=bl.dataSize+bl.metadataSize+12)
        elif bl.type.value==0xffffff31:
            self.b=Block31(readLen=bl.dataSize+bl.metadataSize+12)
        elif bl.type.value==0xffffff3b:
            self.b=Block3b(readLen=bl.dataSize+bl.metadataSize+12)
        elif bl.type.value==0xffffff45:
            self.b=Block45(readLen=bl.dataSize+bl.metadataSize+12)
        elif bl.type.value==0xffffff53:
            self.b=Block53(readLen=bl.dataSize+bl.metadataSize+12)
        elif bl.type.value==0xffffff54:
            self.b=Block54(readLen=bl.dataSize+bl.metadataSize+12)
        elif bl.type.value==0xffffff24:
            self.b=Block24(readLen=bl.dataSize+bl.metadataSize+12)
        elif bl.type.value==0xffffff52:
            self.b=Block52(readLen=bl.dataSize+bl.metadataSize+12)
        else:
            print "MYERROR:in Block__read__",hex(s.pos),s.pos/16,hex(bl.type.value)
            assert(0)
        s.readType(self.b)
        self.padding_=String(readLen=CallableValue((4-sizeof(self.b) % 4) % 4))
        s.readType(self.padding_)

    def __mutate__(self):
        CompositeType.__mutate__(self)
        self.padding_.value ="\x00"*((4-sizeof(self.b) % 4) % 4)


#14
class Block14(CompositeType):
    class BoundingSphere(CompositeType):
        def __inti__(self,readLen=None):
            CompositeType.__init__(self,readlen=readLen)
            self.centerx=UInt32Le()
            self.centery=UInt32Le()
            self.centerz=UInt32Le()
            self.radius=UInt32Le()
    class BoundingBox(CompositeType):
        def __inti__(self,readLen=None):
            CompositeType.__init__(self,readlen=readLen)
            self.minx=UInt32Le()
            self.miny=UInt32Le()
            self.minz=UInt32Le()
            self.maxx=UInt32Le()
            self.maxy=UInt32Le()
            self.maxz=UInt32Le()
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
        self.type_=UInt32Le()
        self.dataSize_=UInt32Le()
        self.metadataSize_=UInt32Le()
        self.name_=LString()
        self.chainType=UInt32Le()
        self.chainAttr_=UInt32Le()
        self.bsphere=Block14.BoundingSphere(conditional=(lambda:self.chainAttr_&0x1==0x1))
        self.bbox=Block14.BoundingBox(conditional=(lambda:self.chainAttr_&0x2==0x2))
        self.chainPadding=String(readLen=CallableValue( lambda:(4-(sizeof(self.name_))%4)%4 ))
        self.mArrCount_=UInt32Le()
        self.mArr=ArrayType(Block,readLen=CallableValue(lambda:self.mArrCount_))
        self.padding=String(readLen=CallableValue( lambda:(4-(sizeof(self.mArr))%4)%4 ))
    def __mutate__(self):
        CompositeType.__mutate__(self)
        self.chainPadding.value='\x00'*((4-(sizeof(self.name_))%4)%4)
        self.padding.value='\x00'*((4-(sizeof(self.mArr))%4)%4)
        self.dataSize_.value=sizeof(self)-12
#15
class Block15(CompositeType):
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
        self.type_=UInt32Le()
        self.dataSize_=UInt32Le()
        self.metadataSize_=UInt32Le()
        self.newPriority=UInt32Le()
    def __mutate__(self):
        CompositeType.mutate(self)
        self.dataSize_.value=sizeof(self)-12
class Block24(CompositeType):
    class Backdrop(CompositeType):
        def __init__(self,readLen=None):
            CompositeType.__init__(self,readLen=readLen)
            self.name_=LString()
            self.data=ArrayType(UInt32Le,readLen=CallableValue(8))
    class Overlay(CompositeType):
        def __init__(self,readLen=None):
            CompositeType.__init__(self,readLen=readLen)
            self.name_=LString()
            self.data=ArrayType(UInt32Le,readLen=CallableValue(8))
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
        self.type_=UInt32Le()
        self.dataSize_=UInt32Le()
        self.metadataSize_=UInt32Le()
        self.name_=LString()
        self.nodesCount_=UInt32Le()
        self.nodes=ArrayType(Block21.Node,readLen=CallableValue(lambda:self.nodesCount_.value))
        self.resName_=LString()
        self.nodeAttr_=UInt32Le()
        self.viewClip=ArrayType(UInt32Le,readLen=CallableValue(2))
        self.v1=UInt32Le(conditional=lambda :self.nodeAttr_==0)
        self.v2=UInt32Le(conditional=lambda :self.nodeAttr_&0x02==0x02)
        self.v3=ArrayType(UInt32Le,readLen=CallableValue(3),conditional=lambda :(self.nodeAttr_&0x04==0x04 or self.nodeAttr_&0x06==0x06))
        self.viewPoint=ArrayType(UInt32Le,readLen=CallableValue(4))
        self.backdropsCount=UInt32Le()
        self.backdrops=ArrayType(Block24.Backdrop,readLen=CallableValue(lambda :self.backdropsCount.value))
        self.overlaysCount=UInt32Le()
        self.overlays=ArrayType(Block24.Overlay,readLen=CallableValue(lambda :self.overlaysCount.value))
    def __mutate__(self):
        CompositeType.mutate(self)
        self.dataSize_.value=sizeof(self)-12
#3b
class Block3b(CompositeType):
    class MeshDescData(CompositeType):
        def __init__(self,readLen=None):
            CompositeType.__init__(self,readLen=readLen)
            self.faceCount=UInt32Le()
            self.posCount=UInt32Le()
            self.norCount=UInt32Le()
            self.dcolorCount=UInt32Le()
            self.scolorCount=UInt32Le()
            self.tcolorCount=UInt32Le()
            self.data=ArrayType(UInt32Le,readLen=CallableValue(lambda:(self._readLen.value-24)/4))
            self.mpadding_=String(readLen=CallableValue(lambda:(self._readLen.value-24)%4))
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
        self.type_=UInt32Le()
        self.dataSize_=UInt32Le()
        self.metadataSize_=UInt32Le()
        self.name_=LString()
        self.chainIndex=UInt32Le()
        self.meshDescData=Block3b.MeshDescData(readLen=CallableValue(lambda:self._readLen.value-sizeof(self.name_)-16))
    def __mutate__(self):
        CompositeType.mutate(self)
        self.dataSize_.value=sizeof(self)-12
class Block53(CompositeType):
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
        self.type_=UInt32Le()
        self.dataSize_=UInt32Le()
        self.metadataSize_=UInt32Le()
        self.name_=LString()
        self.attr=UInt32Le()
        self.ref=UInt32Le()
        self.alphaTestFun=UInt32Le()
        self.colorBlendFun=UInt32Le()
        self.flags=UInt32Le()
        self.shaderChannels=UInt32Le()
        self.textureChannels=UInt32Le()
        self.materialName_=LString()
        self.data=ArrayType(UInt32Le,readLen=CallableValue(lambda:(self._readLen.value-sizeof(self))/4))
    def __mutate__(self):
        CompositeType.mutate(self)
        self.dataSize_.value=sizeof(self)-12
class Block54(CompositeType):
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
        self.type_=UInt32Le()
        self.dataSize_=UInt32Le()
        self.metadataSize_=UInt32Le()
        self.name_=LString()
        self.attr=UInt32Le()
        self.ambColor=ArrayType(UInt32Le,readLen=CallableValue(lambda:3))
        self.difColor=ArrayType(UInt32Le,readLen=CallableValue(lambda:3))
        self.speColor=ArrayType(UInt32Le,readLen=CallableValue(lambda:3))
        self.emiColor=ArrayType(UInt32Le,readLen=CallableValue(lambda:3))
        self.ref=UInt32Le()
        self.opacity=UInt32Le()
        self.data=ArrayType(UInt32Le,readLen=CallableValue(lambda:(self._readLen.value-sizeof(self))/4))
    def __mutate__(self):
        CompositeType.mutate(self)
        self.dataSize_.value=sizeof(self)-12
class Block443355(CompositeType):
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
        self.type_=UInt32Le()
        self.dataSize_=UInt32Le()
        self.metadataSize_=UInt32Le()
        self.version=UInt32Le()
        self.profiler=UInt32Le()
        self.declarationSize=UInt32Le()
        self.fileSize=ArrayType(UInt32Le,readLen=CallableValue(lambda:2))
        self.encoding=UInt32Le()
        self.metaData=String(readLen=CallableValue(lambda:self.metadataSize_.value))
    def __mutate__(self):
        CompositeType.mutate(self)
        self.metadataSize_.value=sizeof(self.metaData)
        self.dataSize_.value=sizeof(self)-sizeof(self.metaData)-12
class Block21(CompositeType):
    class Node(CompositeType):
        def __init__(self,readLen=None):
            CompositeType.__init__(self,readLen=readLen)
            self.name_=LString()
            self.matElems=ArrayType(UInt32Le,readLen=CallableValue(lambda:16))
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
        self.type_=UInt32Le()
        self.dataSize_=UInt32Le()
        self.metadataSize_=UInt32Le()
        self.name_=LString()
        self.nodesCount_=UInt32Le()
        self.nodes=ArrayType(Block21.Node,readLen=CallableValue(lambda:self.nodesCount_.value))
    def __mutate__(self):
        CompositeType.mutate()
        self.dataSize_.value=sizeof(self)-12
class Block22(CompositeType):
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
        self.type_=UInt32Le()
        self.dataSize_=UInt32Le()
        self.metadataSize_=UInt32Le()
        self.name_=LString()
        self.nodesCount_=UInt32Le()
        self.nodes=ArrayType(Block21.Node,readLen=CallableValue(lambda:self.nodesCount_.value))
        self.resname_=LString()
        self.visibility=UInt32Le()
    def __mutate__(self):
        CompositeType.mutate()
        self.dataSize_.value=sizeof(self)-12
class Block31(CompositeType):
    class MeshDesc(CompositeType):
        class ShadingDesc(CompositeType):
            def __init__(self,readLen=None):
                CompositeType.__init__(self,readLen=readLen)
                self.attr=UInt32Le()
                self.coordsCount_=UInt32Le()
                self.coords=ArrayType(UInt32Le,readLen=CallableValue(lambda:self.coordsCount_.value))
                self.id=UInt32Le()
        def __init__(self,readLen=None):
            CompositeType.__init__(self,readLen=readLen)
            self.attr=UInt32Le()
            self.faceCount=UInt32Le()
            self.posCount=UInt32Le()
            self.norCount=UInt32Le()
            self.dcolorCount=UInt32Le()
            self.scolorCount=UInt32Le()
            self.tcolorCount=UInt32Le()
            self.shadingsCount_=UInt32Le()
            self.shadings=ArrayType(Block31.MeshDesc.ShadingDesc,readLen=CallableValue(lambda:self.shadingsCount_.value))
    class ClodDesc(CompositeType):
        def __init__(self,readLen=None):
            CompositeType.__init__(self,readLen=readLen)
            self.minRes=UInt32Le()
            self.finalMaxRes=UInt32Le()
    class ResDesc(CompositeType):
        def __init__(self,readLen=None):
            CompositeType.__init__(self,readLen=readLen)
            self.data=ArrayType(UInt32Le,readLen=CallableValue(lambda:11))
    class SkeDesc(CompositeType):
        class Bone(CompositeType):
            def __init__(self,readlen):
                CompositeType.__init__(self,readLen=None)
                self.name_=LString()
                self.pName_=LString()
                self.attrs=UInt32Le()
                self.mLength=UInt32Le()
                self.displacement=ArrayType(UInt32Le,readLen=CallableValue(lambda:3))
                self.orientation=ArrayType(UInt32Le,readLen=CallableValue(lambda:4))
                self.boneLinkCount=UInt32Le(conditional=lambda:(self.attrs.value &0x1)==0x1)
                self.boneLinkLength=UInt32Le(conditional=lambda:(self.attrs.value &0x1)==0x1)
                self.boneStartJoint=ArrayType(UInt32Le,readLen=CallableValue(lambda:4),conditional=(lambda:self.attrs.value&0x2==2))
                self.boneEndJoint=ArrayType(UInt32Le,readLen=CallableValue(lambda:4),conditional=(lambda:self.attrs.value&0x2==2))
                self.boneRotationConstraints=ArrayType(UInt32Le,readLen=CallableValue(lambda:6))
        def __init__(self,readLen=None):
            CompositeType.__init__(self,readLen=readLen)
            self.bonesCount=UInt32Le()

    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
        self.type_=UInt32Le()
        self.dataSize_=UInt32Le()
        self.metadataSize_=UInt32Le()
        self.name_=LString()
        self.chainIndex=UInt32Le()
        self.maxMeshDesc=Block31.MeshDesc()
        self.clodDesc=Block31.ClodDesc()
        self.resDesc=Block31.ResDesc()
        self.skeDesc=Block31.SkeDesc()
    def __mutate__(self):
        CompositeType.mutate()
        self.dataSize_.value=sizeof(self)-12

class Block45(CompositeType):
    class ShaderList(CompositeType):
        def __init__(self,readLen=None):
            CompositeType.__init__(self,readLen=readLen)
            self.names_Count_=UInt32Le()
            self.names_=ArrayType(LString,readLen=CallableValue(lambda:self.names_Count_.value))
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
        self.type_=UInt32Le()
        self.dataSize_=UInt32Le()
        self.metadataSize_=UInt32Le()
        self.name_=LString()
        self.chainIndex=UInt32Le()
        self.attrs_=UInt32Le()
        self.listsCount_=UInt32Le()
        self.lists=ArrayType(Block45.ShaderList,readLen=CallableValue(lambda:self.listsCount_.value))
    def __mutate__(self):
        CompositeType.mutate()
        self.dataSize_.value=sizeof(self)-12

class Block52(CompositeType):
    class Pass(CompositeType):
        def __init__(self,readLen=None):
            CompositeType.__init__(self,readLen=readLen)
            self.name_=LString()
            self.attr_=UInt32Le()
            self.fog=ArrayType(UInt32Le,readLen=CallableValue(7))
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
        self.type_ = UInt32Le()
        self.dataSize_ = UInt32Le()
        self.metadataSize_ = UInt32Le()
        self.name_ = LString()
        self.passesCount_=UInt32Le()
        self.passes=ArrayType(Block52.Pass,readLen=CallableValue(lambda :self.passesCount_.value))
    def __mutate__(self):
        CompositeType.mutate()
        self.dataSize_.value=sizeof(self)-12
class U3DStream(CompositeType):
    def __init__(self,readLen=None):
        CompositeType.__init__(self,readLen=readLen)
    
    def __read__(self,s):
        self.blocks=[]
        bl=BlockHeader()
        while s.dataLen()>0:
            if (4-s.pos%4)%4 !=0:
                s.read((4-s.pos%4)%4)
                if s.dataLen()<=0:
                    break
            s.readNextType(bl)
            if bl.type.value==0x443355:
                self.blocks.append(Block443355(readLen=bl.dataSize+bl.metadataSize+12))
            elif bl.type.value==0xffffff14:
                self.blocks.append(Block14(readLen=bl.dataSize+bl.metadataSize+12))
            elif bl.type.value==0xffffff15:
                self.blocks.append(Block15(readLen=bl.dataSize+bl.metadataSize+12))
            elif bl.type.value==0xffffff21:
                self.blocks.append(Block21(readLen=bl.dataSize+bl.metadataSize+12))
            elif bl.type.value==0xffffff22:
                self.blocks.append(Block22(readLen=bl.dataSize+bl.metadataSize+12))
            elif bl.type.value==0xffffff31:
                self.blocks.append(Block31(readLen=bl.dataSize+bl.metadataSize+12))
            elif bl.type.value==0xffffff3b:
                self.blocks.append(Block3b(readLen=bl.dataSize+bl.metadataSize+12))
            elif bl.type.value==0xffffff45:
                self.blocks.append(Block45(readLen=bl.dataSize+bl.metadataSize+12))
            elif bl.type.value==0xffffff53:
                self.blocks.append(Block53(readLen=bl.dataSize+bl.metadataSize+12))
            elif bl.type.value==0xffffff54:
                self.blocks.append(Block54(readLen=bl.dataSize+bl.metadataSize+12))
            elif bl.type.value==0xffffff24:
                self.blocks.append(Block24(readLen=bl.dataSize+bl.metadataSize+12))
            elif bl.type.value==0xffffff52:
                self.blocks.append(Block52(readLen=bl.dataSize+bl.metadataSize+12))
            else:
                print "MYERROR:"
                print "s.pos:",hex(s.pos),s.pos/16,"UnKnown Type:",hex(bl.type.value),"last_type:",\
                hex(self.blocks[-1].type_.value)
                assert(0)
            s.readType(self.blocks[-1])
            #print "s.pos:",hex(s.pos),s.pos/16,"UnKnown Type:",hex(bl.type.value),"last_type:"
            #raw_input()
    def __write__(self,s):
        for b in self.blocks :
            if (4-s.pos%4)%4!=0:
                s.write('\x00'*((4-s.pos%4)%4))
            s.writeType(b)
        if (4 - s.pos % 4) % 4 != 0:
            s.write('\x00' * ((4 - s.pos % 4) % 4))
    def __write_record__(self,s,d,prefix):
        start_pos=s.pos
        for i in range(0,len(self.blocks)):
            b=self.blocks[i]
            if (4 - s.pos % 4) % 4 != 0:
                s.write('\x00' * ((4 - s.pos % 4) % 4))
            b.write_record(s, d, prefix+"."+str(i)+"[%s]"%(b.__class__.__name__))
        if (4 - s.pos % 4) % 4 != 0:
            s.write('\x00' * ((4 - s.pos % 4) % 4))
        end_pos=s.pos
        d.append((prefix,start_pos,end_pos))

    def __mutate__(self):
        r=random.randint(1,5)
        rindexs=[]
        for i in range(0,len(self.blocks)):
            rindexs.append(i)
        indexs=random.sample(rindexs,r)
        #print indexs
        for i in indexs:
            self.blocks[i].mutate()
        self.blocks[0].fileSize._array[0].value = self.__sizeof__()
        self._is_readed=False
    def mutate(self):
        self.__mutate__()
    def __sizeof__(self):
        size=0
        for b in self.blocks:
            size+=(4-size%4)%4
            size+=sizeof(b)
        size += (4 - size % 4) % 4
        return size

def mutateU3d(u3ds):
    s=Stream(u3ds)
    u3d=U3DStream()
    s.readType(u3d)
    u3d.mutate()
    del s
    outs=Stream()
    outs.writeType(u3d)
    del u3d
    return outs.getvalue()

def test1():
    with open(sys.argv[1], "rb") as u3df:
        u3ds = u3df.read()
    s = Stream(u3ds)
    u3d = U3DStream()
    print "begin read u3d", time.time()
    s.readType(u3d)
    print "end read u3d", time.time()

    print "start mutate u3d", time.time()
    #u3d.mutate()
    print "end mutate u3d", time.time()
    outs = Stream()

    print "start write u3d", time.time()
    outs.writeType(u3d)
    print "end write u3d", time.time()

    ss1=outs.getvalue()
    ss2=s.getvalue()
    print ss1[0:min(len(ss1),len(ss2))] == ss2[0:min(len(ss1),len(ss2))]
    print len(outs.getvalue()),len(s.getvalue())
    for i in range(0,min(len(ss1),len(ss2))):
        if ss1[i] != ss2[i]:
            print "offset:",hex(i),i/16,hex(ord(ss1[i])),hex(ord(ss2[i]))

    u3d2 = U3DStream()
    outs.seek(0)

    with open("a.u3d", "wb") as f:
        f.write(outs.getvalue())

    print "start read u3d2", time.time()
    #outs.readType(u3d2)
    print "end read u3d2", time.time()
    del s,u3d,outs


def test2():
    with open(sys.argv[1], "rb") as u3df:
        u3ds = u3df.read()
    s = Stream(u3ds)
    u3d = U3DStream()
    print "begin read u3d", time.time()
    s.readType(u3d)
    print "end read u3d", time.time()

    dict={}
    for b in u3d.blocks:
        if b.type_.value not in dict.keys():
            dict[b.type_.value]=[sizeof(b)]
        else:
            dict[b.type_.value].append(sizeof(b))

    for key,value in dict.items():
        print hex(key),sum(value)/len(value),len(value)
def test3():
    with open(sys.argv[1], "rb") as u3df:
        u3ds = u3df.read()
    s = Stream(u3ds)
    u3d = U3DStream()
    print "begin read u3d", time.time()
    s.readType(u3d)
    print "end read u3d", time.time()

    outs = Stream()

    d=[]
    print "start write u3d", time.time()
    u3d.write_record(outs,d, "u3d["+u3d.__class__.__name__+"]")
    print "end write u3d", time.time()

    import  shelve

    '''with open("sample\\tu3d1_offset.txt","wb") as sf:
        for v in d:
            sf.write(str(v)+"\n")'''
    with open("sample\\tu3d.u3d","wb") as sf:
        sf.write(outs.getvalue())
    '''dat=shelve.open("sample\\tu3d1_offset.dat")
    dat["offset"]=d
    dat.close()'''

if "__main__"==__name__:
    test3()

