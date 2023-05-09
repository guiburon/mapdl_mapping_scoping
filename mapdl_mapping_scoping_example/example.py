from mapdl_mapping_scoping import MAPDLmapping

# ------ EXAMPLE ------
filename = "example.mapping"
        
maps = MAPDLmapping(filename)

nList = [1,3,10]
DOFlist = ("UX", "PRES")


# --- TESTING ---

print(maps.mapping)
print(maps.scoping.mapping) # empty DataFrame

maps.sort("node")
print(maps.mapping)

maps.sort("DOF")
print(maps.mapping)

# # as expected: no scoping done because no node or DOF type lists given
# maps.scope_mapping()
# print(maps.mapping)
# print(maps.scoping.mapping)

# sort by nodes: wrong node numbers are ignored
maps.scoping.nodes = nList
maps.scope_mapping()
print(maps.scoping.mapping)

# sort by DOF types: wrong DOF type raise error -> ADVANCED: additional valid DOF types can be given
maps.scoping.nodes = []
maps.scoping.DOFtypes = DOFlist
maps.scope_mapping()
print(maps.scoping.mapping)

# # as expected: wrong DOF type
# maps.scoping.nodes = []
# maps.scoping.DOFtypes = ("UX", "ivalid_DOF_type")
# maps.scope_mapping()

# sort by nodes and DOF types
maps.scoping.nodes = nList
maps.scoping.DOFtypes = DOFlist
maps.scope_mapping()
print(maps.scoping.mapping)


maps.sort("node")
print(maps.scoping.mapping)

maps.sort("DOF")
print(maps.scoping.mapping)

# extract DOF numbers
maps.sort("DOF")
print(maps.DOF())

maps.sort("node")
print(maps.DOF())

maps.sort("DOF")
print(maps.scoped_DOF())

maps.sort("node")
print(maps.scoped_DOF())