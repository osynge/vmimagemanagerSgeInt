from vmDisk import diskFacade
from vmstorefacard import vmStoreFacade
import magic

import os

class StorageControler(object):
    def __init__(self,cfgModel):
        self.cfgModel = cfgModel
        self.diskFacardDict = {}
        self.Storage = vmStoreFacade()
        self.UpdateFromModel()
        
    def UpdateFromModel(self):
        self.Storage.storePath = self.cfgModel.defaultPathImages.get()
        itemsByName = self.cfgModel.vmbyName.keys()
        for item in itemsByName:
            if not item in self.diskFacardDict.keys():
                self.diskFacardDict[item] = diskFacade()
            
    def findByHostName(self,hostname): 
        matchset = self.diskFacardDict.keys()
        if hostname in matchset:
            return self.diskFacardDict[hostname]
        return None
    def store(self,hostname,storename):
        self.UpdateFromModel()
        hostDetails = diskFacade()
        hostDetails.disk = self.cfgModel.vmbyName[hostname].CfgDiskType.get()
        hostDetails.path = self.cfgModel.vmbyName[hostname].CfgDiskImage.get()
        hostDetails.target = self.cfgModel.vmbyName[hostname].CfgMountPoint.get()
        hostDetails.partitionNo = self.cfgModel.vmbyName[hostname].CfgDiskImagePartition.get()
        self.Storage.imageStore(hostDetails,storename)
    def restore(self,hostname,storename):
        if not hostname in self.cfgModel.vmbyName.keys():
            self.log.warning("No configuration for '%s'" % (hostname))
            return
        self.UpdateFromModel()
        path = os.path.join(self.Storage.storePath,storename)
        hostDetails = diskFacade()
        hostDetails.disk = self.cfgModel.vmbyName[hostname].CfgDiskType.get()
        hostDetails.path = self.cfgModel.vmbyName[hostname].CfgDiskImage.get()
        hostDetails.target = self.cfgModel.vmbyName[hostname].CfgMountPoint.get()
        hostDetails.partitionNo = self.cfgModel.vmbyName[hostname].CfgDiskImagePartition.get()
        self.Storage.imageRestore(hostDetails,storename)    
    def release(self,hostname):
        if not hostname in self.cfgModel.vmbyName.keys():
            self.log.warning("No configuration for '%s'" % (hostname))
            return
        hostDetails = diskFacade()
        hostDetails.disk = self.cfgModel.vmbyName[hostname].CfgDiskType.get()
        hostDetails.path = self.cfgModel.vmbyName[hostname].CfgDiskImage.get()
        hostDetails.target = self.cfgModel.vmbyName[hostname].CfgMountPoint.get()
        hostDetails.partitionNo = self.cfgModel.vmbyName[hostname].CfgDiskImagePartition.get()
        hostDetails.release()
    def mount(self,hostname):
        if not hostname in self.cfgModel.vmbyName.keys():
            self.log.warning("No configuration for '%s'" % (hostname))
            return
        hostDetails = diskFacade()
        hostDetails.disk = self.cfgModel.vmbyName[hostname].CfgDiskType.get()
        hostDetails.path = self.cfgModel.vmbyName[hostname].CfgDiskImage.get()
        hostDetails.target = self.cfgModel.vmbyName[hostname].CfgMountPoint.get()
        hostDetails.partitionNo = self.cfgModel.vmbyName[hostname].CfgDiskImagePartition.get()
        hostDetails.mount()
    def insert(self,hostname,storename,storeformat):
        if not hostname in self.cfgModel.vmbyName.keys():
            self.log.warning("No configuration for '%s'" % (hostname))
            return
        self.UpdateFromModel()
        foundHost = self.findByHostName(hostname)
        #print (hostname,storename,storeformat,self.cfgModel.vmbyName[hostname].CfgPathInserts.get())
        hostDetails = diskFacade()
        hostDetails.disk = self.cfgModel.vmbyName[hostname].CfgDiskType.get()
        hostDetails.path = self.cfgModel.vmbyName[hostname].CfgDiskImage.get()
        hostDetails.target = self.cfgModel.vmbyName[hostname].CfgMountPoint.get()
        hostDetails.partitionNo = self.cfgModel.vmbyName[hostname].CfgDiskImagePartition.get()
        self.Storage.storeFormat = storeformat
        self.Storage.storePath = self.cfgModel.vmbyName[hostname].CfgPathInserts.get()
        self.Storage.insertRestore(hostDetails,storename)
    def extract(self,hostname,storename,directory,storeformat):
        if not hostname in self.cfgModel.vmbyName.keys():
            self.log.warning("No configuration for '%s'" % (hostname))
            return
        self.UpdateFromModel()
        foundHost = self.findByHostName(hostname)
        #print (hostname,storename,storeformat,self.cfgModel.vmbyName[hostname].CfgPathInserts.get())
        hostDetails = diskFacade()
        hostDetails.disk = self.cfgModel.vmbyName[hostname].CfgDiskType.get()
        hostDetails.path = self.cfgModel.vmbyName[hostname].CfgDiskImage.get()
        hostDetails.target = self.cfgModel.vmbyName[hostname].CfgMountPoint.get()
        hostDetails.partitionNo = self.cfgModel.vmbyName[hostname].CfgDiskImagePartition.get()
        self.Storage.storeFormat = storeformat
        self.Storage.storePath = self.cfgModel.vmbyName[hostname].CfgPathInserts.get()
        self.Storage.insertStore(hostDetails,storename,directory)
    
    
    def returnFiileType(self,magicStr):
        cleanstring = str.strip(magicStr)
        splitString = dir(magicStr)
        splitLine = cleanstring.split(', ')
        if splitLine[0] == 'gzip compressed data':
            return "tgz"
        return None

    def listImages(self):
        output = {}
        availablepaths = set()
        pthInfo = {}
        allHosts = self.cfgModel.vmbyName.keys()
        if len(allHosts) == 0:
            availablepaths.add(self.cfgModel.defaultPathImages.get())
            pthInfo[self.cfgModel.defaultPathImages.get()] = []
        for host in allHosts:
            availablepaths.add(self.cfgModel.vmbyName[host].CfgPathImages.get())
            pth = self.cfgModel.vmbyName[host].CfgPathImages.get()
            if not pth in pthInfo.keys():
                pthInfo[pth] = { 'hosts' : [], 'images' : {}}
            pthInfo[pth]['hosts'].append(host)
        pathImages = {}
        StoreFacade = vmStoreFacade()
        ms = magic.open(magic.MAGIC_NONE)
        ms.load()
        
        for path in pthInfo.keys():
            if not os.path.isdir(path):
                continue
            for fileName in os.listdir(path):
                fileDetails = { 'Name' : fileName, 'Path' : path}
                fullPath = os.path.join(path,fileName)
                fileDetails['fullPath'] = fullPath
                if os.path.isdir(fullPath):
                    fileDetails["type"] = "rsync"
                elif os.path.isfile(fullPath):
                    magicout = ms.file(fullPath)
                    fileType = self.returnFiileType(magicout)
                    if fileType != None:
                        fileDetails["type"] = fileType
                output[fullPath] = fileDetails
        ms.close()
        return output