import pandas as pd
from copy import copy


class MAPDLmappingScoping:
    def __init__(self):
        self.mapping = pd.DataFrame()
        self.nodes = []
        self.DOFtypes = []
        self.valid_DOFtypes = {"UX", "UY", "UZ", "ROTX", "ROTY", "ROTZ", "PRES", "TEMP", "VOLT"} # can be manually enriched with additional MAPDL DOF types
        
        
class MAPDLmapping:
    def __init__(self, mapping_file):
        self.mapping = pd.read_csv(mapping_file, sep='\s+', lineterminator='\n', header=None, skiprows=1)
        self.mapping.columns = ["DOF_num","node_num","DOF_type"]
        self.scoping = MAPDLmappingScoping()
        
    # ------ sort the global and scoped mapping dataframes by node or DOF numbers ------
    def sort(self, by):
        if by == "node":
            self.mapping.sort_values(by=["node_num", "DOF_num"], inplace=True)
            if not(self.scoping.mapping.empty):
                self.scoping.mapping.sort_values(by=["node_num", "DOF_num"], inplace=True)
        elif by == "DOF":
            self.mapping.sort_values(by=["DOF_num"], inplace=True)
            if not(self.scoping.mapping.empty):
                self.scoping.mapping.sort_values(by=["DOF_num"], inplace=True)
        else:
            raise ValueError("sort: supports only sorting by \"node\" or \"DOF\"")
    
    # ------ scope global mapping by node list and/or DOF type list ------
    def scope_mapping(self):
        if not(set(self.scoping.DOFtypes).issubset(self.scoping.valid_DOFtypes)):
            raise ValueError("scope_mapping: scoping.DOFtypes: supported scoping DOF types are " + str(self.scoping.valid_DOFtypes))
        
        if len(self.scoping.nodes) > 0:  # if not empty node list
            self.scoping.mapping = self.mapping[self.mapping.node_num.isin(self.scoping.nodes)]
        else:
            self.scoping.mapping = copy(self.mapping) # deep copy
            
        if len(self.scoping.DOFtypes) > 0:   # if not empty DOF list
            self.scoping.mapping = self.scoping.mapping[self.scoping.mapping.DOF_type.isin(self.scoping.DOFtypes)]
    
    # ------ return global DOF list in current mapping sorting ------
    def DOF(self):
        return self.mapping.DOF_num.to_numpy()
    
    # ------ return scoped DOF list in current mapping sorting ------
    def scoped_DOF(self):
        if self.scoping.mapping.empty:
            DOFs = []
        else:
            DOFs = self.scoping.mapping.DOF_num.to_numpy()
        return DOFs
